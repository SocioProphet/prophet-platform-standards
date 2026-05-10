# Claim Modes v0.1

Claim modes are evidence types. They prevent a document, repo, CI result, model card, proof artifact, or demo from implying more certainty than its supporting evidence permits.

## Modes

### formal_construction
A definition, schema, theorem statement, proof sketch, or architecture doctrine. No executed run is implied.

Required evidence:
- versioned document or schema;
- explicit assumptions;
- explicit non-claims.

### illustrative_schema
An example packet, artifact, or config illustrating expected shape. It is not evidence that a system has executed successfully.

Required evidence:
- example artifact;
- statement that values are illustrative;
- validation against schema if possible.

### fixture_validated
A deterministic fixture or toy run was executed and replayed.

Required evidence:
- fixture input artifact;
- expected result;
- verification output;
- pinned tool/schema versions.

### experimental_run
A real or realistic run was executed under declared assumptions.

Required evidence:
- input hashes;
- environment or runtime metadata;
- result artifact;
- assumptions and coverage contract;
- failure/uncertainty handling.

### independently_reproduced
A second rater, implementation, environment, or verifier reproduced the result.

Required evidence:
- independent run artifact;
- comparison report;
- disagreement/adjudication notes where applicable.

### audited_run
An internal or external reviewer accepted the evidence bundle under an audit protocol.

Required evidence:
- evidence bundle manifest;
- audit or review record;
- scope of acceptance;
- unresolved findings if any.

## Promotion rules

A claim may only move upward when the target mode's evidence requirements are satisfied. Promotions are boundary transitions and SHOULD be evaluated by Policy Fabric.

Invalid promotions:

- README statement -> `fixture_validated` without fixture run.
- CI green -> `audited_run` without audit record.
- system card -> `microstate_sufficient` unless it reconstructs the declared latent state.
- single-team evidence packet -> `independently_reproduced` without second rater or implementation.

## Verdict relation

Proof artifact verdicts and claim modes are separate axes.

- A `PROVED` fixture can support `fixture_validated`.
- A `PROVED` experimental run can support `experimental_run`.
- A `VIOLATION` can be high-quality evidence, but it blocks promotion.
- An `INCONCLUSIVE` artifact is valid evidence of uncertainty, not proof of safety.

## Public-surface rule

Any user-facing page, demo, release note, or model/system card MUST preserve the underlying claim mode. Public language cannot promote a claim beyond its evidence bundle.
