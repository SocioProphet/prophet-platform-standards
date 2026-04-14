# ADR-081: Topology Selection and Ranked Recommendations

## Status
Accepted

## Context

Workload profiles need explicit, inspectable storage recommendations rather than informal backend preferences.

## Decision

The platform standardizes ranked topology recommendations by role and profile. Rankings use three dimensions:
- workload fit
- evidence quality
- operability

Default weights are:
- workload fit: 0.55
- evidence quality: 0.35
- operability: 0.10

## Consequences

- recommendations are ordered and explainable
- missing service evidence stays visible instead of being treated as positive evidence
- downstream conformance tools may execute benchmarks, but the score dimensions remain standard
