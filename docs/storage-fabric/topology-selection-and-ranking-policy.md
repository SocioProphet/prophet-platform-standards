# Topology Selection and Ranking Policy

## Selection model

Topology selection is profile-based.

A profile describes the expected workload envelope, including:
- dominant role or roles
- read/write balance
- latency sensitivity
- mutability and replay needs
- offline or replication needs
- evidence and recovery posture

The selector evaluates candidates role-by-role rather than assuming a single backend should own all workloads.

## Ranked recommendation semantics

A ranked recommendation expresses:
- the profile being evaluated
- the storage role being satisfied
- ordered candidates
- a weighted score per candidate
- score breakdown
- evidence status
- history summary

## Normative score dimensions

The default dimensions are:
- workload fit
- evidence quality
- operability

Default weights SHOULD be:
- workload fit: `0.55`
- evidence quality: `0.35`
- operability: `0.10`

Implementations MAY tune these weights, but any deviation MUST be explicit and explainable.

## Evidence status semantics

A candidate MAY carry evidence status values such as:
- `reference-direct`
- `reference-proxy`
- `service-pass`
- `service-skip`
- `service-fail`
- `policy-fallback`
- `history-learned-long-horizon`

These statuses are explanatory. They do not replace the need for the score breakdown.

## PASS / SKIP / FAIL interpretation

When service-backed evidence is available:
- `PASS` strengthens candidate confidence
- `FAIL` penalizes the candidate
- `SKIP` means the evidence was not executed and MUST NOT be treated as a positive result

## Fallback rule

If service evidence is absent, the selector MAY fall back to workload-fit priors and reference evidence, but it MUST surface that fallback explicitly in the recommendation output.
