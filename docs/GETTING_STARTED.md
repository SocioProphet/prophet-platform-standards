# Getting Started with Prophet Platform Standards

This guide walks you through bootstrapping a new repository to comply with the Prophet Platform DevSecOps, CI/CD, and Observability standards.

## Prerequisites

- Kubernetes cluster (1.26+)
- Tekton Pipelines v0.58+
- ArgoCD v2.10+
- Kyverno v1.11+
- OpenTelemetry Collector v0.96+
- Prometheus, Loki, Jaeger stack

---

## Onboarding Checklist

Use this checklist when onboarding a new service to the platform.

### 1. RBAC Setup

- [ ] Create a dedicated `ServiceAccount` for your service (copy from `rbac/service-account-webhook.yaml`)
- [ ] Bind the appropriate `ClusterRole` to your team:
  - Developers → `prophet-developer`
  - CI/CD system → `prophet-deployer`
  - Compliance team → `prophet-auditor`
- [ ] Store all RBAC resources in `rbac/` and apply via GitOps (ADR-040)
- [ ] Verify no `ClusterAdmin` bindings exist for workload service accounts

```bash
# Verify RBAC for your namespace
kubectl auth can-i --list --namespace=sociosphere --as=system:serviceaccount:sociosphere:<your-sa>

# Check for ClusterAdmin bindings (should be empty for workloads)
kubectl get clusterrolebindings -o json | jq '.items[] | select(.roleRef.name == "cluster-admin") | .subjects'
```

### 2. Tekton Pipeline Setup

- [ ] Copy `tekton/task-build.yaml`, `tekton/task-test.yaml`, `tekton/task-deploy.yaml` to your repo
- [ ] Copy `tekton/pipeline-build-test-deploy.yaml` and configure for your service
- [ ] Set up registry credentials secret: `registry-credentials`
- [ ] Set up ArgoCD token secret: `argocd-token`
- [ ] Configure the pipeline parameters (image, argocd-app-name, etc.)
- [ ] Test the pipeline with a dry run

```bash
# Apply pipeline templates to your cluster
kubectl apply -f tekton/ -n sociosphere

# Create a test PipelineRun
kubectl create -f - <<EOF
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  generateName: build-test-deploy-
  namespace: sociosphere
spec:
  pipelineRef:
    name: build-test-deploy
  params:
    - name: repo-url
      value: https://github.com/SocioProphet/<YOUR_REPO>
    - name: revision
      value: main
    - name: image
      value: ghcr.io/sociosphere/<YOUR_SERVICE>
    - name: argocd-staging-app
      value: <YOUR_APP>-staging
    - name: argocd-prod-app
      value: <YOUR_APP>-prod
    - name: gitops-repo-url
      value: https://github.com/SocioProphet/<YOUR_GITOPS_REPO>
    - name: skip-prod-deploy
      value: "true"  # start with staging only
  workspaces:
    - name: shared-source
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 1Gi
    - name: attestations
      emptyDir: {}
    - name: test-results
      emptyDir: {}
    - name: gitops-repo
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 500Mi
    - name: git-credentials
      secret:
        secretName: git-credentials
EOF
```

### 3. ArgoCD Setup

- [ ] Create an `AppProject` for your service (copy from `argocd/appproject-template.yaml`)
- [ ] Create an `Application` for staging (copy from `argocd/application-template.yaml`)
- [ ] Create an `Application` for prod with `automated: false` (manual gate)
- [ ] Register your GitOps repo in ArgoCD
- [ ] Configure RBAC for your team in the AppProject

```bash
# Apply ArgoCD resources
kubectl apply -f argocd/ -n argocd

# Verify application status
argocd app list
argocd app get <YOUR_APP>-staging
```

### 4. OTEL Instrumentation

- [ ] Add OTEL collector sidecar to your pod template (or enable Kyverno auto-injection)
- [ ] Install OTEL SDK in your service:
  ```bash
  # Python
  pip install opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-flask

  # Node.js
  npm install @opentelemetry/sdk-node @opentelemetry/exporter-otlp-grpc
  ```
- [ ] Copy the appropriate instrumentation template from `otel/`:
  - Flask service → `otel/webhook-instrumentation.py`
  - APScheduler → `otel/scheduler-instrumentation.py`
  - Propagation engine → `otel/engine-instrumentation.py`
- [ ] Set environment variables:
  ```yaml
  env:
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: "http://localhost:4317"
    - name: OTEL_SERVICE_NAME
      value: "<your-service-name>"
    - name: ENVIRONMENT
      value: "staging"
  ```
- [ ] Verify traces appear in Jaeger
- [ ] Verify metrics appear in Prometheus

### 5. Audit Logging

- [ ] Ensure your Tekton pipeline emits audit events (handled automatically by `pipeline-build-test-deploy.yaml`)
- [ ] Set the `AUDIT_LOG_ENDPOINT` environment variable in your pipeline's `audit-log` finally task
- [ ] Verify audit events appear in the audit log database
- [ ] Run a test query:
  ```sql
  SELECT * FROM audit_events 
  WHERE resource_repo = 'SocioProphet/<YOUR_REPO>'
  ORDER BY timestamp DESC 
  LIMIT 10;
  ```

### 6. Kyverno Policies

- [ ] Apply platform policies (done once per cluster):
  ```bash
  kubectl apply -f policies/
  ```
- [ ] Verify your pod is admitted successfully (not blocked by policies)
- [ ] Run a policy audit:
  ```bash
  kubectl get policyreport -n sociosphere
  ```
- [ ] Fix any policy violations before deploying to production

### 7. Grafana Dashboards

- [ ] Import dashboards from `grafana/`:
  ```bash
  # Via Grafana API
  for f in grafana/*.json; do
    curl -X POST \
      -H "Content-Type: application/json" \
      -d @"$f" \
      "http://admin:admin@grafana.monitoring.svc.cluster.local:3000/api/dashboards/import"
  done
  ```
- [ ] Verify metrics appear in **System Health** dashboard
- [ ] Set up alert notification channels in Grafana

---

## Reference Architecture

```
Your Repo (GitHub)
    │
    │ push event
    ▼
Tekton EventListener (sociosphere namespace)
    │
    ▼ PipelineRun: build-test-deploy
    ├── Task: build     → sign (cosign) + SBOM (syft) + attest (in-toto)
    ├── Task: test      → unit + integration tests, coverage ≥80%
    ├── Task: deploy-staging → ArgoCD sync → smoke tests
    └── Task: deploy-prod    → ArgoCD sync (manual gate) → smoke tests
         │
         └─── Audit log event → Postgres (ADR-050)
              OTEL trace → Jaeger (ADR-060)
              Metrics → Prometheus → Grafana (ADR-060)
```

---

## Reference Implementation

The [sociosphere](https://github.com/SocioProphet/sociosphere) repository is the canonical reference implementation of all these standards.

---

## Getting Help

- Open an issue in this repository for questions or ADR amendments
- See [GOVERNANCE.md](../GOVERNANCE.md) for the change process
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to propose changes
