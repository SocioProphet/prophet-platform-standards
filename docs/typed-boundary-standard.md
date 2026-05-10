# Typed Boundary Standard v0.1

Status: normative draft.

This standard defines how SocioProphet repos declare jurisdiction, claim modes, evidence contracts, sufficiency levels, and boundary crossings. It is the common contract consumed by Sociosphere, Policy Fabric, Prophet Platform, Model Governance Ledger, and downstream runtime or OS trust layers.

## 1. Core doctrine

A boundary is a typed interface between a producer, a consumer, and a claim. It is not just a folder, API, repo, or service edge. A boundary states what a component owns, what it may emit, what it may consume, and what evidence is required before another component may rely on its outputs.

The canonical chain is:

```text
latent state -> typed trace -> semantic/policy lift -> claim -> evidence artifact -> checker verdict -> admissibility gate
```

The same structure applies across the estate:

- physics/interface papers: bulk state, trace map, reconstruction, semantic lift;
- lawful learning: constraints, gates, active boundary, claim mode, ledger;
- Trust-First Security: Event-IR, assumptions, constraints, abstract domains, proof artifact, checker;
- GitOps: repo jurisdiction, PR transition, CI evidence, release/admission policy.

## 2. Boundary record

Every governed repo SHOULD provide a human-readable `BOUNDARY.md` and a machine-readable `.socioprophet/boundary.yaml` conforming to `schemas/boundary.schema.json`.

A boundary record declares:

- `jurisdiction`: the responsibility this repo owns.
- `non_goals`: what this repo must not own.
- `owned_artifacts`: outputs for which this repo is authoritative.
- `upstream_inputs`: artifacts, schemas, policies, or evidence consumed from other jurisdictions.
- `downstream_outputs`: artifacts, schemas, policies, APIs, or evidence emitted for other jurisdictions.
- `claim_modes`: which claim strengths this repo may publish.
- `sufficiency_types`: which sufficiency levels its surfaces may assert.
- `trust_roots`: cryptographic, procedural, or runtime assumptions required for claims.
- `evidence_required`: evidence needed for each promoted claim.
- `allowed_crossings`: permitted boundary interactions.
- `forbidden_crossings`: interactions that must be denied or treated as violations.
- `promotion_gates`: conditions required to advance claim mode.
- `maturity`: current boundary implementation level.

## 3. Claim-mode discipline

Claim modes are types. A lower-evidence artifact cannot silently present itself as a higher-evidence artifact.

Normative modes:

1. `formal_construction`: definition, schema, or proof sketch only.
2. `illustrative_schema`: example structure; not executed evidence.
3. `fixture_validated`: deterministic fixture run exists and is replayable.
4. `experimental_run`: real data or realistic system run exists; assumptions declared.
5. `independently_reproduced`: a second implementation or rater reproduced the result.
6. `audited_run`: independent review or audit accepted the evidence bundle.

A claim promotion MUST declare the source mode, target mode, evidence artifact, and policy gate authorizing the transition.

## 4. Evidence verdicts

Trust-First proof artifacts use three operational verdicts:

- `PROVED`: the claim holds for all traces consistent with the observed Event-IR window and declared assumptions.
- `VIOLATION`: a counterexample or witness slice demonstrates a forbidden state or transition.
- `INCONCLUSIVE`: required evidence, trust roots, precision, or budget are insufficient to prove or refute the claim.

A dashboard, log excerpt, README statement, or human narrative is never by itself `PROVED`.

## 5. Sufficiency types

A boundary surface must say what it is sufficient for:

- `microstate_sufficient`: reconstructs the underlying latent state in scope.
- `reconstruction_sufficient`: reconstructs a declared sector with bounded error.
- `semantic_sufficient`: preserves task-relevant meaning under the semantic lift.
- `task_sufficient`: supports a specific action or decision.
- `governance_sufficient`: supports policy, audit, escalation, or deployment governance.
- `audit_sufficient`: supports independent replay or assessor review.
- `not_sufficient`: explicitly not enough for the stated claim.

Semantic sufficiency is not microstate sufficiency. The standard requires this distinction because many governance surfaces are intentionally microstate-incomplete but still adequate for policy decisions.

## 6. Boundary crossing rules

A boundary crossing is admissible only when:

1. the producer boundary declares the output;
2. the consumer boundary declares the input;
3. the artifact carries an allowed claim mode;
4. required evidence is present;
5. Policy Fabric admits the transition;
6. Sociosphere can register the crossing in the Boundary Atlas.

If any required evidence family is absent, the crossing MUST NOT be upgraded to a stronger claim. The correct result is `INCONCLUSIVE` unless a violation is directly witnessed.

## 7. Maturity levels

- `L0`: repo exists; boundary informal.
- `L1`: `BOUNDARY.md` exists.
- `L2`: `.socioprophet/boundary.yaml` exists.
- `L3`: schema validation exists.
- `L4`: claim-mode/evidence gates exist in CI or policy.
- `L5`: Sociosphere ingests boundary metadata.
- `L6`: cross-repo boundary checks run on PRs or release.
- `L7`: release artifacts carry evidence bundles and sufficiency labels.
- `L8`: independent replay or audit exists.

## 8. Required repository behavior

New governed repos SHOULD add boundary files before claiming production readiness. Existing governed repos SHOULD add boundary files during their next architecture or governance pass.

No repo SHOULD consume another repo's artifact as authoritative unless the producer and consumer boundary declarations agree.

No repo SHOULD emit public/demo claims stronger than its evidence mode.

## 9. Initial consumers

- `SocioProphet/sociosphere`: estate Boundary Atlas.
- `SocioProphet/policy-fabric`: admissibility and promotion gates.
- `SocioProphet/prophet-platform`: run bundles, checkers, proof artifacts.
- `SocioProphet/model-governance-ledger`: sufficiency scoring and evidence packets.
- `SocioProphet/ontogenesis`: schema-to-law compilation.
- `SourceOS-Linux/sourceos-boot`: boot trust boundary.
- `SourceOS-Linux/sourceos-syncd`: local-first state integrity boundary.
