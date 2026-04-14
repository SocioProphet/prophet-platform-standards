# ADR-082: History-Aware Threshold Learning

## Status
Accepted

## Context

History-aware storage ranking must distinguish meaningful drift from harmless movement.

## Decision

The platform standardizes history-aware threshold interpretation using:
- noise-aware classification
- minimum practical effect size
- persistence across a rolling window
- long-horizon threshold learning when enough preserved history exists

## Consequences

- one short benchmark movement is not enough to claim operational regression
- long-horizon learning may activate only when preserved history is sufficient
- executable conformance may implement the learning logic, but the interpretation policy remains standard
