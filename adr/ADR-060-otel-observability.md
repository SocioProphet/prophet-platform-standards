# ADR-060: OTEL Observability and Telemetry Standards

**Status:** Accepted  
**Date:** 2026-04-06  
**Deciders:** Platform Engineering, SRE Team  
**Tags:** observability, otel, prometheus, grafana, jaeger, loki, telemetry

---

## Context and Problem Statement

The SocioProphet platform operates across multiple services (webhook handler, scheduler, propagation engine, DevOps orchestrator) and environments. Without centralized observability, the team cannot:
- Diagnose production incidents in a timely manner
- Track API quota consumption before hitting limits
- Measure the end-to-end latency of the propagation pipeline
- Prove compliance with SLOs
- Attribute costs to specific repos or operations

This ADR establishes mandatory OpenTelemetry (OTEL)-based observability standards across all platform services.

---

## Decision

**All platform services SHOULD be instrumented with OpenTelemetry. Traces go to Jaeger, metrics to Prometheus, and logs to Loki. Dashboards are in Grafana.**

### Requirements Language

Per RFC 2119:
- **MUST** — Mandatory requirement
- **SHOULD** — Recommended unless there is a specific reason not to
- **MAY** — Optional

---

## OTEL Instrumentation (SHOULD)

### Architecture

```
Service Pod
├── Application container
│     └── OTEL SDK → gRPC → OTEL Collector (sidecar, port 4317)
└── otel-collector sidecar
      ├── Receivers:  otlp/grpc (4317), otlp/http (4318)
      ├── Processors: batch, memory_limiter, resource_detector, tail_sampling
      └── Exporters:
            ├── prometheus → Prometheus (metrics)
            ├── otlp/grpc  → Jaeger (traces)
            └── loki       → Loki (logs)
```

### Requirements

1. Every production Pod **SHOULD** have an OTEL Collector sidecar injected (via Kyverno mutation policy or pod template).
2. All services **SHOULD** export telemetry via gRPC to the local sidecar on port 4317.
3. The following services **MUST** be instrumented: webhook handler, scheduler, propagation engine, DevOps orchestrator.
4. All OTEL SDKs **SHOULD** use automatic instrumentation where available (e.g., `opentelemetry-instrumentation-flask`).

### Trace Data Model

Every span **MUST** include:

| Field | Description |
|-------|-------------|
| `trace_id` | W3C TraceContext-compliant trace ID |
| `span_id` | Unique span identifier |
| `parent_span_id` | Parent span (null for root) |
| `service.name` | Service name (e.g., `webhook-handler`) |
| `duration_ms` | Span duration in milliseconds |
| `status` | `OK`, `ERROR` |
| `http.method` | HTTP method (for HTTP spans) |
| `http.status_code` | HTTP response code |
| `repo` | GitHub repository full name (custom attribute) |
| `actor` | GitHub user or SA (custom attribute) |
| `adr_reference` | Relevant ADR (custom attribute) |

---

## Metrics (Prometheus Exporter)

All metrics **SHOULD** follow Prometheus naming conventions: `<namespace>_<subsystem>_<name>_<unit>`.

### API Latency

```
prophet_api_request_duration_seconds{method, endpoint, status}
  Histogram: p50, p95, p99 buckets [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
```

### Webhook Delivery

```
prophet_webhook_deliveries_total{repo, status}          Counter
prophet_webhook_delivery_duration_seconds{repo}         Histogram
prophet_webhook_delivery_success_rate{repo}             Gauge
```

### Propagation Engine

```
prophet_propagation_runs_total{repo, status}            Counter
prophet_propagation_success_rate                        Gauge (target: ≥90%)
prophet_propagation_end_to_end_duration_seconds{repo}   Histogram
prophet_propagation_repos_affected_total{repo}          Counter
```

### Build / Deploy

```
prophet_build_duration_seconds{repo, branch}            Histogram
prophet_build_success_total{repo}                       Counter
prophet_build_failure_total{repo}                       Counter
prophet_deploy_rollback_total{repo, env}                Counter
```

### API Quota Tracking

```
prophet_github_api_calls_total{repo, endpoint}          Counter
prophet_github_api_calls_per_hour{repo}                 Gauge
prophet_github_api_quota_percent_used                   Gauge (alert >80%)
prophet_github_api_cost_per_sprint{repo}                Gauge
```

### System Health

```
prophet_pod_restarts_total{pod, namespace}              Counter
prophet_error_rate{service}                             Gauge
prophet_queue_depth{queue_name}                         Gauge
```

---

## Traces (Jaeger Exporter)

### Requirements

1. Full end-to-end traces **MUST** be emitted for the critical path:
   ```
   webhook.received → tekton.pipeline_run.triggered → tekton.build.complete
       → tekton.test.complete → argocd.sync.initiated → argocd.sync.complete
   ```
2. Traces **MUST** preserve error context: which step failed, the error message, and the affected repository.
3. Trace context **MUST** be propagated across service boundaries using W3C `traceparent` headers.
4. Sampling strategy: tail-based sampling at 10% for success paths; 100% for error paths.
5. Traces **MUST** be correlated with audit log entries via the `trace_id` field.

### Key Trace Spans

| Span Name | Parent | Tags |
|-----------|--------|------|
| `webhook.received` | (root) | `repo`, `event_type`, `delivery_id` |
| `tekton.pipeline.triggered` | `webhook.received` | `pipeline_run_name`, `commit_sha` |
| `tekton.task.build` | `tekton.pipeline.triggered` | `image_digest`, `duration_ms` |
| `tekton.task.test` | `tekton.pipeline.triggered` | `coverage_pct`, `test_count` |
| `argocd.sync.initiated` | `tekton.task.build` | `app_name`, `env`, `revision` |
| `argocd.sync.complete` | `argocd.sync.initiated` | `status`, `resources_synced` |

