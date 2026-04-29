# Service-Class and Provider-Class Matrix

## Purpose

This matrix gives the broker enough vocabulary to make honest service-routing, evidence, cost, and portability decisions.

## Service classes

| Service class | Description | Typical units | Mandatory controls |
|---|---|---|---|
| `environment` | Account, project, namespace, landing zone, or app environment | environment-day | owner, cost center, observability, expiry/retirement rule |
| `compute-runtime` | Kubernetes, serverless, VM pool, job/batch runtime | CPU-hour, memory-hour, request, job | runtime policy, scaling bounds, telemetry |
| `data-store` | Relational DB, document DB, object store, vector store, cache | instance, GB-month, IOPS, request | data class, backup, restore, encryption, retention |
| `messaging-eventing` | Queues, topics, streams, event buses | message, topic, partition, GB ingress/egress | retention, replay, access policy |
| `identity-security` | IAM integration, secrets, key management, security control services | principal, secret, key, policy pack | entitlement, rotation, audit, SoD |
| `observability` | Logs, metrics, traces, dashboards, alerts | GB ingested, metric series, trace span | retention, alert ownership, dashboard ownership |
| `api-integration` | API gateway, service mesh, external API boundary | route, request, egress GB | authn/z, rate limit, schema/version policy |
| `ai-ml-runtime` | Model serving, eval runtime, inference endpoints, GPU profiles | request, token, GPU-hour, eval run | model/runtime evidence, cost meter, safety/control policy |
| `saas-subscription` | Governed SaaS consumption and integration | user, seat, tenant, API call | vendor evidence, data boundary, exit terms |
| `legacy-adapter` | Brokered wrapper around legacy or black-box systems | adapter call, batch, transaction | manual-control declaration, evidence-gap register |
| `partner-managed-service` | Outsourced or partner-operated managed service | service unit, SLA tier, ticket, transaction | delegated control evidence, support model, contract linkage |

## Provider classes

| Provider class | Broker stance | Main risk |
|---|---|---|
| `internal-shared-service` | Preferred when mature and standardized | hidden capacity and informal ownership |
| `private-cloud` | Strong control posture with internal capacity management | platform maturity and scarcity |
| `public-cloud` | High automation potential with explicit native-service governance | cost volatility, jurisdiction, lock-in |
| `saas` | Subscription/API consumption with provider evidence | data exit, evidence dependency, contract lock-in |
| `partner-managed-service` | Delegated execution under brokered controls | control delegation and support handoff |
| `legacy-adapter` | Brokered wrapping, not modernization | evidence gaps and manual control remnants |

## Initial service/provider eligibility matrix

Legend:
- `A`: allowed default
- `C`: conditional; requires explicit provider binding and controls
- `N`: provider-native; allowed only as declared native feature
- `X`: not recommended as default

| Service class | Internal shared | Private cloud | Public cloud | SaaS | Partner service | Legacy adapter |
|---|---:|---:|---:|---:|---:|---:|
| `environment` | A | A | A | X | C | X |
| `compute-runtime` | A | A | A | X | C | X |
| `data-store` | A | A | A | C | C | C |
| `messaging-eventing` | A | A | A | C | C | C |
| `identity-security` | A | C | C | C | C | X |
| `observability` | A | A | A | C | C | C |
| `api-integration` | A | A | A | C | C | C |
| `ai-ml-runtime` | C | C | A | C | C | X |
| `saas-subscription` | X | X | X | A | C | X |
| `legacy-adapter` | X | X | X | X | C | A |
| `partner-managed-service` | X | C | C | C | A | C |

## Portability tiers

| Tier | Meaning |
|---|---|
| `P0-governed-native` | Provider-native service brokered through request/control/evidence/economics only |
| `P1-contract-compatible` | Same service class is exposed across providers, but implementation differs |
| `P2-blueprint-portable` | Common blueprint shape can fulfill across providers |
| `P3-operationally-portable` | Monitoring, backup, incident, evidence, and cost model are also portable |
| `P4-exit-tested` | Migration or exit path has been tested and evidenced |

## Required fields for every provider binding

Every provider binding must declare:

- service class
- provider class
- provider identifier
- blueprint reference
- policy pack references
- portability tier
- native feature exposure
- evidence profile
- cost meter profile
- continuity profile
- exit plan reference
- approval state

## Provider-selection factors

A broker provider-selection decision must consider:

- service class
- data classification
- jurisdiction and residency
- availability tier
- latency requirement
- expected unit cost
- approved provider profiles
- evidence requirements
- portability tier
- lock-in risk
- continuity requirements
- team maturity and support readiness

## Selection output

A provider-selection decision must record:

- selected provider binding
- rationale
- rejected alternatives
- policy decisions
- exception records, if applicable
