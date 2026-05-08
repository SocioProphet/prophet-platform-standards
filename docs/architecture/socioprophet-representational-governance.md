# SocioProphet Representational Governance Architecture

Status: draft v0.1  
Scope: SocioProphet, Fog Stack, Prophet Platform, SourceOS, SociOS, Sherlock, Holmes, GAIA, Ontogenesis, Agentplane, Lattice, New Hope, Guardrail Fabric, and Sociosphere.

## 1. Purpose

SocioProphet Representational Governance Architecture (SRGA) is the estate-wide architectural style for governed, agentic, semantic, local-first, multi-organization infrastructure.

SRGA is not a product name, service inventory, repository taxonomy, API convention, or diagramming style. It is a coordinated set of runtime constraints that restricts how architectural elements identify resources, exchange representations, mediate trust, preserve provenance, and evolve without losing visibility, policy enforceability, or evidence integrity.

The core doctrine is:

> Every meaningful system action is a governed transfer or transformation of a typed representation of a durable conceptual resource, mediated by visible connectors, bounded by policy, and preserved as evidence.

## 2. Fielding-derived basis

Roy Fielding's architectural work is treated here as method, not just as REST history. The applicable method is:

1. Identify the forces of the target system.
2. Derive constraints that induce the required properties.
3. Name the coordinated constraint set as an architectural style.
4. Use the style as an acid test for extensions and implementations.
5. Maintain a mismatch ledger for deployed behavior that violates the style.
6. Validate through standards, reference implementations, conformance tests, and operational deployment.

SRGA extends this method from Internet-scale distributed hypermedia to Internet-scale governed agentic infrastructure.

## 3. System forces

SRGA exists because the estate must operate across forces that are not solved by ordinary service decomposition.

Primary forces:

- Multi-organization deployment across SocioProphet, SourceOS-Linux, SociOS-Linux, user machines, cloud runtimes, and external services.
- Fragmented deployment where old and new implementations coexist.
- Agentic execution where mobile code can act with delegated authority.
- Semantic resource identity across slash-topics, search, world models, policy, builds, notebooks, data products, and runtime artifacts.
- Local-first operation where devices and workspaces must continue during partial network failure.
- Evidence preservation where outputs must be traceable to source resources, policies, models, prompts, tools, and runtime contexts.
- Trust-boundary crossing through New Hope membranes, MCP gateways, TriTRPC connectors, cloud shells, browsers, map surfaces, OS sync, and model routers.
- Adversarial pressure where malformed data, opaque tool calls, hidden state, and ungoverned agents must be expected.
- High evolvability where repositories and implementations can change without invalidating resource semantics.

## 4. Required architectural properties

SRGA inherits several properties from network-based architectural design and adds properties required for governed agentic systems.

Required properties:

- Scalability: components must tolerate many actors, requests, resources, and intermediaries without requiring global knowledge.
- Evolvability: implementations can change while resource semantics and representation contracts remain stable.
- Visibility: intermediaries can inspect enough message semantics to route, enforce, cache, audit, and explain.
- Policy enforceability: connectors can evaluate authority, capability, risk, context, and permitted transitions.
- Provenance strength: outputs preserve source references, derivation paths, actor identity, runtime context, and evidence receipts.
- Revocation latency: cached or delegated authority can be invalidated predictably.
- Offline survivability: local-first actors can continue within bounded policy and later reconcile state.
- Evidence cacheability: evidence-bearing results can be reused when their freshness, authority, and invalidation conditions are explicit.
- Semantic interoperability: different implementations can exchange typed representations without sharing storage internals.
- Agent containment: mobile code and autonomous execution remain bounded, attestable, replayable where appropriate, and auditable.
- Audit completeness: meaningful actions leave sufficient evidence for later reconstruction and adversarial review.
- Trust-boundary transparency: crossings between organizations, devices, runtimes, and membranes are explicit.

## 5. Architectural elements

### 5.1 Resource

A resource is a durable conceptual mapping, not a file, database row, service endpoint, object, repository, container, model, tile, or implementation.

Examples:

