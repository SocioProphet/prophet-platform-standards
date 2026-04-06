# Deployment Guide

Step-by-step instructions for deploying the Prophet Platform observability and DevSecOps stack to a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.26+ cluster with cluster-admin access
- `kubectl` configured for your cluster
- `helm` v3.12+
- `argocd` CLI v2.10+
- `tkn` (Tekton CLI) v0.36+

---

## 1. Deploy OTEL Collector

### Apply ConfigMap and DaemonSet

```bash
# Apply the OTEL collector configuration
kubectl apply -f otel/collector-config.yaml

# Verify DaemonSet is running
kubectl rollout status daemonset/otel-collector -n sociosphere
kubectl get pods -n sociosphere -l app.kubernetes.io/name=otel-collector
```

### Configure Service Endpoints

Edit `otel/collector-config.yaml` to set the correct endpoints for your cluster:

```yaml
exporters:
  otlp/jaeger:
    endpoint: "jaeger-collector.monitoring.svc.cluster.local:4317"
  loki:
    endpoint: "http://loki.monitoring.svc.cluster.local:3100/loki/api/v1/push"
  prometheus:
    endpoint: "0.0.0.0:8889"
```

---

## 2. Deploy Prometheus + Loki + Jaeger (Observability Stack)

### Option A: kube-prometheus-stack (Recommended)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=15d \
  --set prometheus.prometheusSpec.retentionSize=10GB \
  --set grafana.enabled=true \
  --set grafana.adminPassword=<CHANGE_ME> \
  --wait

# Verify Prometheus is running
kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus
```

### Deploy Loki

```bash
helm repo add grafana https://grafana.github.io/helm-charts

helm upgrade --install loki grafana/loki \
  --namespace monitoring \
  --set loki.auth_enabled=false \
  --set loki.retention_period=30d \
  --wait
```

### Deploy Jaeger

```bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts

helm upgrade --install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --set provisionDataStore.cassandra=false \
  --set provisionDataStore.elasticsearch=true \
  --set storage.type=elasticsearch \
  --wait

# Verify Jaeger collector is running
kubectl get pods -n monitoring -l app.kubernetes.io/name=jaeger
```

### Import Grafana Dashboards

```bash
# Get Grafana pod name
GRAFANA_POD=$(kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana -o jsonpath='{.items[0].metadata.name}')

# Port-forward Grafana
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80 &

# Import dashboards
for dashboard in grafana/*.json; do
  echo "Importing: $dashboard"
  curl -s -X POST \
    -H "Content-Type: application/json" \
    -u "admin:<GRAFANA_PASSWORD>" \
    -d "{\"dashboard\": $(cat $dashboard), \"overwrite\": true}" \
    http://localhost:3000/api/dashboards/import
done

# Kill port-forward
kill %1
```

---

## 3. Deploy Kyverno (Policy Enforcement)

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm upgrade --install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set replicaCount=3 \
  --wait

# Verify Kyverno is running
kubectl get pods -n kyverno

# Apply platform policies
kubectl apply -f policies/

# Verify policies are installed
kubectl get clusterpolicies
```

### Verify Policy Enforcement

```bash
# Test that unsigned images are rejected
kubectl run test-unsigned --image=nginx:latest --restart=Never -n sociosphere
# Expected: Error from server: admission webhook "mutate.kyverno.svc" denied the request

# Check policy reports
kubectl get policyreports -n sociosphere
kubectl get clusterpolicyreports
```

---

## 4. Deploy ArgoCD

```bash
helm repo add argo https://argoproj.github.io/argo-helm

helm upgrade --install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set server.extraArgs="{--insecure}" \
  --set configs.params."server\.insecure"=true \
  --wait

# Get initial admin password
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d

# Apply AppProjects and Applications
kubectl apply -f argocd/

# Verify ArgoCD applications
argocd app list
```

### Configure ArgoCD RBAC

```bash
# Create ArgoCD RBAC ConfigMap
kubectl patch configmap argocd-rbac-cm -n argocd --patch '
data:
  policy.default: role:readonly
  policy.csv: |
    p, role:admin, applications, *, */*, allow
    p, role:deployer, applications, get, */*, allow
    p, role:deployer, applications, sync, */*, allow
    g, SocioProphet:platform-admins, role:admin
    g, SocioProphet:deployers, role:deployer
'
```

---

## 5. Deploy Tekton Pipelines

```bash
# Install Tekton Pipelines
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# Install Tekton Triggers (for GitHub webhook integration)
kubectl apply -f https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml

# Install Tekton Dashboard (optional)
kubectl apply -f https://storage.googleapis.com/tekton-releases/dashboard/latest/release.yaml

# Wait for Tekton to be ready
kubectl rollout status deployment/tekton-pipelines-controller -n tekton-pipelines

# Apply platform tasks and pipelines
kubectl apply -f tekton/ -n sociosphere

# Verify tasks are installed
tkn task list -n sociosphere
tkn pipeline list -n sociosphere
```

### Set Up Secrets

```bash
# Registry credentials (for pushing container images)
kubectl create secret docker-registry registry-credentials \
  --docker-server=ghcr.io \
  --docker-username=<GITHUB_USERNAME> \
  --docker-password=<GITHUB_PAT> \
  -n sociosphere

# ArgoCD token (for triggering syncs)
ARGOCD_TOKEN=$(argocd account generate-token --account tekton)
kubectl create secret generic argocd-token \
  --from-literal=ARGOCD_AUTH_TOKEN="${ARGOCD_TOKEN}" \
  -n sociosphere

# Git credentials (for cloning and pushing to GitOps repo)
kubectl create secret generic git-credentials \
  --from-literal=username=<GITHUB_USERNAME> \
  --from-literal=password=<GITHUB_PAT> \
  -n sociosphere
```

---

## 6. Apply RBAC Templates

```bash
# Apply all RBAC resources
kubectl apply -f rbac/

# Verify roles are created
kubectl get clusterroles | grep prophet
kubectl get clusterrolebindings | grep prophet

# Verify service accounts
kubectl get serviceaccounts -n sociosphere
```

---

## Verification Checklist

After completing the deployment, verify each component:

```bash
# OTEL Collector
kubectl get pods -n sociosphere -l app.kubernetes.io/name=otel-collector
# Expected: All pods Running

# Prometheus scraping OTEL metrics
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job == "prophet-platform")'

# Kyverno policies active
kubectl get clusterpolicies
# Expected: require-signed-images, require-fips-validation, require-resource-limits, enforce-pod-security

# ArgoCD applications synced
argocd app list
# Expected: all apps showing Healthy/Synced

# Tekton pipeline runs (trigger a test run)
tkn pipelinerun list -n sociosphere
# Expected: Recent successful pipeline runs

# Grafana dashboards
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80
# Open http://localhost:3000 — verify all 4 dashboards are present
```

---

## Troubleshooting

### OTEL Collector not receiving spans
```bash
kubectl logs -n sociosphere -l app.kubernetes.io/name=otel-collector -c otel-collector | grep -i error
# Check: Is the pod running? Are ports 4317/4318 accessible?
```

### Kyverno rejecting pods unexpectedly
```bash
kubectl get policyreport -n sociosphere -o yaml
# Check: Is the policy in Enforce mode? Is the image signed?
```

### ArgoCD sync failing
```bash
argocd app get <APP_NAME> --show-operation
# Check: Is the GitOps repo accessible? Are manifests valid?
```

### Tekton pipeline failing
```bash
tkn pipelinerun logs <PIPELINERUN_NAME> -n sociosphere --follow
# Check: Are secrets mounted correctly? Is the registry accessible?
```
