# Capability Fabric Adoption Note

This repository is a **consumer** of the canonical Capability Fabric standards.

## Canonical source of truth

The protocol-independent semantic core for the Capability Fabric lives in:

- `SocioProphet/socioprophet-standards-knowledge`
  - `docs/standards/040-capability-fabric-core.md`
  - `docs/standards/041-capability-fabric-realization-profiles.md`
  - `schemas/jsonschema/capability-fabric/`

## Scope in this repository

This repository MAY define:
- platform adoption profiles
- deployment patterns
- planner/runtime/operator guidance
- integration examples for Prophet Platform

This repository MUST NOT redefine:
- `FunctionIdentity`
- `CapabilitySignature`
- `EffectContext`
- `InteractionMode`
- `DeliverySemantics`
- `ReceiptSemantics`
- `ExecutionControllabilityProfile`
- `ProofStrengthProfile`
- `RealizationMetadata`

These MUST be imported or referenced from the canonical standards source.

## Intended follow-on work

Future platform-facing documents in this repository SHOULD explain:
- how Prophet Platform consumes the Capability Fabric core
- how realization profiles lower into platform planners, operators, and execution substrates
- how proof/telemetry hooks are surfaced operationally without redefining their semantics