- SlashTopic
- GAIAFeature
- WorldObservation
- EvidenceBundle
- SherlockQueryRun
- AgentRun
- PolicyDecision
- CapabilityGrant
- NotebookSession
- RuntimeBundle
- ModelCandidate
- EvaluationBundle
- BootReleaseSet
- SourceOSStateRecord
- PlatformAssetRecord
- PublicationArtifact

The resource identifier must remain stable across representation changes, implementation changes, storage migration, and deployment fragmentation.

### 5.2 Representation

A representation is transferable system state for a resource. It may express the current state, intended state, derived state, evidence state, error state, review state, or transition state of the resource.

A representation must carry or reference:

- data
- representation metadata
- resource metadata
- control data
- schema reference
- integrity digest
- provenance
- evidence references
- policy context
- validity window
- cache and revocation semantics

### 5.3 Connector

A connector is an architectural control point, not incidental plumbing.

Examples:

- TriTRPC connector
- MCP gateway
- HTTP API gateway
- Sherlock retrieval gateway
- GAIA feature/tile gateway
- Guardrail Fabric policy gateway
- SourceOS syncd transport
- model router
- New Hope membrane
- CloudFog shell boundary

A valid SRGA connector mediates communication, coordination, policy enforcement, evidence capture, cache/revalidation, replay classification, and trust-boundary crossing.

### 5.4 Component

A component transforms, stores, serves, evaluates, renders, indexes, executes, or validates representations. Components must not rely on hidden assumptions unavailable to connectors when governance depends on those assumptions.

### 5.5 Event

An event announces a change, observation, or requested transition. It is not authoritative state unless the event itself is the resource being governed.

Default rule: events should point to retrievable representations.

### 5.6 Receipt

A receipt is a durable representation that records that an action, decision, transition, execution, transformation, cache use, or membrane crossing occurred.

Receipts are first-class evidence resources.

## 6. Derived constraints

### C1. Stable conceptual resource identity

Every meaningful object must have a durable resource identity independent of its current storage, file path, URL implementation, service endpoint, or repository location.

Induced properties: evolvability, semantic interoperability, audit stability.

### C2. Representation-mediated manipulation

Components manipulate resources through typed representations, not hidden implementation objects.

Induced properties: portability, visibility, interoperability, evolvability.

### C3. Self-descriptive governance envelope

Every cross-boundary action must carry an SRGA envelope sufficient for an intermediary to understand the action without hidden session context.

Minimum semantic dimensions:

- method or action
- resource identity
- representation type and schema
- actor identity
- authority or capability
- policy context
- provenance and evidence references
- cacheability and invalidation
- request and trace correlation
- validity window

Induced properties: visibility, policy enforceability, audit completeness, replayability.

### C4. Visible connectors

Connectors that route, enforce, cache, transform, or audit must be able to inspect the semantics required for that responsibility.

Opaque transport tunneling is permitted only when the boundary is explicitly classified as a tunnel and governance is enforced outside the tunnel.

Induced properties: trust-boundary transparency, policy enforceability, security, operational diagnosis.

### C5. Explicit state locality

Application, workflow, agent, policy, and user state must be represented explicitly in client state, workflow resources, local-first stores, state records, or receipts. Hidden server-side session state is an architectural mismatch unless it is explicitly modeled as a governed resource.

Induced properties: reliability, replayability, auditability, offline survivability.

### C6. Governed cacheability

Representations may be cached only when freshness, authority, policy dependency, privacy scope, source version, and revocation behavior are known.

Induced properties: performance, evidence reuse, resilience, cost control.

### C7. Layered policy intermediaries

Policy gateways, guardrail systems, New Hope membranes, model routers, search gateways, sync controllers, and runtime gateways are part of the architecture, not optional middleware.

Induced properties: security, scalability, encapsulation of legacy systems, adversarial containment.

### C8. Governed mobile code

Agents, notebooks, kernels, model tools, runtime bundles, and code-on-demand behavior must execute only within explicit trust realms.

Required execution metadata:

- signed runtime or agent manifest
- declared input resources
- declared output representations
- capability-scoped actor identity
- sandbox profile
- resource quotas
- network policy
- evidence output contract
- revocation behavior
- replay classification

