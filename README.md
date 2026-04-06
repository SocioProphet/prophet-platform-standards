# SocioProphet Platform Standards — DevSecOps, CI/CD, and Observability

**Canonical standards for the SocioProphet platform.**

This repository defines:
- **ADR-040:** Tekton + ArgoCD + GitOps strategy (SHOULD)
- **ADR-050:** DevSecOps, RBAC, and Audit standards (MUST)
- **ADR-060:** OTEL Observability and Telemetry (SHOULD)

## Quick Start
1. Read `adr/ADR-040-tekton-argocd-gitops.md`
2. Copy templates from `tekton/`, `argocd/`, `rbac/`
3. Follow `docs/GETTING_STARTED.md`
4. Reference implementation: [sociosphere](https://github.com/SocioProphet/sociosphere)

## Repository Map
- `adr/` — Architecture Decision Records
- `tekton/` — Tekton Task and Pipeline templates
- `argocd/` — ArgoCD Application and AppProject templates
- `rbac/` — Kubernetes RBAC role templates
- `policies/` — Kyverno admission policies
- `otel/` — OpenTelemetry collector and instrumentation
- `grafana/` — Grafana dashboard definitions
- `schemas/` — Avro schemas for audit logs
- `docs/` — Implementation guides

## Status
**v1.0 in development** — Validated by sociosphere reference implementation.

## License
MIT
