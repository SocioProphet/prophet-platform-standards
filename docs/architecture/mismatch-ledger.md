# SRGA Mismatch Ledger

Status: draft v0.1  
Scope: architectural mismatches against SocioProphet Representational Governance Architecture (SRGA).

## Purpose

A mismatch is deployed or proposed behavior that violates SRGA constraints or weakens a required architectural property. Mismatches are not automatically defects; some may be temporarily necessary for compatibility, performance, or experimental work. But every known mismatch must be named, classified, contained, and either corrected or bridged as a parallel architecture.

## Severity

- Critical: violates trust, policy enforceability, revocation, or safety boundaries.
- High: blocks evidence, audit, provenance, or semantic interoperability.
- Medium: harms evolvability, cacheability, repairability, or cross-repo integration.
- Low: documentation, naming, or conformance hygiene issue with limited runtime effect.

## Initial mismatch classes

### MISMATCH-001: Repo-as-architecture

A repository inventory, service list, or code-layout diagram is treated as the architecture.

Why it matters: SRGA architecture is constrained runtime behavior across components, connectors, and data. Repos are implementation containers.

Default severity: medium.

Required containment:

- Identify runtime resources, representations, connectors, and trust boundaries.
- Link repo scope to a substrate plane and conformance questions.

### MISMATCH-002: Resource-as-file

A durable conceptual resource is confused with its current file, database row, blob, tile, endpoint, or implementation object.

Why it matters: breaks evolvability and causes unstable identifiers.

Default severity: high.

Required containment:

- Assign a stable resource identifier.
- Treat files, rows, objects, tiles, or endpoint responses as representations.

### MISMATCH-003: Opaque agent execution

An agent call lacks declared inputs, declared outputs, policy context, capability scope, sandbox profile, runtime manifest, or evidence receipt.

Why it matters: agents are governed mobile code and can cross trust boundaries with delegated authority.

Default severity: critical.

Required containment:

- Require an AgentRun resource.
- Attach SRGA envelope, capability, sandbox, output contract, and receipt.

### MISMATCH-004: Hidden session state

Workflow behavior depends on implicit server-side memory, sticky model state, unversioned prompt context, hidden user/session data, or unmodeled stateful middleware.

Why it matters: breaks replay, audit, recovery, cacheability, and user-controlled state.

Default severity: high.

Required containment:

- Model the state as a governed resource or move it into explicit client/workflow/local-first state.

### MISMATCH-005: Event-as-truth

An event payload becomes authoritative state instead of pointing to a retrievable representation.

Why it matters: causes event storms, irreparable divergence, and weak provenance.

Default severity: high.

Required containment:

- Treat events as notifications by default.
- Include resource and representation references.

### MISMATCH-006: Transport tunneling

HTTP, gRPC, MCP, TriTRPC, WebSocket, or another transport is used as an opaque pipe that prevents policy or evidence intermediaries from understanding required semantics.

Why it matters: disables visible connectors and policy enforcement.

Default severity: critical when crossing trust boundaries; medium inside a single trusted process.

Required containment:

- Classify the connector as a tunnel.
- Enforce governance before or after the tunnel.
- Prefer SRGA self-descriptive envelope at the boundary.

### MISMATCH-007: Policy without evidence

A decision says allowed, denied, redacted, approved, or deferred but lacks policy references, input facts, actor identity, capability, reason, or replay data.

Why it matters: decisions become unverifiable and non-contestable.

Default severity: critical.

Required containment:

- Emit a PolicyDecision resource and receipt.
- Include input facts, policy refs, actor, capability, and obligations.

### MISMATCH-008: Cache without revocation

A cached representation lacks TTL, authority, source version, policy dependency, privacy scope, or invalidation rule.

Why it matters: stale or unauthorized state can persist after revocation or source change.

Default severity: high.

Required containment:

- Add governed cache metadata.
- Require revalidation triggers.

### MISMATCH-009: Model output without lineage

LLM or model output lacks prompt/resource refs, model identity, runtime, evaluation state, risk class, evidence refs, or downstream-use boundary.

Why it matters: blocks audit, evaluation, and safe reuse.

Default severity: high.

Required containment:

- Emit a ModelOutput or EvaluationBundle representation with provenance.

### MISMATCH-010: Schema bypass

Data enters Sherlock, GAIA, Agentplane, syncd, Sociosphere, or platform APIs without Ontogenesis/SHACL-compatible validation or an explicit experimental bypass marker.

Why it matters: weakens semantic interoperability and policy enforcement.

Default severity: high.

Required containment:

- Validate against schema/shape or mark as experimental with quarantine scope.

### MISMATCH-011: Boundary confusion

A New Hope membrane, policy boundary, cloud boundary, device boundary, tenant boundary, or runtime boundary is mentioned but no explicit crossing rule, transformation rule, or receipt exists.

Why it matters: trust-boundary semantics become rhetorical rather than enforceable.

Default severity: critical where secrets, agents, models, or user data cross boundaries; otherwise high.

Required containment:

- Add membrane metadata with crossing rule, transformation rule, and receipt.

### MISMATCH-012: UI hides trust state

A user-facing surface shows output without resource identity, evidence, provenance, confidence/uncertainty, cache state, or policy state.

Why it matters: operators cannot distinguish grounded output from ungrounded output.

Default severity: medium; high for policy, security, world-model, medical, legal, financial, or operational surfaces.

Required containment:

- Add evidence/provenance affordances and visible trust state.

### MISMATCH-013: Parallel architecture without bridge

A subsystem uses a specialized style for performance or domain reasons but lacks a governed bridge back to SRGA.

Why it matters: useful systems become isolated islands and later force architectural corruption.

Default severity: medium.

Required containment:

- Declare the parallel style.
- Define resource/representation bridge and conformance boundary.

### MISMATCH-014: Unversioned representation

A representation is exchanged without schema/version semantics.

Why it matters: fragmented deployment becomes unsafe.

Default severity: high.

Required containment:

- Add schema_ref and representation version.

### MISMATCH-015: Receipt gap

An action, transition, policy decision, runtime execution, cache reuse, or membrane crossing occurs without a durable receipt.

Why it matters: audit and repair cannot reconstruct the action.

Default severity: high.

Required containment:

- Emit receipt resource or attach receipt_ref to the envelope.

## Review checklist

Every architecture-affecting PR should answer:

1. Which resource class is introduced or modified?
2. Which representation contract is introduced or modified?
3. Which connector mediates the action?
4. Which policy/evidence behavior is required?
5. Which mismatch classes are avoided, accepted, or newly created?
6. What conformance test or validation command proves this?

## Disposition states

- proposed
- accepted-temporary
- accepted-permanent-with-bridge
- contained
- remediated
- rejected
- superseded

## Ledger maintenance

Mismatch classes may be added without changing SRGA's core constraints. Existing classes should not be deleted unless superseded; instead, mark them superseded and point to the replacement class.
