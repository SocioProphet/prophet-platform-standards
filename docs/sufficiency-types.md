# Sufficiency Types v0.1

Sufficiency types describe what a boundary surface is adequate for. They prevent a typed interface from being judged by the wrong standard.

## Why this exists

A surface can be useful without exposing total internal state. Model cards, system cards, proof artifacts, boot attestations, audit logs, map tiles, and agent traces are all typed interfaces. Each may preserve the distinctions required for a particular claim while remaining incomplete with respect to latent state.

## Types

### microstate_sufficient
The surface supports exact reconstruction of the declared latent state within scope.

Use sparingly. Most governance, audit, and documentation surfaces are not microstate-sufficient.

### reconstruction_sufficient
The surface supports reconstruction of a declared sector, projection, or abstraction with bounded error.

Required fields:
- declared sector;
- reconstruction map or procedure;
- error bound or replay condition.

### semantic_sufficient
The surface preserves the semantic equivalence classes needed for the declared meaning or interpretation.

Example: a documentation surface that preserves the governance classification even though it does not expose full internal weights, logs, or hidden states.

### task_sufficient
The surface supports a specific operational task.

Example: a repository header may be sufficient to identify and fetch a model, but not sufficient for governance approval.

### governance_sufficient
The surface supports policy review, deployment gating, escalation, withdrawal, or compliance interpretation.

Required fields typically include intended use, limitations, evaluation evidence, risk posture, provenance, approval state, and escalation channel.

### audit_sufficient
The surface supports independent replay, assessor review, or dispute resolution.

Required fields typically include hashes, signatures, input manifests, policy versions, checker versions, and replay instructions.

### not_sufficient
The surface is explicitly insufficient for the stated claim. This is a valid and useful label; it prevents accidental overclaiming.

## Rule of separation

Semantic sufficiency does not imply microstate sufficiency.

Task sufficiency does not imply governance sufficiency.

A proof artifact about an observation window does not imply exact proof about unobserved reality. It supports the claim only under its declared assumptions.

## Examples

| Surface | Likely sufficiency | Not sufficient for |
| --- | --- | --- |
| Model repository header | task_sufficient | governance_sufficient, microstate_sufficient |
| Full model card | governance_sufficient, sometimes semantic_sufficient | microstate_sufficient |
| Trust-First proof artifact | audit_sufficient for a claim under assumptions | claims outside coverage |
| Boot attestation | reconstruction_sufficient for boot trust state | full host runtime state |
| Map tile | task_sufficient for visualization | full world-model microstate |
| Agent trace | audit_sufficient for emitted actions | total cognition or hidden tool state |

## Policy implication

Policy Fabric SHOULD deny claim promotion when the required sufficiency type is absent.

Sociosphere SHOULD report boundary surfaces whose declared sufficiency does not meet downstream consumer requirements.
