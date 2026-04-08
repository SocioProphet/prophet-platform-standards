# ADR-040: Tekton + ArgoCD + GitOps Strategy

**Status:** Accepted  
**Date:** 2026-04-06  
**Deciders:** Platform Engineering Team  
**Tags:** ci-cd, gitops, tekton, argocd, pipeline

---

## Context and Problem Statement

The SocioProphet platform requires a reproducible, auditable, cloud-native CI/CD strategy that:
- Supports multi-repo, multi-environment deployments
- Enforces supply-chain security (SLSA L3)
- Integrates with Kubernetes-native tooling
- Provides immutable audit trails for all build and deploy events
- Enables GitOps-style declarative configuration management

Existing ad-hoc deployment scripts and manual processes cannot scale to the requirements of a production-grade platform.

---

## Decision

**Use Tekton Pipelines for CI and ArgoCD for CD, following a GitOps model where Git is the single source of truth.**

### Requirements Language

Per RFC 2119:
- **MUST** — Mandatory requirement
- **SHOULD** — Recommended unless there is a specific reason not to
- **MAY** — Optional

---

## Tekton Pipelines (SHOULD)

### Rationale

Tekton is a Kubernetes-native, declarative CI/CD framework. It runs as Custom Resource Definitions (CRDs) inside the cluster, providing:
- Native pod-level isolation per task
- Declarative TaskRuns and PipelineRuns
- First-class support for SLSA supply chain provenance

### Requirements

1. All build and test pipelines **SHOULD** be defined as Tekton `Pipeline` resources stored in `tekton/`.
2. Every `PipelineRun` **MUST** be triggered by a webhook event and **MUST NOT** be executed manually in production.
3. Pipelines **SHOULD** implement SLSA Level 3 by:
   - Building in a hermetic environment
   - Generating provenance attestations (in-toto format)
   - Signing artifacts with cosign
   - Generating SBOMs with syft
4. `TaskRun` execution **MUST** be logged to the immutable audit log with: actor, action, timestamp, commit SHA, and ADR reference.
5. All Tekton `ServiceAccount` resources **MUST** follow the least-privilege model defined in ADR-050.

### Pipeline Structure

```
GitHub Webhook
    │
    ▼
EventListener (Tekton Triggers)
    │
    ▼
PipelineRun: build-test-deploy
    ├── Task: build        (docker build, cosign sign, syft SBOM, in-toto)
    ├── Task: test         (unit tests, integration tests, coverage ≥80%)
    ├── Task: deploy-staging (ArgoCD sync to staging)
    ├── Gate: manual-approval (prod only; automated for staging)
    └── Task: deploy-prod  (ArgoCD sync to prod)
```

### TaskRun Outputs

Each TaskRun **MUST** produce:
- `$(results.image-digest)` — SHA256 digest of built image
- `$(results.sbom-url)` — Location of generated SBOM
- `$(results.attestation-url)` — Location of provenance attestation
- `$(results.signature)` — cosign signature reference

---

## ArgoCD Deployments (SHOULD)

### Rationale

ArgoCD implements the GitOps pull model: the cluster state is continuously reconciled to match the desired state declared in Git. This provides:
- Automatic drift detection and remediation
- Full deployment history in Git
- Multi-environment promotion via branch/path strategies
- Built-in rollback via `git revert`

### Requirements

1. All application deployments **SHOULD** be managed by ArgoCD `Application` resources stored in `argocd/`.
2. Git repositories **MUST** be the authoritative source of truth for cluster state. Direct `kubectl apply` to production **MUST NOT** be used.
3. ArgoCD **SHOULD** be configured with automatic sync and self-healing enabled for staging environments.
4. Production promotion **MUST** require a manual sync gate (enforced via ArgoCD sync policy `automated: false` or `syncOptions: ManualSync`).
5. All ArgoCD `AppProject` resources **MUST** define source repo allowlists and destination cluster restrictions.
6. Rollback **MUST** be performed via `git revert` + ArgoCD sync, not via direct cluster manipulation.
7. ArgoCD **SHOULD** emit deployment events to the OTEL collector (ADR-060) and audit log (ADR-050).

### Sync Policy

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
    - ServerSideApply=true
  retry:
    limit: 3
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

---

## Event Flow

