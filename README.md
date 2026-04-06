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

```
prophet-platform-standards/
├── adr/                          Architecture Decision Records
│   ├── ADR-040-tekton-argocd-gitops.md
│   ├── ADR-050-devsecops-rbac-audit.md
│   └── ADR-060-otel-observability.md
├── tekton/                       Tekton Task and Pipeline templates
│   ├── task-build.yaml           Build, sign (cosign), SBOM (syft), attest (in-toto)
│   ├── task-test.yaml            Unit + integration tests, coverage ≥80%
│   ├── task-deploy.yaml          Deploy via ArgoCD with smoke tests + rollback
│   └── pipeline-build-test-deploy.yaml  Orchestrated CI/CD pipeline
├── argocd/                       ArgoCD Application and AppProject templates
│   ├── application-template.yaml
│   ├── appproject-template.yaml
│   └── applicationset-multienv.yaml     Dev/staging/prod with promotion gates
├── rbac/                         Kubernetes RBAC role templates
│   ├── cluster-role-admin.yaml
│   ├── cluster-role-developer.yaml
│   ├── cluster-role-deployer.yaml
│   ├── cluster-role-auditor.yaml
│   ├── service-account-webhook.yaml
│   └── service-account-scheduler.yaml
├── policies/                     Kyverno admission policies
│   ├── policy-signed-images.yaml
│   ├── policy-fips-validation.yaml
│   ├── policy-resource-limits.yaml
│   └── policy-pod-security.yaml
├── otel/                         OpenTelemetry collector and instrumentation
│   ├── collector-config.yaml
│   ├── webhook-instrumentation.py
│   ├── scheduler-instrumentation.py
│   └── engine-instrumentation.py
├── grafana/                      Grafana dashboard definitions
│   ├── dashboard-system-health.json
│   ├── dashboard-cost-tracking.json
│   ├── dashboard-compliance.json
│   └── dashboard-propagation-waterfall.json
├── schemas/                      Avro schemas for audit logs
│   └── audit-log-schema.avro
├── docs/                         Implementation guides
│   ├── GETTING_STARTED.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── AUDIT_LOG_GUIDE.md
│   ├── OTEL_INSTRUMENTATION_GUIDE.md
│   ├── RBAC_GUIDE.md
│   └── KYVERNO_GUIDE.md
├── GOVERNANCE.md
├── VERSIONING.md
└── CONTRIBUTING.md
```

## Status
**v1.0** — Validated by sociosphere reference implementation.

## License
Apache-2.0
