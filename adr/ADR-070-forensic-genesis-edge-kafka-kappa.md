# ADR-070: Forensic Genesis Edge Ingress on Kafka/Kappa

## Status
Proposed

## Context
The platform needs a Silverblue-first, local-evidence-preserving edge ingress lane for host and transport observations such as mounts, SNMP observations, verification completions, and evidence sealing events.

The runtime monorepo (`prophet-platform`) is explicitly a thin runtime/deployment hub. Normative standards, schemas, and ADRs belong in a standards repository. This ADR therefore anchors the normative split for the edge lane here.

## Decision
We standardize a **Forensic Genesis edge ingress lane** with the following properties:

1. **Local-first evidence capture** remains authoritative at the edge. Host collectors spool JSON/JSON-LD evidence to local storage before any publication step.
2. **Kafka/Kappa** is the durable derivation and replay plane. Edge observations publish into append-only Kafka fact topics plus compacted latest-state views where appropriate.
3. **TriTRPC** remains the synchronous control/query plane. It is not the system of record for edge derivation history.
4. Edge events remain in the **structural-fact lane**. Stronger semantic claims are deferred to downstream processors.
5. Heavy artifacts such as PCAPs publish by **manifest + digest**, not inline payload, unless explicitly justified by a bounded profile.
6. Edge schema evolution follows explicit registry compatibility rules; compatibility policy is part of the standard, not an implementation afterthought.

## Initial topic family
- `edge.forensic.snmp.observed.v1`
- `edge.forensic.mounts.observed.v1`
- `edge.forensic.verify.completed.v1`
- `edge.forensic.seal.completed.v1`

## Initial keying rule
Topic keys MUST be deterministic and scoped to the natural join boundary for the event type.

## Consequences
### Positive
- preserves replayable evidence history
- keeps local forensic discipline intact
- allows runtime and standards repos to evolve without collapsing into one another
- provides a clean ingress point into deeper control-flow-recovery / semantic lanes

### Negative
- requires an outbox publisher and schema-registry discipline
- adds operational complexity versus local-file-only capture

## Follow-on artifacts
See `docs/FORENSIC_GENESIS_EDGE.md` and `schemas/forensic-genesis/` for the initial standard surface.
