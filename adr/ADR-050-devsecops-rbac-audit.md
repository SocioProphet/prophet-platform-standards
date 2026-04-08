# ADR-050: DevSecOps, RBAC, and Audit Standards

**Status:** Accepted  
**Date:** 2026-04-06  
**Deciders:** Platform Engineering, Security Team  
**Tags:** devsecops, rbac, audit, security, compliance

---

## Context and Problem Statement

The SocioProphet platform handles multi-tenant, multi-repo workloads with varying levels of sensitivity. Without a formal security model, the platform is vulnerable to:
- Unauthorized access to cluster resources
- Unaudited deployment activity
- Supply chain attacks (unsigned images, unverified dependencies)
- Secrets sprawl and misconfiguration
- Compliance gaps (SOC2, FIPS-140)

This ADR establishes mandatory security, RBAC, audit logging, secrets management, and policy-as-code standards.

---

## Decision

**Implement a defense-in-depth DevSecOps model with mandatory RBAC, immutable audit logging, secrets management, and policy-as-code enforcement.**

### Requirements Language

Per RFC 2119:
- **MUST** — Mandatory requirement
- **SHOULD** — Recommended unless there is a specific reason not to
- **MAY** — Optional

---

## RBAC Model (MUST)

### Persona Definitions

All access to platform resources **MUST** be controlled through one of the following defined personas:

| Persona | Description | Allowed Actions |
|---------|-------------|-----------------|
| **Admin** | Cluster operators only | Full cluster access; create/delete namespaces, nodes, ClusterRoles |
| **Developer** | Application developers | Read pods, logs, events; exec port-forward; view deployments |
| **Deployer** | CI/CD and release engineers | Deploy to staging/prod; approve promotions; trigger PipelineRuns |
| **Auditor** | Compliance and security | Read-only audit logs; read pod events; view deployments |

### Requirements

1. Every human user **MUST** be bound to exactly one persona ClusterRole.
2. Every workload **MUST** run under a dedicated `ServiceAccount` — shared service accounts **MUST NOT** be used.
3. All `ServiceAccount` resources **MUST** be namespace-scoped to `sociosphere` unless explicitly justified.
4. `ClusterAdmin` bindings **MUST NOT** be granted to any workload service account or developer persona.
5. RBAC bindings **MUST** be defined in code (stored in `rbac/`) and applied via GitOps — not manually with `kubectl`.
6. Namespace isolation **MUST** be enforced: workloads in `sociosphere` **MUST NOT** access resources in other namespaces except via explicit RBAC grant.

### ServiceAccount Model

```
Namespace: sociosphere
├── ServiceAccount: webhook-sa       → webhook deployment
│     Roles: read ConfigMap, write Queue, trigger Tekton PipelineRun
├── ServiceAccount: scheduler-sa     → scheduler deployment
│     Roles: trigger Tekton, update registry, query GitHub API
├── ServiceAccount: tekton-build-sa  → Tekton build tasks
│     Roles: push to registry, write attestation store
└── ServiceAccount: argocd-sa        → ArgoCD application controller
      Roles: managed by ArgoCD; scoped to destination namespaces
```

---

## Audit Capture at Build Time (MUST)

### Requirements

1. Every Tekton `TaskRun` and `PipelineRun` **MUST** emit an audit event to the immutable audit log.
2. Audit events **MUST** capture:
   - `actor`: GitHub user ID or ServiceAccount name
   - `action`: Task name (e.g., `task.build`, `task.test`, `pipeline.deploy`)
   - `timestamp`: ISO 8601 UTC
   - `reason`: Git commit SHA + ADR reference (e.g., `commit:abc123 adr:ADR-040`)
   - `status`: `success`, `failure`, or `in_progress`
3. Build artifacts **MUST** be signed using `cosign` with ephemeral keys (Sigstore keyless signing).
4. SBOMs **MUST** be generated for every container image using `syft` in SPDX or CycloneDX format.
5. Provenance attestations **MUST** be generated in `in-toto` format and stored alongside the image in the registry.
6. The audit log **MUST** be stored in Postgres with append-only semantics. Records **MUST NOT** be modified or deleted.
7. The audit log **MUST** be queryable by: commit SHA, actor, timestamp range, action type, and policy reference.
8. Audit log write latency **MUST** be < 100ms (p99).

### Audit Log Schema

See `schemas/audit-log-schema.avro` for the canonical schema. Key fields:

```
AuditEvent {
  id:            UUID (primary key)
  timestamp:     Unix epoch milliseconds
  actor {
    user_id:       GitHub user or null
    service_account: SA name or null
    ip_address:    Source IP or null
  }
  action:        String (e.g., "task.build", "deploy.prod")
  resource {
    repo:          GitHub repo full name
    ref:           Branch or tag
    path:          File path (optional)
  }
  status:        Enum [success, failure, in_progress]
  details:       JSON string with additional context
  adr_reference: ADR ID (e.g., "ADR-040")
  signature:     cosign signature reference
  trace_id:      OTEL trace ID for correlation
}
```

---

## Secrets Management

### Requirements

