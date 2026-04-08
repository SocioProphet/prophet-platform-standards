# Contributing

Thank you for contributing to the Prophet Platform Standards. This document explains the process for proposing and landing changes.

---

## Code of Conduct

Be respectful, constructive, and patient. This is a collaborative standards effort — disagreement is healthy; disrespect is not.

---

## How to Propose Changes

### For Small Changes (Docs, Typos, Template Fixes)

1. Fork the repository
2. Create a branch: `fix/description-of-change`
3. Make your changes
4. Open a Pull Request with a clear description
5. Await 1 maintainer approval

### For ADRs and Architectural Changes

1. **Open an issue first** to discuss the change before writing an ADR
2. Draft the ADR using the template below
3. Open a PR with the ADR in `adr/`
4. Solicit feedback from maintainers and stakeholders
5. Revise based on feedback
6. Merge with 2 maintainer approvals after the minimum review period (see GOVERNANCE.md)

---

## ADR Template

```markdown
# ADR-XXX: Title

**Status:** Draft | Accepted | Deprecated | Superseded  
**Date:** YYYY-MM-DD  
**Deciders:** <Team names>  
**Tags:** <relevant tags>

---

## Context and Problem Statement

<Describe the context and problem this ADR addresses>

---

## Decision

<State the decision>

### Requirements Language

Per RFC 2119: MUST = mandatory, SHOULD = recommended, MAY = optional

---

## <Component Name> (MUST/SHOULD/MAY)

### Rationale

<Why this approach>

### Requirements

1. <Requirement 1>
2. <Requirement 2>

---

## Options Considered

### Option A: <Name> (Rejected/Accepted/Partially Adopted)
- **Pros:** ...
- **Cons:** ...

---

## Tradeoffs

| Concern | Impact | Mitigation |
|---------|--------|------------|
| | | |

---

## Measurement Plan

| Metric | Target | Collection Method |
|--------|--------|------------------|
| | | |

---

## Consequences

### Positive
- 

### Negative
- 

### Neutral
- 

---

## Related ADRs

- [ADR-XXX](ADR-XXX-title.md)

---

## References

- [Link](URL)
```

---

## Testing Requirements

### Template Changes (YAML)

All YAML templates should be validated before submitting:

```bash
# Validate Kubernetes YAML
kubectl --dry-run=client apply -f tekton/task-build.yaml
kubectl --dry-run=client apply -f rbac/cluster-role-developer.yaml

# Validate Kyverno policies
kyverno apply policies/policy-pod-security.yaml --resource /path/to/test-pod.yaml
```

### Python Instrumentation Files

```bash
# Syntax check
python3 -m py_compile otel/webhook-instrumentation.py
python3 -m py_compile otel/scheduler-instrumentation.py
python3 -m py_compile otel/engine-instrumentation.py
```

### JSON Dashboards

```bash
# Validate JSON syntax
for f in grafana/*.json; do python3 -c "import json; json.load(open('$f'))" && echo "$f: OK"; done
```

---

## Code Review Guidelines

When reviewing a PR:

1. **Correctness**: Does the change do what it says? Are there edge cases?
2. **Consistency**: Does it follow existing patterns and naming conventions?
3. **ADR alignment**: Does it align with existing ADRs? If not, is an ADR amendment needed?
4. **Security**: Does the change introduce any security risks? (Especially for RBAC and policy changes)
5. **Documentation**: Is the change documented? Are guides updated?
6. **Measurement**: Are metrics and measurement plans updated if needed?

---

## Sign-Off Process

By submitting a PR, you certify that:

```
Developer Certificate of Origin v1.1

I certify that:
(a) The contribution was created in whole or in part by me and I have the right to submit it under the Apache 2.0 license; or
(b) The contribution is based upon previous work that I know is covered under an appropriate open source license and I have the right under that license to submit that work with modifications; and
(c) The contribution was provided directly to me by some other person who certified (a) or (b) above.
```

Add a `Signed-off-by` line to your commit messages:
```
git commit -s -m "feat(adr): add ADR-070 for XYZ"
```

---

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
Signed-off-by: Your Name <email@example.com>
```

**Types:**
- `feat` — new ADR, template, or feature
- `fix` — correction to existing content
- `docs` — documentation only
- `refactor` — restructuring without changing meaning
- `security` — security-related fix

**Scopes:** `adr`, `tekton`, `argocd`, `rbac`, `policies`, `otel`, `grafana`, `schemas`, `docs`, `governance`

**Examples:**
```
feat(adr): add ADR-070 for multi-cluster federation
fix(tekton): correct cosign signing step in task-build
docs(rbac): clarify ServiceAccount namespace requirements
security(policies): tighten pod security policy for privileged escalation
```
