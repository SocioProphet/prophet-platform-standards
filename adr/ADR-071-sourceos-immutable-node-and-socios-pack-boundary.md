# ADR-071: SourceOS Immutable Node and Socios Pack Boundary

**Status:** Draft  
**Date:** 2026-05-04  
**Deciders:** Platform Architecture, SourceOS Runtime, Socios Commons, Security Engineering, Operations  
**Tags:** sourceos, socios, immutable-linux, bootc, ostree, host-runtime, optional-capability-pack

---

## Context and Problem Statement

ADR-070 introduced the immutable-node host capability placement model for bootc-first, OSTree-compatible Linux systems. That model remains useful, but the surrounding repository estate has clarified an important boundary:

- **SourceOS** is the base Linux substrate.
- **Socios** is an opt-in automation commons and personalization/orchestration layer.

The standards language must not imply that Socios is a mandatory dependency of the base SourceOS node. SourceOS must be able to boot, install, recover, update, roll back, validate, and emit evidence without requiring enrollment into the Socios commons.

At the same time, Socios may provide optional host capability packs after explicit enrollment, Proof-of-Life, signed intent, and policy approval.

---

## Decision

The platform SHALL split immutable-node language into two layers:

1. **SourceOS Immutable Node Profile** — mandatory base substrate policy for immutable Linux nodes.
2. **Socios Host Capability Pack** — optional automation/personalization/update commons activated only after explicit enrollment.

ADR-070 remains the generic placement grammar. ADR-071 clarifies authority, naming, and dependency direction.

### Requirements Language

Per RFC 2119: MUST = mandatory, SHOULD = recommended, MAY = optional.

---

## SourceOS Immutable Node Profile (MUST)

### Rationale

SourceOS must remain independently bootable and operable without optional community automation.

### Requirements

1. SourceOS immutable node capability MUST NOT depend on Socios enrollment.
2. SourceOS base node profiles MUST own mandatory boot, install, recovery, update, rollback, and local evidence requirements.
3. SourceOS base node profiles SHOULD use ADR-070 placement classes for image-baked capabilities, sysext, confext, Quadlet-bound workloads, Quadlet-floating workloads, and `/var` state.
4. SourceOS base node profiles MUST be expressible through machine-readable contracts in `SourceOS-Linux/sourceos-spec`.
5. SourceOS boot and recovery handoff MUST remain owned by `SourceOS-Linux/sourceos-boot` or its successor boot/recovery authority.
6. Local node runtime rendering, validation, activation, and receipts SHOULD be implemented by `SourceOS-Linux/agent-machine` where agent runtime substrate is involved.
7. Operator dry-run planning and inspection SHOULD be exposed through `SourceOS-Linux/sourceos-devtools` / `sourceosctl`.

---

## Socios Host Capability Pack (MAY)

### Rationale

Socios is valuable as an opt-in automation commons, but it must not become ambient base-node authority.

### Requirements

1. Socios host capabilities MUST be optional.
2. Socios host capabilities MUST require explicit enrollment before activation.
3. Enrollment MUST require Proof-of-Life and signed intent where user/device personalization, automation, or commons participation is involved.
4. Socios host capabilities MUST NOT silently mutate base SourceOS host state.
5. Socios host capabilities SHOULD be represented as optional capability packs, confext/sysext overlays, Quadlet services, or governed automation workflows rather than as mandatory base substrate.
6. Socios automation MUST emit evidence consumable by AgentPlane, Policy Fabric, or the applicable governance ledger.

---

## Authority Map

| Concern | Authority |
|---|---|
| Generic immutable host placement grammar | `SocioProphet/prophet-platform-standards` |
| Machine-readable SourceOS node contracts | `SourceOS-Linux/sourceos-spec` |
| Boot/recovery/install/rollback handoff | `SourceOS-Linux/sourceos-boot` |
| Local node runtime rendering and activation | `SourceOS-Linux/agent-machine` |
| Operator CLI validation and planning | `SourceOS-Linux/sourceos-devtools` |
| Execution, replay, and evidence consumption | `SocioProphet/agentplane` |
| Platform deployment/runtime consumption | `SocioProphet/prophet-platform` |
| Workspace topology and cross-repo governance | `SocioProphet/sociosphere` |
| Optional automation commons | `SociOS-Linux/socios` |

---

## Options Considered

### Option A: Treat Socios as mandatory immutable-node substrate (Rejected)
- **Pros:** Single named host automation layer.
- **Cons:** Violates SourceOS independence, conflicts with Socios opt-in posture, and risks ambient automation authority.

### Option B: Move all immutable-node standards to SourceOS repos only (Rejected)
- **Pros:** Keeps SourceOS substrate language local.
- **Cons:** Loses platform-wide placement grammar and cross-repo governance consistency.

### Option C: Keep ADR-070 placement grammar and add ADR-071 boundary clarification (Accepted)
- **Pros:** Preserves the useful standard, clarifies authority, and prevents optional Socios automation from being confused with base SourceOS.
- **Cons:** Requires follow-on contract and implementation alignment across repos.

---

## Consequences

### Positive
- SourceOS remains independently operable.
- Socios remains opt-in and policy-gated.
- Immutable-node standards remain reusable across SourceOS, Agent Machine, AgentPlane, and Prophet Platform.
- Implementation ownership becomes clearer.

### Negative
- Existing ADR-070 docs may still contain Socios-heavy wording until amended or superseded in follow-on docs.
- Requires a SourceOS contract tranche and Agent Machine implementation tranche.

### Neutral
- This ADR does not change any runtime behavior by itself.

---

## Required Follow-on Work

1. Add `ImmutableNodeProfile`, `HostCapabilityPlacement`, and `NodeStateSchema` contracts to `SourceOS-Linux/sourceos-spec`.
2. Add an Agent Machine renderer/validator that consumes those contracts and emits systemd, Quadlet, tmpfiles, and receipt artifacts.
3. Add `sourceosctl immutable-node plan|validate|inspect` entrypoints in `SourceOS-Linux/sourceos-devtools`.
4. Add AgentPlane evidence consumption for immutable-node activation/runtime receipts.
5. Register the cross-repo topology edges in `SocioProphet/sociosphere`.

---

## Related ADRs

- [ADR-070-immutable-node-host-capability-model.md](ADR-070-immutable-node-host-capability-model.md)
- [ADR-040-tekton-argocd-gitops.md](ADR-040-tekton-argocd-gitops.md)
- [ADR-050-devsecops-rbac-audit.md](ADR-050-devsecops-rbac-audit.md)
- [ADR-060-otel-observability.md](ADR-060-otel-observability.md)
