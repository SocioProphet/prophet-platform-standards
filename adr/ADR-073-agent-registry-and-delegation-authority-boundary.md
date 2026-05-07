# ADR-073: Agent Registry and Delegation Authority Boundary

**Status:** Proposed  
**Date:** 2026-05-07  
**Deciders:** Platform Engineering, Security, Delivery Governance  
**Tags:** agent-registry, grants, delegation, authority, policy-fabric, agentplane

---

## Context and Problem Statement

The control-plane standards must align with the current upstream authority model.

The estate now includes a dedicated `agent-registry` repository for governed agent specs, identities, sessions, memories, tool grants, revocation, and runtime authority. The estate also includes HolographMe authority/delegation work and AgentPlane event-capability admission gates.

If the control-plane model assigns all registry, grant, and authority responsibilities to `mcp-a2a-zero-trust`, it collapses distinct ownership domains and makes future governance ambiguous.

---

## Decision

**Split identity, grants, delegation, admission, and enforcement into distinct ownership lanes.**

### Agent Registry

`agent-registry` is the canonical home for:
- agent identity records,
- agent specs,
- sessions,
- tool grants,
- grant revocation,
- runtime authority records,
- and agent-facing grant fixtures.

### HolographMe

`HolographMe` is the canonical home for human delegation, consent, and acting-for-human authority semantics.

### AgentPlane

`agentplane` is the canonical execution admission consumer. Events may propose work, but execution admission must validate policy outcomes, idempotency posture, evidence references, dead-letter posture, and high-risk approval constraints before execution proceeds.

### MCP/A2A Zero Trust

`mcp-a2a-zero-trust` is the canonical home for broker enforcement, zero-trust checks, attestation hooks, policy enforcement, and grant consumption at the boundary.

It consumes grant and authority records; it does not own all grant semantics.

---

## Requirements

1. Capability leases **MUST** distinguish broker authority from grant authority.
2. Grant records **SHOULD** be sourced from `agent-registry` where agent/tool authority is involved.
3. Human delegation and consent **SHOULD** reference `HolographMe` authority records where acting-for-human behavior is involved.
4. Execution admission **SHOULD** route through `agentplane` where an event proposes executable work.
5. Broker enforcement **MUST** verify the relevant registry, grant, delegation, policy, and admission references before allowing privileged capability use.
6. Runtime services **MUST NOT** treat Matrix room membership as a substitute for agent grant, human delegation, or execution admission.

---

## Consequences

### Positive
- Prevents `mcp-a2a-zero-trust` from becoming an overloaded god-repo.
- Gives agent grants and revocation a dedicated registry authority.
- Separates human delegation from technical tool grants.
- Adds AgentPlane as the execution stop gate for event-driven work.

### Negative
- Requires more cross-repo references and evidence correlation.
- Requires careful schema design for grant, delegation, lease, and admission references.

---

## Repository placement

- `agent-registry` — identity, grants, sessions, revocation, runtime authority
- `HolographMe` — delegation, consent, acting-for-human authority
- `agentplane` — execution admission and run/replay evidence
- `mcp-a2a-zero-trust` — broker enforcement, attestation, policy, boundary checks
- `policy-fabric` — policy approvals and compiled policy evidence
- `prophet-platform` — deployable runtime topology
- `socioprophet-standards-storage` — portable schemas and event contracts
- `sociosphere` — workspace placement and ownership registry

---

## Related ADRs

- ADR-070 — Matrix Dual-Estate Control Plane
- ADR-071 — Capability Lease and Approval Model
- ADR-072 — Public Moderation and Room Publication
