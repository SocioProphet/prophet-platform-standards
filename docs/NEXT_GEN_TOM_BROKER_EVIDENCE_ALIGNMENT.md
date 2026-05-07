# Broker Evidence Alignment Map

## Purpose

The cross-cloud services broker should reference existing evidence artifacts before creating new broker-specific records.

The broker is the governance and provider-binding layer over the evidence/readiness spine. It should bind `ProviderBinding`, service class, provider class, policy decision, execution evidence, identity context, cost posture, and exit posture to current upstream records.

## Alignment rule

Do not create a new broker evidence record when an existing upstream artifact already proves the fact. Prefer reference, wrap only when required, extend only when a necessary broker field is missing, and reject artifacts that cannot support the declared service/provider posture.

## Evidence alignment table

| Evidence artifact | Owning path | Broker object supported | Service classes | Provider classes | Evidence type | Broker action | Required for approval | Portability impact |
|---|---|---|---|---|---|---|---|---|
| FogStackLiveClusterPreflightRecord | `prophet-platform/schemas/runtime/fogstack-live-cluster-preflight-record-v0.1.schema.json` | ProviderBinding, ServiceInstance | `environment`, `compute-runtime`, `api-integration` | `private-cloud`, `public-cloud`, `partner-managed-service` | readiness, safety | reference | conditional for live cluster use | P2/P3 only if preflight passes or blocks safely |
| FogStackRuntimeDryRunRecord | `prophet-platform/schemas/runtime/fogstack-runtime-dry-run-record-v0.1.schema.json` | ProviderBinding, ServiceInstance | `environment`, `compute-runtime`, `api-integration` | `private-cloud`, `public-cloud`, `partner-managed-service` | execution, policy, readiness | reference | yes for runtime mutation plans | P2/P3 when dry run is replayable and non-mutating |
| BrokerPolicyDecision | `policy-fabric/contracts/schemas/broker-policy-decision.schema.json` | PolicyDecision, ProviderBinding | all service classes | all provider classes | policy | reference | yes for production fulfillment | does not raise tier; gates use |
| BrokerExecutionBundle | `agentplane/schemas/broker-execution-bundle.schema.v0.1.json` | ProviderBinding, EvidencePack | all executable service classes | all provider classes | execution, replay | reference | conditional by service class | supports P3/P4 when validation/replay evidence exists |
| ProviderBinding | `prophet-platform/specs/brokerage/schemas/provider-binding.schema.json` | ProviderBinding | all service classes | all provider classes | binding metadata | authoritative runtime binding | yes | declares tier; does not prove tier alone |
| IdentitySubjectContext | `prophet-platform/contracts/identity/IdentitySubjectContext.v0.1.json` | PolicyDecision, EvidencePack | `identity-security`, `environment`, `compute-runtime`, `saas-subscription` | all provider classes | identity | reference | yes where subject identity is required | neutral |
| IdentitySessionContext | `prophet-platform/contracts/identity/IdentitySessionContext.v0.1.json` | PolicyDecision, ServiceRequest | all requestable service classes | all provider classes | identity/session | reference | conditional for session-bound requests | neutral |
| IdentityProofIngressRecord | `prophet-platform/contracts/identity/IdentityProofIngressRecord.v0.1.json` | PolicyDecision, EvidencePack | `identity-security`, `saas-subscription`, `partner-managed-service` | all provider classes | identity proof | reference | conditional by assurance policy | neutral |
| OfficeVersionRecord | `prophet-platform/schemas/office/office_version_record.schema.json` | ServiceInstance, EvidencePack | `saas-subscription`, `api-integration`, `legacy-adapter` | `internal-shared-service`, `saas`, `legacy-adapter` | content/version evidence | reference | conditional for office/document service classes | P1/P2 depending on format/export posture |
| OfficeWritebackRecord | `prophet-platform/schemas/office/office_writeback_record.schema.json` | ServiceInstance, EvidencePack | `saas-subscription`, `api-integration` | `internal-shared-service`, `saas` | writeback evidence | reference | conditional for writeback-capable bindings | P1/P2 if saveback can replay |
| OfficePolicyDecisionRecord | `prophet-platform/schemas/office/office_policy_decision_record.schema.json` | PolicyDecision, EvidencePack | `saas-subscription`, `api-integration` | `internal-shared-service`, `saas` | policy/side-effect evidence | reference | yes for side-effect actions | neutral |
| OfficeAdapterProfile | `prophet-platform/schemas/office/office_adapter_profile.schema.json` | ProviderBinding | `saas-subscription`, `api-integration`, `legacy-adapter` | `saas`, `legacy-adapter`, `internal-shared-service` | provider/adapter evidence | reference | yes for office adapter bindings | tier depends on adapter authority scope |

## Broker action vocabulary

- `reference`: broker points to the upstream artifact as authoritative evidence.
- `wrap`: broker creates a broker-local view that aggregates upstream evidence without duplicating its content.
- `extend`: upstream artifact is missing a required broker field and should gain a compatible field or companion contract.
- `reject`: artifact cannot support the claimed broker posture.

## Required evidence profile fields

Every service-class evidence profile should specify:

- required policy evidence
- required identity evidence
- required readiness evidence
- required execution or replay evidence
- required cost evidence
- required exit evidence
- conditional evidence by provider class

## Approval rule

A ProviderBinding can be approved only when its evidence profile is satisfied or when an explicit exception record describes missing evidence, compensating controls, owner, and expiry.

## Portability rule

ProviderBinding portability tier is a claim. It is valid only when matching evidence exists:

- P0: governance, policy, and evidence references are sufficient.
- P1: contract-compatible implementation evidence exists.
- P2: blueprint or equivalent fulfillment evidence exists.
- P3: operational readiness, continuity, evidence, and cost metadata exist.
- P4: exit or migration path has been tested and evidenced.
