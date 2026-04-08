# Versioning

This document describes the versioning strategy for the Prophet Platform Standards.

---

## Version History

### v1.0 — Tekton + ArgoCD Baseline (Current)

**Released:** 2026-Q2  
**Status:** Active

Includes:
- ADR-040: Tekton + ArgoCD + GitOps Strategy
- ADR-050: DevSecOps, RBAC, and Audit Standards
- ADR-060: OTEL Observability and Telemetry Standards
- Tekton Templates: task-build, task-test, task-deploy, pipeline-build-test-deploy
- ArgoCD Templates: application, appproject, applicationset-multienv
- RBAC Templates: 4 ClusterRoles, 2 ServiceAccounts
- Kyverno Policies: signed-images, fips-validation, resource-limits, pod-security
- OTEL: collector config, Flask/APScheduler/Engine instrumentation
- Grafana: 4 dashboards (system-health, cost-tracking, compliance, propagation-waterfall)
- Schemas: audit-log-schema.avro
- Documentation: Getting Started, Deployment, Audit Log, OTEL, RBAC, Kyverno guides
- Governance: GOVERNANCE.md, VERSIONING.md, CONTRIBUTING.md

### v1.1 — Planned: Enhanced Observability (Additive)

**Target:** 2026-Q3  
**Status:** Planning

Planned additions:
- SLO definition templates (Prometheus recording rules)
- ArgoCD notification templates for Slack/PagerDuty
- Tekton EventListener templates (GitHub webhook ingestion)
- Cost alert Prometheus rules
- Per-environment retention policies

### v2.0 — Planned: Breaking Changes

**Target:** 2026-Q4  
**Status:** Proposal Phase  
**Breaking Change Notice:** Announced 6 months before release per GOVERNANCE.md

Planned breaking changes:
- Updated RBAC model (new `Operator` persona, removal of `Deployer` persona)
- Audit log schema v2 (new required fields)
- Migrating from OTEL Collector DaemonSet to sidecar injection via Kyverno

Migration guides will be published alongside the v2.0 release.

---

## Upgrade Paths

### v1.0 Initial Installation

No prior version. Follow [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

### v1.0 → v1.1 (Planned)

v1.1 is additive. No existing templates are modified.

1. Apply new templates from `tekton/`, `argocd/` (new files only)
2. Apply new Prometheus recording rules
3. No service restarts required

### v1.x → v2.0 (Planned)

Breaking changes require a migration period:

1. **6 months before v2.0**: Deprecation notices published in all affected files
2. **3 months before v2.0**: Migration guide published
3. **v2.0 release**: Old templates removed, new templates active
4. **90-day migration window**: Services must update within 90 days of v2.0 release

---

## Release Schedule

| Version | Target | Cadence |
|---------|--------|---------|
| Patch releases | As needed | Bug fixes and clarifications |
| Minor releases | Quarterly | Additive features |
| Major releases | Annually | Breaking changes (with 6-month notice) |

---

## Compatibility Matrix

| Standards Version | Kubernetes | Tekton | ArgoCD | Kyverno | OTEL Collector |
|------------------|-----------|--------|--------|---------|----------------|
| v1.0 | 1.26+ | v0.58+ | v2.10+ | v1.11+ | v0.96+ |
| v1.1 (planned) | 1.27+ | v0.60+ | v2.11+ | v1.12+ | v0.100+ |
