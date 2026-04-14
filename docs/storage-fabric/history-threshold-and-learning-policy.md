# History Threshold and Learning Policy

## Purpose

History-aware selection must distinguish meaningful drift from harmless noise.

## Canonical history classes

Recommendations and benchmark-history outputs MAY classify movement as:
- `improved`
- `regressed`
- `stable`
- `noise`
- `new`
- `missing`
- `no-data`

`noise` and `stable` are not the same:
- `noise` means movement exists but is not decision-relevant
- `stable` means no meaningful change signal is present

## Threshold policy

History interpretation SHOULD combine:
- noise bands
- minimum practical effect size
- persistence across a rolling window
- long-horizon threshold learning when enough preserved history exists

A candidate MUST NOT be classified as operationally regressed merely because one local microbenchmark sample moved slightly outside a single short-window expectation.

## Long-horizon learning

Long-horizon learning MAY activate only when enough preserved historical windows exist to support a learned threshold estimate.

Implementations SHOULD expose:
- whether learning is active
- what historical versions were used
- whether thresholds are learned or fallback

## Practical effect posture

The classifier SHOULD require more than raw delta. It SHOULD consider whether the observed movement is:
- outside the relevant noise band
- large enough to matter in practice
- persistent enough across the observed window

## Trust boundary

These semantics define the normative interpretation policy. Executable benchmark harnesses, repeated-run sampling logic, and synthetic fixtures belong in downstream conformance repositories.
