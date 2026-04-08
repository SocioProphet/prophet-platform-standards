# Governance

This document describes how the Prophet Platform Standards repository is governed.

---

## Overview

This repository contains the canonical DevSecOps, CI/CD, and Observability standards for the SocioProphet platform. Changes to this repository affect all services in the SocioProphet ecosystem and must follow a deliberate review process.

---

## Change Process

### Proposing a Change

1. **Open an issue** describing the proposed change, the problem it solves, and any tradeoffs.
2. **Draft an ADR** (or ADR amendment) if the change affects an architectural decision. Use the template in [CONTRIBUTING.md](CONTRIBUTING.md).
3. **Open a Pull Request** referencing the issue and ADR.
4. **Assign reviewers** from the maintainers list.

### Review Requirements

| Change Type | Required Approvals | Minimum Review Period |
|-------------|-------------------|----------------------|
| New ADR | 2 maintainers | 5 business days |
| ADR amendment | 2 maintainers | 3 business days |
| New template (non-breaking) | 1 maintainer | 2 business days |
| Documentation | 1 maintainer | 1 business day |
| Security fix | 2 maintainers + Security Team | Expedited (24h) |
| Breaking change | 2 maintainers + 1 stakeholder | 10 business days |

### Merge Criteria

A PR may be merged when:
1. All required approvals are obtained
2. Minimum review period has elapsed
3. All CI checks pass
4. No unresolved blocking comments

---

## Versioning

This repository uses **semantic versioning** (`major.minor.patch`):

| Version Increment | When to Use |
|-------------------|-------------|
| **Major** (v2.0) | Breaking changes: new mandatory RBAC model, removed templates, incompatible schema changes |
| **Minor** (v1.1) | Additive changes: new optional templates, new ADRs, new documentation |
| **Patch** (v1.0.1) | Fixes: typos, clarifications, non-breaking template corrections |

### Deprecation Policy

- Breaking changes **MUST** be announced via a GitHub issue at least **6 months** before taking effect.
- Deprecated items are marked with a `DEPRECATED` notice in the relevant file.
- Deprecated items are removed in the next major version.
- A migration guide **MUST** be provided for every breaking change.

---

## Maintainers

Maintainers have merge rights and are responsible for upholding these governance standards.

Current maintainers:
- [@mdheller](https://github.com/mdheller) — Platform Engineering Lead

To become a maintainer:
1. Be an active contributor for at least 3 months
2. Have at least 5 merged PRs
3. Be nominated by an existing maintainer
4. Approved by majority vote of existing maintainers

---

## Escalation Path

For disputes that cannot be resolved in PR review:

1. **Async discussion**: Open a GitHub Discussion in this repository.
2. **Synchronous review**: Request a platform architecture review meeting (open issue with `agenda` label).
3. **Final decision**: Platform Engineering Lead has final authority on technical matters; Security Team on security matters.

---

## Security Vulnerabilities

Do **not** open a public issue for security vulnerabilities. Instead:
- Email `security@sociosphere.io` with details
- Allow 72 hours for acknowledgment
- Coordinate disclosure timeline with the security team

---

## License

All content in this repository is licensed under [Apache 2.0](LICENSE).

Contributions are accepted under the same license. By submitting a PR, you certify that your contribution is your original work and you have the right to license it under Apache 2.0.
