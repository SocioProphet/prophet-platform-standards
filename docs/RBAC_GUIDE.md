# RBAC Guide

Reference guide for understanding, implementing, and auditing the Prophet Platform RBAC model.

RBAC standards are defined in ADR-050.

---

## RBAC Model Overview

The Prophet Platform uses a role-based access control model built on Kubernetes RBAC. All access is controlled through one of four defined personas.

### Persona Definitions

| Persona | ClusterRole | Who Uses It | Key Permissions |
|---------|-------------|-------------|-----------------|
| **Admin** | `prophet-admin` | Cluster operators | Full cluster access |
| **Developer** | `prophet-developer` | App developers | Read pods, logs, events; port-forward |
| **Deployer** | `prophet-deployer` | CI/CD SA, release engineers | Deploy, trigger pipelines, sync ArgoCD |
| **Auditor** | `prophet-auditor` | Compliance team | Read-only: audit, events, deployments |

### Principle of Least Privilege

Every user and workload **MUST** have only the permissions required for their function:
- Developers **cannot** create or delete workloads
- Service accounts **cannot** access secrets outside their own namespace
- No workload service account can be granted `ClusterAdmin`

---

## Granting Roles to Users

### Grant Developer Access

```bash
# Bind a GitHub user to the developer role
kubectl create clusterrolebinding prophet-developer-<USERNAME> \
  --clusterrole=prophet-developer \
  --user=<GITHUB_USERNAME>

# Or bind a GitHub team (if using Dex/OIDC)
kubectl create clusterrolebinding prophet-developer-team \
  --clusterrole=prophet-developer \
  --group=SocioProphet:developers
```

**Then commit the binding to Git:**
```yaml
# rbac/bindings/developer-<USERNAME>.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: prophet-developer-<USERNAME>
  annotations:
    adr.sociosphere.io/reference: "ADR-050"
    rbac.sociosphere.io/granted-by: "<APPROVER>"
    rbac.sociosphere.io/granted-date: "<YYYY-MM-DD>"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prophet-developer
subjects:
  - kind: User
    name: <GITHUB_USERNAME>
    apiGroup: rbac.authorization.k8s.io
```

### Grant Deployer Access (for Humans)

```bash
kubectl create clusterrolebinding prophet-deployer-<USERNAME> \
  --clusterrole=prophet-deployer \
  --user=<GITHUB_USERNAME>
```

Note: The primary deployer is the `tekton-build-sa` ServiceAccount (bound via `rbac/cluster-role-deployer.yaml`).

### Grant Auditor Access

```bash
kubectl create clusterrolebinding prophet-auditor-<USERNAME> \
  --clusterrole=prophet-auditor \
  --user=<AUDITOR_USERNAME>
```

### Grant Admin Access (Requires Security Team Approval)

Admin bindings require documented justification and Security Team approval:

```bash
# ONLY after Security Team approval
kubectl create clusterrolebinding prophet-admin-<USERNAME> \
  --clusterrole=prophet-admin \
  --user=<OPERATOR_USERNAME>
```

Store the binding in Git with justification annotation:
```yaml
annotations:
  rbac.sociosphere.io/justification: "Cluster operator for platform incident response"
  rbac.sociosphere.io/approved-by: "security-team@sociosphere.io"
  rbac.sociosphere.io/approved-date: "2026-04-06"
```

---

## Creating Custom Roles

If the standard personas don't fit your use case, create a custom Role (namespace-scoped, not ClusterRole):

```yaml
# rbac/custom-roles/my-custom-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-custom-role
  namespace: sociosphere
  annotations:
    adr.sociosphere.io/reference: "ADR-050"
    rbac.sociosphere.io/justification: "Custom role for X because standard personas don't cover Y"
    rbac.sociosphere.io/approved-by: "<APPROVER>"
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
    resourceNames:
      - specific-configmap-only
```

**Custom role requirements:**
1. Use `Role` (namespace-scoped) instead of `ClusterRole` unless cluster-level access is genuinely required
2. Document justification in annotations
3. Require Security Team review for any new permissions not in existing personas
4. Store in `rbac/custom-roles/` and apply via GitOps

---

## ServiceAccount Permissions

### ServiceAccount per Workload (MUST)

Every workload deployment **MUST** use a dedicated ServiceAccount:

```yaml
# In your Deployment spec
spec:
  template:
    spec:
      serviceAccountName: my-service-sa
      automountServiceAccountToken: false  # Only enable if needed
```

### Disable Auto-mount by Default

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-sa
  namespace: sociosphere
automountServiceAccountToken: false
```

If your service needs to call the Kubernetes API, explicitly mount the token:

```yaml
volumes:
  - name: service-token
    projected:
      sources:
        - serviceAccountToken:
            expirationSeconds: 3600
            path: token
        - configMap:
            name: kube-root-ca.crt
            items:
              - key: ca.crt
                path: ca.crt
```

---

## Auditing RBAC Access Logs

### Check What a User Can Do

```bash
# List all permissions for a specific user
kubectl auth can-i --list --as=<USERNAME>

# List permissions in a specific namespace
kubectl auth can-i --list --as=<USERNAME> --namespace=sociosphere

# Check a specific permission
kubectl auth can-i create pipelineruns --as=<USERNAME> --namespace=sociosphere
```

### Audit Existing Bindings

```bash
# List all ClusterRoleBindings
kubectl get clusterrolebindings -o wide | grep prophet

# Find who has admin access (should be very few)
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name == "prophet-admin") | {name: .metadata.name, subjects: .subjects}'

# Find all bindings for a specific user
kubectl get clusterrolebindings,rolebindings --all-namespaces -o json | \
  jq --arg user "mdheller" \
  '.items[] | select(.subjects[]? | .name == $user) | {name: .metadata.name, role: .roleRef.name}'
```

### Review ServiceAccount Permissions

```bash
# What can the webhook-sa do?
kubectl auth can-i --list \
  --as=system:serviceaccount:sociosphere:webhook-sa \
  --namespace=sociosphere

# Verify tekton-build-sa can create PipelineRuns
kubectl auth can-i create pipelineruns \
  --as=system:serviceaccount:sociosphere:tekton-build-sa \
  --namespace=sociosphere
```

### Detect Overprivileged Bindings

```bash
# Find any workload ServiceAccounts with ClusterAdmin (should be empty)
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name == "cluster-admin") | 
      select(.subjects[]?.kind == "ServiceAccount") | 
      {binding: .metadata.name, subjects: .subjects}'

# Find any wildcard resource bindings (risky)
kubectl get clusterroles -o json | \
  jq '.items[] | select(.rules[]? | .resources[]? == "*") | .metadata.name'
```

---

## Namespace Isolation Verification

```bash
# Verify sociosphere SA cannot access other namespaces
kubectl auth can-i get pods \
  --as=system:serviceaccount:sociosphere:webhook-sa \
  --namespace=kube-system
# Expected: no

# Verify no cross-namespace secret access
kubectl auth can-i get secrets \
  --as=system:serviceaccount:sociosphere:webhook-sa \
  --namespace=argocd
# Expected: no
```

---

## RBAC Change Process

All RBAC changes **MUST** follow the GitOps process:

1. Create a PR with the proposed RBAC change in `rbac/`
2. Include justification in PR description and annotation
3. Require review from Security Team (`@SocioProphet/security-team`)
4. Auto-applied by ArgoCD after merge — no manual `kubectl apply`
5. Audit event automatically logged when binding is created

See [GOVERNANCE.md](../GOVERNANCE.md) for the full change process.