Induced properties: agent containment, audit completeness, safety, reliability.

### C9. Event-as-notification default

Events notify consumers that something changed or should be inspected. Authoritative state should be retrieved as a typed representation unless the event resource itself is the authoritative object.

Induced properties: scalability, repairability, replayability, reduced event-storm risk.

### C10. Parallel architecture for incompatible forces

If a required behavior conflicts with SRGA constraints, it must be implemented as a parallel architectural style with an explicit bridge back to SRGA through governed representations.

Likely parallel styles:

- high-volume telemetry streams
- bulk data pipelines
- real-time OS coordination
- notebook/kernel execution
- model training and tuning
- spatial tile serving
- low-latency interactive sessions

Induced properties: architectural integrity, evolvability, mismatch containment.

## 7. Substrate planes

SRGA is organized as a substrate map with planes that own distinct architectural responsibilities.

| Plane | Responsibility | Primary repos |
| --- | --- | --- |
| Constitutional standards | Style, constraints, mismatch ledger, conformance vocabulary | `prophet-platform-standards` |
| Resource/representation | Resource classes, schemas, semantic contracts | `ontogenesis`, `prophet-platform`, `sherlock-search`, `gaia-world-model` |
| Connector/gateway | Visible mediation, envelopes, routing, cache, enforcement | `prophet-platform`, `guardrail-fabric`, `model-router`, `sourceos-syncd` |
| Trust/policy/evidence | Capability, policy, provenance, receipts, audit | `guardrail-fabric`, `policy-fabric`, `model-governance-ledger`, `ProCybernetica` |
| State/sync/coherence | Local-first state, events, repair, reconciliation | `SourceOS-Linux/sourceos-syncd`, `SourceOS-Linux/sourceos-spec`, `sociosphere` |
| Runtime/execution | Governed mobile code, agents, kernels, bundles | `agentplane`, `agent-registry`, `lattice-forge`, `new-hope` |
| Knowledge/discovery | Search, evidence retrieval, slash-topic addressing, interpretation | `sherlock-search`, `Holmes`, `slash-topics`, `memory-mesh`, `sociosphere` |
| World model | Spatial-temporal resources, observations, uncertainty, map evidence | `gaia-world-model`, `socioprophet`, `sherlock-search` |
| Operator surfaces | CLI, shell, terminal, browser, map, evidence panels | `prophet-cli`, `cloudshell-fog`, `TurtleTerm`, `BearBrowser`, `socioprophet` |
| Delivery/conformance | Dashboards, CI gates, mismatch counts, repo readiness | `delivery-excellence`, `delivery-excellence-automation`, `sociosphere` |

## 8. Conformance questions

A repo, feature, connector, runtime, or artifact is not SRGA-integrated until it can answer:

1. What is the resource?
2. What is the representation?
3. Which connector mediates it?
4. What policy permits or denies it?
5. What evidence is produced?
6. How is provenance preserved?
7. Can it be cached, replayed, revoked, or repaired?
8. Which trust boundary is crossed?
9. What mismatch class would failure fall under?
10. What test proves conformance?

## 9. Minimum implementation path

The first reference loop should prove:

1. A slash-topic identifies a durable conceptual resource.
2. Ontogenesis supplies or validates the representation schema.
3. A request enters through a visible connector with an SRGA envelope.
4. Guardrail/policy evaluates actor, capability, and context.
5. Sherlock returns an evidence-bearing representation.
6. Sociosphere records resource, lineage, health, and conformance status.
7. A UI or CLI renders resource identity, evidence, provenance, and policy state.

## 10. Extension rule

New protocols, gateways, agents, schemas, repos, model surfaces, notebooks, events, or UI features must declare whether they are:

- SRGA-conformant
- SRGA-adjacent with a bridge
- intentionally parallel architecture
- known mismatch requiring containment

No extension should be accepted as platform architecture solely because it is useful code.

## 11. Review standard

Reviewers should reject or block architectural claims that lack:

- resource identity
- representation contract
- connector semantics
- policy/evidence behavior
- mismatch analysis
- validation command or conformance test

SRGA should become the estate's acid test for architectural evolution.
