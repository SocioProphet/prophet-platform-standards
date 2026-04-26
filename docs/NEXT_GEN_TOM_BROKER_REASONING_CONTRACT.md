# Broker Reasoning Contract v0

## Purpose

This contract defines the reasoning loop around the cross-cloud services broker.

The broker is the object of reasoning. The ecosystem reasons about broker requests, provider bindings, policy decisions, execution evidence, operational exhaust, curriculum promotion, and workspace governance.

## Plane roles

| Plane | Role |
|---|---|
| BrokerPlane | Represents service requests, service classes, provider bindings, service instances, evidence packs, and cost meters |
| PolicyPlane | Evaluates policy, provider eligibility, exception posture, evidence requirements, and approval obligations |
| AgentPlane | Executes validation, placement, smoke, continuity, exit, and replay bundles and emits evidence artifacts |
| SocioSphere | Governs workspace topology, dependency direction, drift, source exposure, hardening critique, and cross-repo propagation |
| DevSecOps Intelligence | Ingests operational exhaust and produces broker risk findings, drift findings, and routing recommendations |
| Alexandrian Academy | Converts validated patterns and failures into training, evaluations, and canon learning objects |

## Canonical broker events

- `broker.request.submitted`
- `broker.request.classified`
- `broker.provider_binding.selected`
- `broker.policy_decision.recorded`
- `broker.exception.opened`
- `broker.fulfillment.started`
- `broker.service_instance.registered`
- `broker.evidence_pack.updated`
- `broker.cost_meter.updated`
- `broker.exit_plan.tested`
- `broker.binding.suspended`
- `broker.binding.promoted`
- `broker.binding.retired`

## Required reasoning outputs

- `BrokerRiskFinding`
- `ProviderBindingRecommendation`
- `PortabilityTierAssessment`
- `EvidenceCompletenessFinding`
- `CostAnomalyFinding`
- `PolicyExceptionAgingFinding`
- `ServiceClassCoverageGap`
- `AcademyTrainingRecommendation`
- `SocioSpherePropagationPlan`

## Handoff rules

1. BrokerPlane must not fulfill a production service without a PolicyPlane decision or an explicit exception.
2. PolicyPlane must return the policy snapshot and evidence requirements used for the decision.
3. AgentPlane must emit validation, placement, run, and replay evidence for broker validation bundles.
4. DevSecOps Intelligence must treat broker exhaust as evidence-backed operational graph input, not as free-text status.
5. Alexandrian Academy must only promote broker training objects to canon when evidence and evaluation records exist.
6. SocioSphere must propagate broker-standard changes to all affected implementation and reasoning repos.
7. No plane may claim portability unless the declared portability tier and supporting evidence are present.

## Minimum evidence edges

Every broker reasoning record should be able to link to:

- service class
- provider class
- provider binding
- policy decision
- exception record, if applicable
- service instance
- cost meter
- evidence pack
- execution or replay artifact, if applicable
- curriculum/evaluation object, if applicable
- propagation or hardening finding, if applicable

## Design invariant

Policy decides. AgentPlane executes. DevSecOps Intelligence reasons. Alexandrian Academy teaches. SocioSphere governs cross-repo propagation. BrokerPlane coordinates the service lifecycle without collapsing those responsibilities.
