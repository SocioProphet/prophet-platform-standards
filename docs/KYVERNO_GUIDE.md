# Kyverno Guide

Reference guide for understanding, writing, testing, and operating Kyverno admission policies on the Prophet Platform.

Kyverno policies implement the Policy as Code requirements defined in ADR-050.

---

## Kyverno Architecture

Kyverno operates as a Kubernetes admission webhook:

```
kubectl apply / Tekton deploy / ArgoCD sync
    │
    ▼ Kubernetes API Server
    │
    ├── Mutating Admission Webhook (Kyverno)
    │       └── Mutate: add labels, inject sidecars, set defaults
    │
    ├── Validating Admission Webhook (Kyverno)
    │       └── Validate: enforce rules, reject non-compliant resources
    │
    └── Resource created in cluster
```

Kyverno policies can:
- **Validate**: Allow or deny resources based on rules
- **Mutate**: Automatically modify resources (add labels, defaults)
- **Generate**: Create related resources automatically
- **Verify Images**: Validate cosign signatures and attestations

---

## Platform Policies

| Policy | File | Mode | Effect |
|--------|------|------|--------|
| Require Signed Images | `policy-signed-images.yaml` | Enforce | Reject unsigned images |
| FIPS Validation | `policy-fips-validation.yaml` | Enforce | Reject non-FIPS images |
| Resource Limits | `policy-resource-limits.yaml` | Enforce | Reject pods without limits |
| Pod Security | `policy-pod-security.yaml` | Enforce | Reject insecure pods |

### Apply All Policies

```bash
kubectl apply -f policies/

# Verify all policies are installed and ready
kubectl get clusterpolicies
# NAME                        ADMISSION   BACKGROUND   VALIDATE ACTION   READY
# require-signed-images       true        true         Enforce           True
# require-fips-validation     true        true         Enforce           True
# require-resource-limits     true        true         Enforce           True
# enforce-pod-security        true        true         Enforce           True
```

---

## Writing Policies

### Policy Structure

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: my-policy
  annotations:
    policies.kyverno.io/title: Human-readable title
    policies.kyverno.io/category: Category
    policies.kyverno.io/severity: low|medium|high|critical
    policies.kyverno.io/description: |
      What this policy does and why.
spec:
  # Enforce = reject; Audit = allow but report
  validationFailureAction: Enforce
  
  # Also check existing resources (background scan)
  background: true
  
  rules:
    - name: my-rule
      match:
        any:
          - resources:
              kinds: [Pod]
              namespaces: [sociosphere]
      exclude:
        any:
          - resources:
              namespaces: [kube-system]
      validate:
        message: "Helpful error message explaining what to fix"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
```

### Validation Rule Patterns

```yaml
# Require a field to exist and be non-empty
pattern:
  metadata:
    labels:
      app: "?*"

# Require a field to have a specific value
pattern:
  spec:
    containers:
      - securityContext:
          readOnlyRootFilesystem: true

# Deny a specific condition (deny rule)
deny:
  conditions:
    any:
      - key: "{{ request.object.spec.hostNetwork }}"
        operator: Equals
        value: true

# Check with JMESPath expression
deny:
  conditions:
    any:
      - key: "{{ request.object.spec.containers[].resources.limits.memory | [0] }}"
        operator: GreaterThan
        value: "8Gi"
```

### Image Verification Rules

```yaml
verifyImages:
  - imageReferences:
      - "ghcr.io/sociosphere/*"
    attestors:
      - count: 1
        entries:
          - keyless:
              subject: "https://github.com/SocioProphet/*/.github/workflows/*.yaml@refs/heads/main"
              issuer: "https://token.actions.githubusercontent.com"
    # Verify SBOM attestation
    attestations:
      - predicateType: https://spdx.dev/Document
    mutateDigest: true
    required: true
```

---

## Testing Policies

### Method 1: Kyverno CLI (Recommended for CI)

```bash
# Install Kyverno CLI
brew install kyverno  # macOS
# or
curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_amd64.tar.gz

