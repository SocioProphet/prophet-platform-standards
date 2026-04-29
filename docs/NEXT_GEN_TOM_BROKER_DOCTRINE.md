# Broker Doctrine for the Next Gen Operating Model

## Canonical lens

The Next Gen operating model is a cross-cloud services broker model.

It is not a generic cloud operating model. It is a governance, fulfillment, evidence, economics, and lifecycle model for brokering service classes across internal shared services, private cloud, public cloud, SaaS, partner services, and legacy adapters.

## What the broker standardizes

The broker standardizes:

- service request intake
- service contracts
- policy evaluation
- provider eligibility
- fulfillment blueprints
- service-instance registration
- evidence capture
- usage and cost metering
- lifecycle and exit obligations

## What the broker does not standardize

The broker does not pretend all providers are identical.

Provider-native capabilities may be exposed when they are:

- explicitly declared
- policy-bound
- metered
- evidence-producing
- exit-classified
- documented as native rather than portable

## Core doctrine statement

The broker standardizes service consumption, governance, evidence, and economics. It does not erase provider-native differences. Provider-native capabilities may be exposed when explicitly declared, policy-bound, metered, and exit-classified.

## Broker invariants

1. No service consumption without an owning service class.
2. No service fulfillment without an approved provider binding.
3. No provider binding without provider-class eligibility.
4. No live service instance without owner, cost meter, evidence pack, and lifecycle state.
5. No exception without owner, rationale, compensating controls, expiry, and review date.
6. No portability claim without a declared portability tier.
7. No benefit credit unless the brokered path materially displaces the manual path.
8. No provider-native feature exposure unless it is declared and governed.
9. No retirement without evidence closure, cost-meter closure, and exit evidence.
10. No broker bypass for production services except through an approved exception.

## Broker anti-patterns

The following are explicitly disallowed as broker design patterns:

- lowest-common-denominator abstraction that destroys provider value
- service catalog with no policy enforcement
- provisioning without registration
- registration without owner or cost center
- policy without implementation hooks
- cost showback based only on provider invoices
- exceptions without expiry
- claiming portability without tested or classified exit
- SaaS onboarding without provider evidence and data-exit terms
- legacy adapters marketed as modernization
- runtime routing decisions without recorded rationale
- manual evidence assembly as the normal operating path

## Use rule

When in doubt, prefer a truthful provider-specific binding over a misleading universal abstraction.
