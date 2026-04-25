# ADR-070: Next Gen Operating Model

- Status: Proposed
- Date: 2026-04-14

## Context

The platform needs a vendor-neutral operating model that is suitable for hybrid-cloud service delivery, explicit control obligations, and measurable service economics. Existing platform and standards repositories already distinguish between normative standards and implementation repositories. The operating model therefore needs to live as a standard, not only as implementation prose inside a runtime repository.

## Decision

Adopt a **brokerage-centered, hybrid-cloud, ITaaS-style operating model** for platform-aligned services.

The model has five structural domains:
1. Engage
2. Orchestrate
3. Provision
4. Service
5. Control

The model must preserve three parallel views:
- structural ownership view
- benefits realization view
- enterprise journey/value view

Control is a centralized authority coalition spanning finance, security, audit, enterprise architecture, sourcing, HR, and PMO/change governance. Provision is the shared brokerage and fulfillment factory. Engage remains primarily tower-facing and federated.

## Consequences

### Positive
- separates normative operating doctrine from implementation details
- gives the platform a stable governance and decision-rights model
- supports service economics, control evidence, and brokered fulfillment
- aligns hybrid-cloud and legacy-adjacent work under one service model

### Negative
- adds governance overhead if implementation hooks are not automated
- requires clear central-versus-federated boundaries
- requires implementation repositories to bind the model carefully rather than copy it loosely

## Required follow-on

- maintain the canonical operating-model reference under `docs/`
- keep implementation bindings in runtime repositories such as `prophet-platform`
- enforce drift checks through cross-repo governance in the appropriate enforcement layer