```
1. Developer pushes commit to GitHub
2. GitHub webhook fires → Tekton EventListener
3. Tekton PipelineRun triggered:
   a. Task: build → container image built, signed (cosign), SBOM (syft), provenance (in-toto)
   b. Task: test  → unit + integration tests, coverage ≥80%
   c. Task: deploy-staging → ArgoCD Application synced to staging
4. Staging smoke tests run automatically
5. (Manual gate for prod) → ArgoCD Application synced to prod
6. Deployment event → OTEL collector → Prometheus/Loki/Jaeger
7. All events → immutable Postgres audit log
```

---

## Status Tracking

All pipeline events **MUST** be written to the audit log as immutable records:

| Field | Value |
|-------|-------|
| `actor` | GitHub user or ServiceAccount |
| `action` | `pipeline.run`, `task.complete`, `deploy.staging`, `deploy.prod` |
| `timestamp` | ISO 8601 UTC |
| `commit_sha` | Git commit that triggered the run |
| `adr_reference` | `ADR-040` |
| `status` | `success`, `failure`, `in_progress` |
| `pipeline_run_name` | Tekton PipelineRun name |
| `image_digest` | SHA256 of built image |

---

## Options Considered

### Option A: GitHub Actions (Rejected)
- **Pros:** Familiar, no infrastructure required, large ecosystem
- **Cons:** Not Kubernetes-native, limited SLSA support, vendor lock-in to GitHub, secrets managed externally, poor auditability for K8s environments

### Option B: GitLab CI (Rejected)
- **Pros:** Integrated with GitLab, good pipelines
- **Cons:** Requires GitLab SCM migration, not K8s-native, additional vendor dependency

### Option C: Jenkins (Rejected)
- **Pros:** Mature, large plugin ecosystem
- **Cons:** Not cloud-native, requires dedicated infrastructure, Groovy DSL complexity, poor K8s integration, security challenges

### Option D: Argo Workflows (Partially Adopted)
- **Pros:** K8s-native DAG workflows
- **Cons:** Not purpose-built for CI/CD, lacks Tekton's supply chain security features
- **Resolution:** Argo Workflows may be used for data pipelines; Tekton is preferred for CI/CD

### Option E: Tekton + ArgoCD (Chosen)
- **Pros:** K8s-native, declarative, SLSA support, GitOps model, strong audit trail, community backing (CNCF)
- **Cons:** Steeper learning curve, requires K8s cluster

---

## Tradeoffs

| Concern | Impact | Mitigation |
|---------|--------|------------|
| Complexity vs. control | Higher operational complexity | Comprehensive documentation; standardized templates in this repo |
| Kubernetes dependency | Platform requires K8s | Already a platform requirement |
| Learning curve | Team training needed | Guides in `docs/`; pair programming sessions |
| Build latency (+signing) | ~30s added per build | Acceptable for production security posture; parallelized where possible |
| Vendor neutrality | Reliance on CNCF projects | Both Tekton and ArgoCD are CNCF-graduated; no single-vendor lock-in |

---

## Measurement Plan

The following metrics **MUST** be tracked to validate this ADR's effectiveness:

| Metric | Target | Collection Method |
|--------|--------|------------------|
| Build duration p95 | < 10 minutes | Tekton PipelineRun duration → Prometheus |
| Deploy success rate | ≥ 95% | ArgoCD sync status → Prometheus |
| Rollback frequency | < 2% of deployments | Audit log query |
| SLSA provenance coverage | 100% of images | Attestation store |
| Pipeline-as-code adoption | 100% of services | ADR compliance check |

---

## Consequences

### Positive
- Full traceability: every artifact can be traced back to a commit, actor, and pipeline run
- GitOps model: deployments are reproducible and auditable
- Hermetic builds: reduced supply chain risk
- SLSA L3: meets enterprise security requirements

### Negative
- Kubernetes is a hard dependency for the CI/CD infrastructure
- Tekton has a steeper learning curve than traditional CI systems
- Initial setup cost is higher than simpler alternatives

### Neutral
- All new services onboarded to the platform **MUST** use these pipelines
- Existing manual deployment processes **MUST** be migrated within 90 days of ADR acceptance

---

## Related ADRs

- [ADR-050](ADR-050-devsecops-rbac-audit.md) — DevSecOps, RBAC, and Audit Standards
- [ADR-060](ADR-060-otel-observability.md) — OTEL Observability and Telemetry Standards

---

## References

- [Tekton Pipelines](https://tekton.dev/docs/pipelines/)
- [ArgoCD GitOps](https://argo-cd.readthedocs.io/)
- [SLSA Framework](https://slsa.dev/)
- [cosign](https://docs.sigstore.dev/cosign/overview/)
- [syft SBOM](https://github.com/anchore/syft)
- [in-toto attestations](https://in-toto.io/)
