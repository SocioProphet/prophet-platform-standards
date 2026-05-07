# ADR-072: Public Moderation and Room Publication

**Status:** Proposed  
**Date:** 2026-05-07  
**Deciders:** Platform Engineering, Security, Delivery Governance  
**Tags:** moderation, federation, publication, matrix, abuse-prevention, governance

---

## Context and Problem Statement

The platform intends to use Matrix as a public-facing collaboration and intake surface.

Public room publication and public federation are powerful, but they create risk if they are treated as default behavior rather than governed behavior. Risks include:
- abuse and spam,
- accidental publication of the wrong rooms,
- poor separation between public intake and sensitive collaboration,
- and inconsistent moderation expectations across estates.

A formal publication and moderation posture is therefore required.

---

## Decision

**Adopt a governed publication model for public Matrix rooms, with moderation as a prerequisite rather than an afterthought.**

Public visibility and publication are not the default. They are governed actions.

---

## Requirements

### Publication

1. Public room publication **MUST** be explicitly approved.
2. Rooms intended for publication **MUST** be classified as low-sensitivity collaboration spaces.
3. Regulated, privileged, or governed operational rooms **MUST NOT** be published as public rooms.
4. Public-room publication state **MUST** be reviewable and reversible.

### Moderation

5. The public Matrix estate **MUST** have moderation controls before broad publication.
6. Moderation **MUST** include a documented process for abuse review, escalation, and room-level response.
7. Moderation decisions **SHOULD** produce reviewable evidence when they affect publication or access posture.
8. Public federation **SHOULD** use proactive moderation or policy-server style controls where available.

### Room lifecycle

9. Public intake rooms **SHOULD** be treated as intake surfaces, not durable case ledgers.
10. Sensitive or governed work **MUST** pivot into private or restricted rooms rather than continue in public published rooms.
11. Publication **MUST NOT** imply authorization for privileged work.

### Governance

12. Publication policy **MUST** be owned and versioned as part of the platform standards.
13. Public moderation posture **MUST** be documented in operator guidance.
14. Deviations or exceptions **SHOULD** be rare and reviewable.

---

## Consequences

### Positive
- Safer public collaboration posture.
- Reduced accidental overexposure of governed rooms.
- Clearer operator expectations around room publication and moderation.
- Better separation between intake/community surfaces and privileged collaboration.

### Negative
- More review and operational overhead before public publication.
- More process than a casual default-public model.

### Neutral
- Public rooms remain supported, but only as intentionally governed collaboration surfaces.

---

## Repository and implementation split

This ADR is normative only.

Implementation is split as follows:
- standards here in `prophet-platform-standards`
- platform runtime wiring in `prophet-platform`
- event and provenance contracts in `socioprophet-standards-storage`
- policy and grant/broker enforcement in `mcp-a2a-zero-trust`

---

## Related ADRs

- ADR-070 — Matrix Dual-Estate Control Plane
- ADR-071 — Capability Lease and Approval Model