1. Kubernetes `Secret` resources **MUST** be managed with `Sealed Secrets` (Bitnami) for secrets stored in Git.
2. Secrets from external vaults (HashiCorp Vault, AWS Secrets Manager) **MUST** be synchronized using `external-secrets-operator`.
3. All secrets **MUST** have a rotation policy. The default rotation interval is **30 days**.
4. Secret access events **MUST** be logged to the audit system with actor, secret name (not value), and timestamp.
5. Plaintext secrets **MUST NOT** appear in Git, container images, logs, or environment variable dumps.
6. Secrets **MUST** be mounted as volumes, not injected as environment variables, where the framework supports it.

### Secret Rotation

```
Secret lifecycle:
  Created → Active (30 days) → Rotation Warning (day 25) → Rotated → Old version archived
  
Failure to rotate:
  Day 30: Alert (warning)
  Day 35: Alert (critical) → Page on-call
  Day 40: Automated rotation or incident escalation
```

---

## Policy as Code

### Requirements

1. All admission-time policies **MUST** be implemented using `Kyverno` and stored in `policies/`.
2. Policies **MUST** be enforced in `Enforce` mode (not `Audit` only) for production clusters.
3. The following policies are **MANDATORY**:

| Policy | Effect | Description |
|--------|--------|-------------|
| `policy-signed-images` | Reject | All container images must be cosign-signed by an authorized key |
| `policy-fips-validation` | Reject | Images must pass FIPS-140 compliance scan |
| `policy-resource-limits` | Reject | All pods must define CPU and memory limits |
| `policy-pod-security` | Reject | No privileged pods, read-only rootfs, non-root user, no host networking |

4. Policy exceptions **MUST** be documented as ADR amendments and approved by the Security Team.
5. Policy violations **MUST** be logged to the audit system and trigger a critical alert (ADR-060).

### FIPS-140 Validation

- Container images **MUST** use FIPS-validated cryptographic modules.
- The FIPS scanner **MUST** be run as part of the Tekton build pipeline before image push.
- Images failing FIPS validation **MUST** be rejected at both build time (pipeline failure) and admission time (Kyverno policy).

---

## Compliance Tracking

### Build-Time Checks

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Image signing | cosign | Signature present in registry |
| SBOM generation | syft | SBOM stored alongside image |
| FIPS validation | FIPS scanner | No FIPS violations |
| Vulnerability scan | grype | No critical CVEs |

### Runtime Checks

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Pod security | Kyverno | No privileged pods, non-root |
| Network policies | Kyverno + CNI | All pods have NetworkPolicy |
| Resource limits | Kyverno | All pods have CPU/memory limits |
| Image signatures | Kyverno | All running images are signed |

### Post-Deploy Checks

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Vulnerability rescan | grype (scheduled) | No new critical CVEs in 24h |
| RBAC drift | kube-bench | No ClusterAdmin bindings to workloads |
| Audit log coverage | Custom query | 100% of deploys have audit events |

---

## Failure Modes

| Event | Response |
|-------|----------|
| Unsigned image detected at admission | Pod rejected; alert sent; audit event written |
| Expired cosign certificate | Alert sent; pipeline blocked until renewal |
| FIPS validation failure | Build pipeline fails; image not pushed |
| Secret rotation overdue | Warning at day 25; critical + page at day 35 |
| RBAC violation attempt | Kubernetes API server rejects; audit event written |
| Audit log write failure | Pipeline paused; on-call paged; data not lost (retry queue) |

---

## Measurement Plan

| Metric | Target | Collection Method |
|--------|--------|------------------|
| % builds with valid signatures | ≥ 95% | Audit log query |
| Audit log write latency (p99) | < 100ms | Prometheus histogram |
| Policy violation count | 0 critical/week | Kyverno metrics → Prometheus |
| SBOM coverage | 100% of images | Registry attestation check |
| Secret rotation compliance | 100% within SLA | Secrets management tool metrics |
| FIPS compliance rate | 100% | Pipeline metrics |

---

## Consequences

### Positive
- Full supply chain traceability: every artifact is signed, attested, and auditable
- Compliance-ready: SOC2 Type II, FIPS-140, SLSA L3
- Automated policy enforcement: no manual security gates to forget
- Immutable audit trail: tamper-evident log for forensic and compliance use

### Negative
- Build latency increases by ~30 seconds for signing, SBOM, and attestation generation
- Postgres is required for the audit log store
- Team training required for Kyverno, cosign, and sealed-secrets
- Operational complexity increases with additional tools

### Neutral
- All new services **MUST** implement these standards before deploying to production
- Existing services **MUST** migrate within 90 days of ADR acceptance

---

## Related ADRs

- [ADR-040](ADR-040-tekton-argocd-gitops.md) — Tekton + ArgoCD + GitOps Strategy
- [ADR-060](ADR-060-otel-observability.md) — OTEL Observability and Telemetry Standards

---

## References

- [cosign / Sigstore](https://docs.sigstore.dev/)
- [syft SBOM generator](https://github.com/anchore/syft)
- [in-toto attestation framework](https://in-toto.io/)
- [Kyverno Policy Engine](https://kyverno.io/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [external-secrets-operator](https://external-secrets.io/)
- [SLSA Framework](https://slsa.dev/)
- [FIPS 140-2](https://csrc.nist.gov/publications/detail/fips/140/2/final)