---

## Logs (Loki Exporter)

### Requirements

1. All service logs **SHOULD** be centralized in Loki.
2. Logs **MUST** be structured JSON.
3. Every log line **MUST** include `trace_id` and `span_id` for correlation with traces.
4. Log labels **MUST** include: `service`, `namespace`, `env`, `repo` (where applicable).
5. Logs **MUST** be searchable by: `trace_id`, `span_id`, `repo`, `timestamp`, `level`.
6. Audit log entries (from ADR-050) **SHOULD** be mirrored to Loki for cross-system correlation.

### Log Format

```json
{
  "timestamp": "2026-04-06T02:14:42.856Z",
  "level": "INFO",
  "service": "webhook-handler",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "repo": "SocioProphet/sociosphere",
  "message": "Webhook event received",
  "event_type": "push",
  "delivery_id": "abc-123"
}
```

---

## Dashboards (Grafana)

### Requirements

1. All dashboards **SHOULD** be defined as JSON and stored in `grafana/`.
2. Dashboards **MUST** auto-refresh at ≤ 30-second intervals for real-time monitoring.
3. Alerts **MUST** be shown inline within relevant dashboards.

### Dashboard Inventory

| Dashboard | File | Purpose |
|-----------|------|---------|
| System Health | `dashboard-system-health.json` | Real-time service health, SLOs |
| Cost Tracking | `dashboard-cost-tracking.json` | API usage, cost per repo |
| Compliance | `dashboard-compliance.json` | Signing coverage, policy violations |
| Propagation Waterfall | `dashboard-propagation-waterfall.json` | E2E latency breakdown |

### System Health Dashboard

Panels:
- Webhook delivery rate (target: ≥95% success)
- Propagation success rate (target: ≥90%)
- API request latency p95 (target: <1 minute)
- Active PipelineRuns
- ArgoCD sync status per environment
- Recent error log stream

### Cost Tracking Dashboard

Panels:
- GitHub API calls per hour (with 80%/95% quota lines)
- API calls per repo (top 10)
- Cost per propagation (estimated)
- Budget burn rate (daily/weekly/monthly)
- Trend: efficiency over time

### Compliance Dashboard

Panels:
- % builds with valid signatures (target: ≥95%)
- % images scanned for vulnerabilities (target: 100%)
- Audit log coverage (% deploys with audit events)
- Failed Kyverno policies (target: 0)
- RBAC violations (target: 0)
- FIPS compliance rate (target: 100%)

### Propagation Waterfall Dashboard

Panels:
- Timeline: `webhook.received` → `argocd.sync.complete` (Gantt-style)
- Per-repo latency breakdown
- Bottleneck identification (slowest spans)
- Failed propagations with error context

---

## Alerting Rules

All alerts **MUST** be defined as Prometheus `PrometheusRule` resources and stored alongside dashboards.

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| `APIQuotaWarning` | `prophet_github_api_quota_percent_used > 80` | Warning | Notify team channel |
| `APIQuotaCritical` | `prophet_github_api_quota_percent_used > 95` | Critical | Page on-call immediately |
| `PropagationFailureCritical` | `prophet_propagation_success_rate < 0.90` | Critical | Page on-call |
| `WebhookLatencyWarning` | `prophet_webhook_delivery_duration_seconds{p95} > 5` | Warning | Notify team channel |
| `BuildFailureRateCritical` | `rate(prophet_build_failure_total[5m]) / rate(prophet_build_success_total[5m]) > 0.05` | Critical | Page on-call |
| `UnsignedImageCritical` | Custom metric from Kyverno | Critical | Page on-call + block deploys |

---

## Retention Policy

| Signal | Retention | Storage |
|--------|-----------|---------|
| Metrics | 15 days | Prometheus TSDB |
| Traces | 7 days | Jaeger (object store) |
| Logs | 30 days | Loki (object store) |
| Audit Log | 1 year minimum (immutable) | Postgres (append-only) |

Long-term metric aggregates (daily/weekly rollups) **MAY** be retained beyond 15 days in a separate store for capacity planning.

---

## Resource Overhead

| Component | CPU | Memory |
|-----------|-----|--------|
| OTEL Collector sidecar | 50m | 100Mi |
| Prometheus (per cluster) | 500m | 2Gi |
| Loki (per cluster) | 500m | 1Gi |
| Jaeger (per cluster) | 250m | 512Mi |
| Grafana | 100m | 256Mi |

Total overhead per instrumented Pod: ~100MB RAM, ~50m CPU.

---

## Consequences

### Positive
- Full observability across the entire propagation pipeline
- SLO tracking with data-driven improvement cycles
- Cost attribution per repo for capacity planning
- Security observability: unsigned images, RBAC violations surfaced in real-time
- Incident response accelerated by correlated traces + logs + metrics

### Negative
- Resource overhead: ~100MB RAM per instrumented pod for the sidecar
- Prometheus + Loki + Jaeger stack required in every environment
- Operator training required for Grafana and PromQL
- Trace sampling must be tuned to balance cost vs. coverage

### Neutral
- All new services **SHOULD** instrument before deploying to staging
- Existing services **SHOULD** instrument within 60 days of ADR acceptance

---

## Related ADRs

- [ADR-040](ADR-040-tekton-argocd-gitops.md) — Tekton + ArgoCD + GitOps Strategy
- [ADR-050](ADR-050-devsecops-rbac-audit.md) — DevSecOps, RBAC, and Audit Standards

---

## References

- [OpenTelemetry](https://opentelemetry.io/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [Jaeger](https://www.jaegertracing.io/)
- [Loki](https://grafana.com/docs/loki/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
