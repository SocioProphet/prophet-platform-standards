# ADR-071: Capability Lease and Approval Model

**Status:** Proposed  
**Date:** 2026-05-07  
**Deciders:** Platform Engineering, Security, Delivery Governance  
**Tags:** authorization, zero-trust, approvals, capabilities, leases, audit

---

## Context and Problem Statement

The platform requires agent and service capabilities to be:
- explicit,
- reviewable,
- time-bounded,
- scoped to the target system and task,
- and auditable.

Standing or implicit permissions are a poor fit for a governed control plane. They make it harder to:
- distinguish collaboration from authorization,
- prove why an action was allowed,
- revoke or expire access safely,
- and map approval decisions to concrete executed actions.

The platform therefore needs a short-lived capability model rather than a static entitlement model.

---

## Decision

**Adopt short-lived capability leases as the normative authorization model for privileged control-plane actions.**

A capability lease is the authoritative, time-bounded grant that permits a principal to invoke a scoped capability against a specific target for a bounded task or case.

The lease model applies to:
- agent capability invocation,
- broker-mediated tool access,
- privileged workflow execution,
- and any control-plane action that exceeds ambient read-only collaboration.

---

## Requirements

### Lease properties

1. Capability grants **MUST** be represented as explicit leases.
2. A lease **MUST** be short-lived.
3. A lease **MUST** be scoped to:
   - subject,
   - acting principal or human sponsor where applicable,
   - target audience or resource,
   - allowed capability scope,
   - task or case correlation,
   - and expiry window.
4. A lease **MUST** be auditable and replayable at the decision level.

### Approval posture

5. High-risk or mutating capabilities **MUST** require explicit approval according to policy.
6. Low-risk read-only capabilities **MAY** be auto-approved by policy when risk posture permits.
7. Approval state **MUST** be distinguishable from lease issuance.
8. A lease **MUST NOT** imply that approval evidence is optional.

### Authority boundaries

9. Matrix room membership **MUST NOT** be treated as a capability grant.
10. Capability leases **MUST** be issued by a broker or equivalent authority surface, not by collaboration tools directly.
11. Capability leases **MUST** be revocable or naturally expiring.
12. Long-lived standing privileges **SHOULD** be avoided for routine control-plane actions.

### Audit and provenance

13. Lease issuance, denial, revocation, and expiry **MUST** produce auditable records.
14. Approval records **MUST** be linkable to the lease and to the invoked action or task.
15. Lease-consuming systems **MUST** validate lease scope and expiry before honoring a request.

---

## Lease model (minimum)

A conforming lease object **MUST** include fields equivalent to the following classes of information:
- issuer
- subject
- actor / sponsor when applicable
- audience / target
- scope
- purpose or intended use
- task and/or case correlation
- approval reference when required
- issued-at / not-before / expiry
- unique lease identifier
- policy or decision reference

Exact schema details are defined in the contract layer, not this ADR.

---

## Consequences

### Positive
- Clear separation between collaboration context and actual authority.
- Stronger auditability and better bounded execution.
- Easier revocation and reduced standing privilege.
- Better fit for policy-gated agent and broker execution.

### Negative
- More moving parts than static credentials.
- Additional broker, policy, and approval infrastructure required.
- More correlation logic needed across rooms, tasks, cases, and runtime actions.

### Neutral
- Collaboration surfaces remain useful, but they are no longer mistaken for the authorization system.

---

## Repository and implementation split

This ADR is normative only.

Implementation is split as follows:
- control-plane standards here in `prophet-platform-standards`
- lease/event schemas in `socioprophet-standards-storage`
- broker / registry / grant / enforcement implementation in `mcp-a2a-zero-trust`
- runtime wiring in `prophet-platform`

---

## Follow-on ADR

- ADR-072 — Public Moderation and Room Publication
