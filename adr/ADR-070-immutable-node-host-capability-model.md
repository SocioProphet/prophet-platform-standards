# ADR-070: Immutable Node Host Capability Model

**Status:** Draft  
**Date:** 2026-04-13  
**Deciders:** Platform Architecture, Runtime Engineering, Security Engineering, Operations  
**Tags:** immutable-linux, bootc, ostree, host-runtime, quadlet, systemd, rollback

---

## Context and Problem Statement

The current standards repository defines DevSecOps, RBAC, and observability norms, but it does not yet define how Socios host capabilities should be placed, promoted, and rolled back on immutable Linux systems.

Without a normative placement model, host-runtime work risks collapsing into one of two bad patterns:

1. mutable host drift that breaks transactional semantics and rollback discipline; or
2. an unbounded mix of host logic, service logic, and mutable state with no clear trust boundary.

Socios needs a model that works cleanly with bootc-first, OSTree-compatible hosts while remaining explicit about:

- which functions belong in the image;
- which functions may be additive extensions;
- which services belong in Quadlet-managed containers;
- where authoritative mutable state must live;
- how upgrades and rollback behave when `/var` survives but the host deployment changes.

---

## Decision

The platform SHALL adopt a host capability placement model for immutable Linux nodes with six canonical placement classes:

1. image-baked host capability;
2. sysext host capability;
3. confext policy/config capability;
4. Quadlet-bound service workload;
5. Quadlet-floating service workload;
6. `/var` state object.

### Requirements Language

Per RFC 2119: MUST = mandatory, SHOULD = recommended, MAY = optional.

---

## Host Capability Placement Model (MUST)

### Rationale

Immutable hosts behave well only when program tree, configuration, and durable mutable state are treated as distinct control surfaces.

The platform therefore needs a placement grammar that makes lifecycle coupling explicit.

### Requirements

1. Every Socios capability MUST have exactly one canonical placement class.
2. `/etc` MUST remain declarative and MUST NOT become a mutable operational database.
3. Authoritative mutable state MUST live under `/var/lib/socios/`.
4. Image-baked host capabilities MUST be composed and promoted with the host image.
5. sysext packs MUST remain additive and MUST NOT hide baseline trust logic.
6. confext packs MUST remain declarative and SHOULD prefer drop-ins over whole-file replacement.
7. Critical service workloads MUST be expressed as system-level Quadlet units.
8. Critical services SHOULD be lifecycle-coupled to the host release and pinned by digest.
9. Floating services MAY move independently but MUST declare compatibility with the active host release.
10. Rollback-sensitive state MUST define explicit schema compatibility expectations.

---

## Linux Privileged Surfaces (SHOULD)

### Rationale

Socios should not invent kernel-resident mechanisms casually when existing Linux surfaces provide reviewable and portable control points.

### Requirements

1. The platform SHOULD prefer eBPF for runtime observability and selected enforcement hooks.
2. The platform SHOULD prefer nftables for host packet policy realization.
3. The platform SHOULD use Linux Audit for compliance-grade watch rules and supporting evidence.
4. The platform SHOULD use systemd for lifecycle, credentials, tmpfiles, and service hardening.
5. The platform SHOULD use Quadlet for system-managed container services.
6. Custom kernel modules SHOULD be rejected by default unless a specific exception case is documented.

---

## Rollout Model (MUST)

### Rationale

Host transactionality is only useful if rollout discipline respects the underlying deployment semantics.

### Requirements

1. Production hosts MUST use transactional image upgrades.
2. Staged deployment workflows SHOULD be the default upgrade path.
3. Live mutation of `/usr` in production MUST NOT be the default path.
4. Bound service images MUST be reviewed together with host promotions.
5. Floating service promotions MUST be policy-gated.
6. Durable state readers SHOULD support N and N-1 compatibility for at least one host release generation.

---

## Options Considered

### Option A: Mutable Host Control Plane (Rejected)
- **Pros:** Fast iteration, minimal initial packaging discipline.
- **Cons:** Breaks immutable-host semantics, weak rollback posture, invites drift, weakens auditability.

### Option B: All Functionality in the Host Image (Partially Adopted)
- **Pros:** Maximal lifecycle coherence.
- **Cons:** Over-couples optional features and ordinary services to host image rebuilds.

### Option C: Placement Model with Image, Extensions, Quadlet, and `/var` State (Accepted)
- **Pros:** Clear trust boundaries, explicit rollout coupling, compatible with immutable-host semantics.
- **Cons:** Requires more up-front standards work and release discipline.

---

## Tradeoffs

| Concern | Impact | Mitigation |
|---------|--------|------------|
| `/etc` drift | Can invalidate repeatability | Keep `/etc` declarative; move mutable truth to `/var` |
| `/var` survives rollback | Reader/writer compatibility burden | Version schemas and enforce N/N-1 compatibility |
| Too many bound services | Slows host promotion cadence | Bind only critical services |
| Too many floating services | Compatibility split-brain risk | Require declared compatibility and policy-gated rollout |

---

## Measurement Plan

| Metric | Target | Collection Method |
|--------|--------|------------------|
| Capabilities with explicit placement | 100% | Standards review checklist |
| Host services using hardening directives | 100% of privileged units | Unit lint and review |
| Critical services digest-pinned | 100% | CI policy validation |
| Rollback test pass rate | 100% for reference node profile | Integration test on immutable-node lane |
| `/etc` mutation incidents in steady-state | 0 | Evidence audit and compliance checks |

---

## Consequences

### Positive
- Clear trust boundaries between host code, service workloads, and durable state.
- Stronger upgrade and rollback discipline.
- Better alignment with bootc-first and OSTree-compatible hosts.
- Better auditability and standards review.

### Negative
- Requires more explicit packaging and release policy work.
- Increases up-front doc and review burden.

### Neutral
- Does not select a single distribution or vendor substrate by itself.

---

## Related ADRs

- [ADR-040-tekton-argocd-gitops.md](ADR-040-tekton-argocd-gitops.md)
- [ADR-050-devsecops-rbac-audit.md](ADR-050-devsecops-rbac-audit.md)
- [ADR-060-otel-observability.md](ADR-060-otel-observability.md)

---

## References

- `docs/HOST_CAPABILITY_MODEL.md`
- `docs/IMMUTABLE_NODE_GUIDE.md`
