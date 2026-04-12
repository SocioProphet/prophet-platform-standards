# Forensic Genesis Edge Standards

This document defines the initial standards surface for the Forensic Genesis edge ingress lane.

## Scope
The edge lane standardizes **host-local evidence capture plus durable event publication** for forensic and validation observations. It does not replace deeper semantic or recovery pipelines; it feeds them.

## Operating model
1. Collect locally on the host.
2. Persist evidence to a local authoritative store.
3. Publish outbox records into Kafka fact topics.
4. Materialize latest-state views where useful.
5. Route selected records into downstream semantic lanes.

## Event classes in this first pass
- SNMP observations
- Mount observations
- Verification completion events
- Seal completion events

## Rules
- Edge records default to `structural_fact` claim class.
- Topic keys are deterministic and topic-specific.
- Heavy binary artifacts publish by manifest and digest, not inline payload.
- Schema changes require compatibility review.

## Relationship to runtime repo
`prophet-platform` carries runtime tooling, CI hooks, import helpers, deployment wiring, and consumers. This repository carries the normative schemas and ADRs.
