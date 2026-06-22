# Guideplane operator workbench reference

## Purpose

Guideplane is a platform operator workbench for governed navigation, qualification, fulfillment, explanation, and outcome review.

It is not a chatbot pattern. It is not an execution engine. It is not an ontology authority. It is not a policy engine.

Guideplane gives operators a common work surface over existing platform authorities.

## Control planes

### Navigation plane

The navigation plane handles:

- inquiry capture
- context display
- intent framing
- ambiguity surfacing
- semantic narrowing
- capability routing
- reference-pattern lookup
- domain comparison
- offer comparison

### Qualification plane

The qualification plane handles:

- entitlement posture
- constraint visibility
- policy basis display
- access qualification
- obligations
- denials
- expiry
- escalation posture

Guideplane must show qualification state before fulfillment. It must not hide blocked or conditional states behind generic disabled controls.

### Fulfillment plane

The fulfillment plane handles:

- delivery request creation
- route selection
- channel selection
- artifact preview
- dispatch readiness
- escalation when dispatch is not allowed
- outcome review

Fulfillment must not proceed unless the relevant policy or access decision allows it or allows it with obligations.

## Workbench zones

A conforming Guideplane workbench should expose these zones or equivalent surfaces:

1. Context rail
2. Inquiry workspace
3. Route board
4. Policy and explanation rail
5. Fulfillment tray
6. Memory and outcome ledger

The zones may be collapsed or rearranged by viewport, but their information roles must remain inspectable.

## State model

The recommended top-level states are:

1. Initialize Context
2. Capture Inquiry
3. Frame Intent
4. Route and Narrow
5. Compare and Decide
6. Qualify Access
7. Fulfill or Escalate
8. Review Outcome

## Boundary rules

Guideplane must consume surrounding authorities instead of replacing them.

- Agent role and conformance standards come from `socioprophet-agent-standards`.
- Platform runtime contracts come from `prophet-platform`.
- Semantic and ontology mappings come from `ontogenesis` and SHIR.
- Execution evidence comes from `agentplane`.
- Policy verdicts come from `policy-fabric`.
- Workspace topology comes from `sociosphere`.

## Minimum conformance

A Guideplane implementation should:

- preserve the visible split between navigation, qualification, and fulfillment
- expose actor and operating context
- expose memory or prior context when used in ranking or suggestions
- expose why a route or offer was selected
- expose policy qualification before dispatch
- preserve denial and escalation context
- record outcome state after fulfillment or escalation

## Non-goals

This reference does not define JSON Schemas for runtime records.
This reference does not define UI pixel tokens.
This reference does not define SHIR mappings.
This reference does not define AgentPlane evidence records.
This reference does not define Policy Fabric verdict shapes.
