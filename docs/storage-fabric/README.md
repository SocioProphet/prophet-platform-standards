# Storage Fabric Standards

This section defines the platform-normative doctrine for workload-shaped storage selection in the SocioProphet stack.

It standardizes:
- the storage role model
- workload-to-topology selection rules
- ranked recommendation semantics
- history-aware threshold and learning policy

These documents are normative platform standards. Executable conformance harnesses, benchmark runners, generated reports, and history fixtures belong in downstream proving repositories and must not be treated as the standards authority.

## Documents

- `role-model-and-backend-roles.md` — canonical storage roles and ownership boundaries
- `topology-selection-and-ranking-policy.md` — profile-based selection and ranking semantics
- `history-threshold-and-learning-policy.md` — noise, effect size, persistence, and long-horizon learning policy

## Repo boundary

This standards subtree defines platform law. It does not define benchmark harness code, integration-matrix execution, or generated benchmark evidence. Those surfaces must consume these standards rather than redefine them.
