# ADR-071: Guideplane operator workbench

## Status

Draft

## Decision

Guideplane is a platform operator-workbench standard.

It belongs in `prophet-platform-standards` because it defines a platform-level operating surface, not an agent persona, runtime implementation, ontology, execution engine, or workspace registry.

## Scope

Guideplane defines the visible operator planes for:

- navigation
- qualification
- fulfillment
- explanation
- outcome review

Guideplane consumes surrounding standards and contracts instead of replacing them.

## Repository boundaries

- Agent conformance belongs in `socioprophet-agent-standards`.
- Runtime consumption belongs in `prophet-platform`.
- Semantic mapping belongs in `ontogenesis`.
- Execution evidence belongs in `agentplane`.
- Policy verdict binding belongs in `policy-fabric`.
- Workspace topology belongs in `sociosphere`.

## Consequence

This ADR supersedes the earlier monolithic Guideplane landing attempt. Future Guideplane work should land as split, reviewable PRs across the correct repo lanes.