# Test a policy against a resource
kyverno apply policies/policy-pod-security.yaml \
  --resource /path/to/test-pod.yaml

# Test with expected results
kyverno test /path/to/policy-tests/
```

### Method 2: Test Resources in Cluster (Development)

```bash
# Switch to Audit mode temporarily for testing
kubectl patch clusterpolicy enforce-pod-security \
  --type merge \
  -p '{"spec":{"validationFailureAction":"Audit"}}'

# Apply your test pod
kubectl apply -f test-pod.yaml -n sociosphere

# Check policy report
kubectl get policyreport -n sociosphere -o yaml

# Switch back to Enforce
kubectl patch clusterpolicy enforce-pod-security \
  --type merge \
  -p '{"spec":{"validationFailureAction":"Enforce"}}'
```

### Policy Test Framework

Create a `kyverno-tests/` directory with test cases:

```
kyverno-tests/
├── pod-security/
│   ├── kyverno-test.yaml        # Test definition
│   ├── pass-compliant-pod.yaml  # Should pass
│   └── fail-privileged-pod.yaml # Should fail
```

**kyverno-test.yaml:**
```yaml
name: pod-security-tests
policies:
  - ../../policies/policy-pod-security.yaml
resources:
  - pass-compliant-pod.yaml
  - fail-privileged-pod.yaml
results:
  - policy: enforce-pod-security
    rule: deny-privileged-containers
    resource: pass-compliant-pod
    result: pass
  - policy: enforce-pod-security
    rule: deny-privileged-containers
    resource: fail-privileged-pod
    result: fail
```

**Run tests:**
```bash
kyverno test kyverno-tests/pod-security/
```

---

## Checking Policy Reports

```bash
# Namespace-scoped policy report
kubectl get policyreport -n sociosphere

# Detailed policy report
kubectl describe policyreport <REPORT_NAME> -n sociosphere

# Cluster-scoped policy report
kubectl get clusterpolicyreport

# Find failing policies
kubectl get policyreport -A -o json | \
  jq '.items[] | {
    namespace: .metadata.namespace,
    failures: [.results[] | select(.result == "fail") | {policy, rule, resource: .resources[0].name}]
  } | select(.failures | length > 0)'

# Find specific violations
kubectl get policyreport -n sociosphere -o json | \
  jq '.items[].results[] | select(.result == "fail") | {
    policy: .policy,
    rule: .rule,
    resource: .resources[0].name,
    message: .message
  }'
```

---

## Policy Exceptions

If a workload has a legitimate reason to bypass a policy:

1. **Document the exception** as an ADR amendment or issue
2. **Get Security Team approval**
3. **Create a PolicyException** resource (Kyverno v1.10+):

```yaml
apiVersion: kyverno.io/v2beta1
kind: PolicyException
metadata:
  name: my-service-exception
  namespace: sociosphere
  annotations:
    adr.sociosphere.io/exception-justification: "This service requires privileged access for X reason"
    adr.sociosphere.io/approved-by: "security-team@sociosphere.io"
    adr.sociosphere.io/approved-date: "2026-04-06"
    adr.sociosphere.io/review-date: "2026-10-06"  # Review in 6 months
spec:
  exceptions:
    - policyName: enforce-pod-security
      ruleNames:
        - deny-privileged-containers
  match:
    any:
      - resources:
          kinds:
            - Pod
          namespaces:
            - sociosphere
          names:
            - my-service-*
```

---

## Monitoring Kyverno

Kyverno exposes Prometheus metrics:

```promql
# Policy admission requests (total)
kyverno_admission_requests_total

# Policy rule results (pass/fail by policy)
kyverno_policy_results_total{rule_result="fail"}

# Webhook latency (should be < 500ms)
kyverno_admission_request_duration_seconds
```

Kyverno violations are surfaced in the **Compliance** Grafana dashboard (`grafana/dashboard-compliance.json`).
