# ADR-070: OS Build / Cybernetic Boundary

**Status:** Proposed  
**Date:** 2026-04-15  
**Deciders:** Platform Engineering Team  
**Tags:** sourceos, bootc, image-builds, policy, runtime-governance

---

## Context and Problem Statement

The platform is formalizing a three-plane contract seam in `SourceOS-Linux/sourceos-spec`:

- `OSImage` — immutable host image identity and substrate contract
- `NodeBinding` — install-time or enrollment-time mutable assignment
- `CyberneticAssignment` — runtime identity, policy, telemetry, relation, and control semantics

Without a platform-standard interpretation of that seam, downstream implementations risk mixing runtime meaning into image identity, or encoding install-time binding concerns inside runtime policy profiles.

This repository already owns canonical platform ADRs, CI/CD templates, Kyverno policy examples, OTEL guidance, and runtime profiles. It is therefore the correct place to define how platform operators should consume the new SourceOS contract family once the upstream schemas are merged.

---

## Decision

Adopt the OS build / cybernetic boundary as a first-class additive platform standard.

### Required interpretation

1. **OSImage is substrate-only.**
   It may define boot/update/attestation/runtime-substrate facts, but it MUST NOT encode deployment environment, topology, runtime service identity, or control-loop semantics.

2. **NodeBinding is mutable assignment.**
   It owns topology, fleet, update ring, installer profile, registry mirrors, and bootstrap trust-root selection.

3. **CyberneticAssignment is runtime meaning.**
   It owns service identity, deployment environment projection, policy refs, graph relations, and control objectives.

4. **Validation gates must fail closed** when cybernetic fields appear in OS image metadata or when substrate-only identity fields are smuggled into runtime assignment objects.

5. **Platform release artifacts SHOULD surface the seam explicitly** so that release approval, rollout, replay, and rollback can distinguish substrate drift from policy/runtime drift.

---

## Platform consequences

### CI/CD and release engineering

- Build pipelines SHOULD validate `OSImage` contracts before image publication.
- Promotion and rollout logic SHOULD evaluate `NodeBinding` separately from image publication.
- Runtime deployment and governance surfaces SHOULD consume `CyberneticAssignment` as a post-image semantic layer.

### Policy

- Kyverno / admission examples in this repository SHOULD reject environment/topology/runtime-role leakage into immutable OS image metadata.
- Release approval checklists SHOULD require proof that the three-plane split remains intact.

### Observability

- OTEL guidance SHOULD treat runtime service identity as a `CyberneticAssignment` concern, not an `OSImage` concern.
- Evidence should preserve enough linkage to distinguish image changes, node-binding changes, and cybernetic/runtime changes.

---

## Options Considered

### Option A: Treat all three layers as one deployable profile (Rejected)
- **Pros:** fewer objects
- **Cons:** destroys replayability and confuses immutable substrate identity with runtime meaning

### Option B: Keep the seam only in upstream SourceOS schemas (Rejected)
- **Pros:** avoids duplicate interpretation docs
- **Cons:** leaves platform implementers without operator guidance or policy examples

### Option C: Add a platform ADR and runtime profile (Chosen)
- **Pros:** preserves upstream contract authority while making platform rollout, policy, and observability expectations explicit
- **Cons:** requires follow-on template and policy work

---

## Consequences

### Positive
- Clean separation between image publication, node enrollment, and runtime control semantics
- Better release evidence and drift attribution
- Lower risk of immutable-image naming rot or environment leakage

### Negative
- Requires follow-on updates to policy templates and rollout guides
- Depends on upstream merge of the new `sourceos-spec` contract family

---

## Related ADRs

- [ADR-040](ADR-040-tekton-argocd-gitops.md) — Tekton + ArgoCD + GitOps Strategy
- [ADR-050](ADR-050-devsecops-rbac-audit.md) — DevSecOps, RBAC, and Audit Standards
- [ADR-060](ADR-060-otel-observability.md) — OTEL Observability and Telemetry Standards

---

## References

- `SourceOS-Linux/sourceos-spec` draft seam PR: `feat(spec): introduce OSImage / NodeBinding / CyberneticAssignment seam`
- `docs/profiles/sourceos-os-build-runtime-profile-v1.md`
