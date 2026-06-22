# ADR-070: Matrix Dual-Estate Control Plane

**Status:** Proposed  
**Date:** 2026-05-07  
**Deciders:** Platform Engineering, Security, Delivery Governance  
**Tags:** matrix, control-plane, federation, moderation, collaboration, zero-trust

---

## Context and Problem Statement

The SocioProphet platform needs a chat-native control surface that can serve both:

1. **public / federated collaboration** for intake, community interaction, lightweight support entry, and external-facing rendezvous; and
2. **private / governed collaboration** for internal operations, regulated case work, privileged approvals, and high-trust agent/human coordination.

A single undifferentiated Matrix estate creates avoidable risk:
- public-room discoverability can leak sensitive context,
- moderation controls for public federation become coupled to internal operator spaces,
- room publishing policy and regulated collaboration policy become entangled,
- and operational boundaries between support intake, case work, and privileged control actions become ambiguous.

The platform therefore requires an explicit architectural split.

---

## Decision

**Adopt a dual-estate Matrix control-plane model.**

### Estate A — Public Matrix Edge

The public Matrix estate is the external collaboration edge.

It **MUST** be used for:
- public rooms,
- federated intake rooms,
- public support/community entry points,
- low-sensitivity coordination,
- and externally reachable Matrix presence.

It **MUST NOT** be used as the authoritative location for:
- regulated case content,
- privileged operational decisions,
- durable capability grants,
- or sensitive human/agent task state.

### Estate B — Private Matrix Core

The private Matrix estate is the governed collaboration plane.

It **MUST** be used for:
- internal operator rooms,
- regulated case collaboration,
- privileged approval rooms,
- high-trust human/agent coordination,
- and control-plane work that requires stronger isolation or policy constraints.

It **MUST NOT** publish public rooms casually and **SHOULD** default to non-public visibility and restricted membership.

---

## Requirements

### Room and estate boundaries

1. Public-edge rooms **MUST** be treated as low-sensitivity collaboration surfaces.
2. Private-core rooms **MUST** be treated as the default location for sensitive or governed collaboration.
3. Sensitive work **MUST** pivot from public intake into the private estate rather than remaining in public or semi-public rooms.
4. The control plane **MUST NOT** treat room membership as equivalent to durable authorization.

### Ownership and creation

5. Controlled rooms **MUST** be created through a long-lived service-owned room factory rather than ad hoc creator accounts where governed ownership matters.
6. Public-room publication **MUST** be policy-governed and reviewable.

### Federation and moderation

7. The public estate **MUST** support moderation and abuse controls before broad publication.
8. The public estate **SHOULD** use proactive moderation/policy-server style controls where available.
9. The private estate **SHOULD** minimize federation and external discoverability by default.

### Data and authority boundaries

10. Matrix rooms **MUST NOT** be the canonical ledger for capability grants.
11. Durable capability, approval, and broker state **MUST** live outside Matrix in the control-plane services and ledgers.
12. Matrix remains a collaboration and coordination surface, not the canonical authorization store.

---

## Consequences

### Positive
- Stronger separation between public collaboration and governed collaboration.
- Clearer moderation and publishing posture for public federation.
- Cleaner operational path for support intake → governed case-room pivot.
- Reduced chance of conflating collaboration context with durable authorization.

### Negative
- More deployment and operational complexity than a single-estate model.
- More documentation and operator training required.
- More explicit federation and room-publication governance needed.

### Neutral
- The Matrix control plane remains a collaboration surface, while runtime authority remains in broker, registry, policy, and ledger components.

---

## Repository and implementation split

This ADR is normative only.

Implementation is split as follows:
- placement and ownership references in `sociosphere`
- runtime/deployment in `prophet-platform`
- contracts and schemas in `socioprophet-standards-storage`
- zero-trust enforcement and broker/registry logic in `mcp-a2a-zero-trust`

---

## Follow-on ADRs

This ADR intentionally does not define the full capability-grant model or moderation publication workflow. Those are defined in follow-on ADRs.

- ADR-071 — Capability Lease and Approval Model
- ADR-072 — Public Moderation and Room Publication
