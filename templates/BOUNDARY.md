# Boundary Declaration: <owner/repo>

Status: draft | active | deprecated  
Schema: `schemas/boundary.schema.json`  
Machine record: `.socioprophet/boundary.yaml`

## 1. Jurisdiction

State the responsibility this repo owns. Keep this narrow enough to govern and broad enough to be useful.

## 2. Owned artifacts

List artifacts this repo may authoritatively produce.

| Artifact | Description | Claim modes | Sufficiency types |
| --- | --- | --- | --- |
| `<artifact>` | `<description>` | `<modes>` | `<types>` |

## 3. Explicit non-goals

This repo must not own:

- `<non-goal>`
- `<non-goal>`

## 4. Upstream inputs

| Producer repo | Artifact | Purpose | Required claim mode | Required sufficiency |
| --- | --- | --- | --- | --- |
| `<owner/repo>` | `<artifact>` | `<purpose>` | `<mode>` | `<type>` |

## 5. Downstream outputs

| Consumer repo | Artifact | Purpose | Required claim mode | Required sufficiency |
| --- | --- | --- | --- | --- |
| `<owner/repo>` | `<artifact>` | `<purpose>` | `<mode>` | `<type>` |

## 6. Claim modes

This repo may publish claims at these modes:

- `formal_construction`
- `illustrative_schema`
- `fixture_validated`
- `experimental_run`
- `independently_reproduced`
- `audited_run`

Remove modes this repo cannot currently support.

## 7. Sufficiency types

This repo may assert these sufficiency types:

- `microstate_sufficient`
- `reconstruction_sufficient`
- `semantic_sufficient`
- `task_sufficient`
- `governance_sufficient`
- `audit_sufficient`
- `not_sufficient`

Remove types this repo cannot currently support.

## 8. Trust roots and assumptions

| Trust root | Type | Assumption |
| --- | --- | --- |
| `<name>` | signature/hash/attestation/policy_bundle/schema/human_review/runtime/other | `<assumption>` |

## 9. Evidence requirements

| Claim mode | Required artifacts | Checker | Missing evidence behavior |
| --- | --- | --- | --- |
| `<mode>` | `<artifacts>` | `<checker>` | `INCONCLUSIVE` |

## 10. Allowed boundary crossings

List interfaces that may cross into or out of this repo.

- `<producer> -> <artifact> -> <consumer>`

## 11. Forbidden boundary crossings

List accesses, claims, or dependencies this repo must reject.

- `<forbidden crossing>`

## 12. Promotion gates

| From | To | Evidence | Policy |
| --- | --- | --- | --- |
| `<mode>` | `<mode>` | `<evidence>` | `<policy>` |

## 13. Maturity

Current level: `L0` through `L8`.

Next step:

- `<next boundary hardening step>`

## 14. Notes

Additional context, unresolved gaps, and known risks.
