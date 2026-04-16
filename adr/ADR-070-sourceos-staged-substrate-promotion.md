# ADR-070: SourceOS staged substrate promotion

## Status
Draft

## Context

We are introducing a workstation and edge substrate lane where a Fedora Asahi host carries a staged Nix control plane. This creates a promotion problem that is more sensitive than ordinary application deployment because it crosses:

- host-level substrate state,
- user-space control-plane state,
- rootless container/runtime state,
- storage and snapshot policy,
- boot-sensitive operational surfaces.

Existing rollout guidance covers general CI/CD and deployment patterns, but this lane needs an explicit staged-substrate rule set.

## Decision

For SourceOS substrate lanes, promotion MUST be staged before host activation.

### Mandatory gates

1. **Stage gate required**
   - A candidate must be built and exercised in an isolated stage lane before promotion.

2. **Evidence required**
   - Stage, promote, rollback, and post-activation health events must emit evidence artifacts.

3. **Explicit rollback strategy required**
   - Every substrate lane must declare rollback behavior at the relevant layers:
     - generation rollback,
     - image rollback,
     - snapshot rollback,
     - or a declared multi-layer combination.

4. **Human approval required for host-sensitive promotions**
   - If a lane is marked boot-sensitive or substrate-sensitive, promotion requires human approval.

5. **Immutable input / mutable state separation required**
   - Promotion must not collapse immutable config inputs and mutable runtime state into one undifferentiated mount or artifact surface.

## Consequences

### Positive

- reduces risk of bricking or destabilizing workstation substrates,
- keeps promotion auditable,
- aligns rollout policy with evidence-first governance.

### Costs

- more friction than direct host mutation,
- additional stage infrastructure and smoke validation work,
- more artifacts to retain and reason about.

## Required downstream alignment

- `SociOS-Linux/SourceOS` implements the substrate mechanics.
- `SourceOS-Linux/sourceos-spec` defines the typed boot/storage/staged-deployment contracts.
- `SociOS-Linux/workstation-contracts` defines conformance for the lane.
- `SocioProphet/agentplane` executes the stage bundle and emits evidence.

## Acceptance rule

A SourceOS substrate lane is non-compliant if it promotes directly to the host without a declared stage gate and explicit rollback strategy.
