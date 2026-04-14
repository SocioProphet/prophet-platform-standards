# ADR-080: Role-Based Storage Fabric

## Status
Accepted

## Context

The platform uses multiple kinds of storage work. A single generic persistence model is not sufficient for all workloads.

## Decision

The platform standardizes a role-based storage fabric. The primary roles are:
- state store
- event log
- document store
- cache
- derived graph or search roles

Storage selection is evaluated role by role.

## Consequences

- backend choice is described in terms of role fitness
- selector outputs must remain explainable by role
- executable conformance may differ by backend while the role model stays stable
