# Storage Fabric Role Model and Backend Roles

## Decision posture

The platform must not model persistence as a single interchangeable CRUD backend. Storage selection is workload-shaped and role-based.

Backend choice MUST follow:
- workload shape
- query pattern
- mutability model
- latency envelope
- evidence and recovery requirements
- replication and synchronization needs

Backend choice MUST NOT be justified by vendor fashion or one-size-fits-all preference.

## Canonical storage roles

### State store
Authoritative mutable operational state.

Typical uses:
- request lifecycle state
- current twin or control state
- current materialized control objects

Properties:
- point lookup and update
- transactional integrity where required
- predictable recovery semantics

### Event log
Append-only historical sequence for replay, audit, causality, and reconstruction.

Typical uses:
- lifecycle events
- audit events
- replayable transitions

Properties:
- append-first semantics
- ordering discipline
- replayability
- explicit retention and evidence posture

### Document store
Flexible structural objects where schema evolution and JSON-shaped artifacts dominate.

Typical uses:
- manifests
- reports
- benchmark outputs
- contract or bundle-like artifacts where document shape matters more than relational joins

### Cache
Low-latency non-authoritative access layer.

Typical uses:
- hot-path request lookups
- derived status caches
- short-lived acceleration for read-heavy paths

A cache MUST NOT be treated as the authority layer unless that authority is explicitly modeled elsewhere.

### Graph and search roles
Graph and search layers are derived or specialized roles, not generic replacements for the roles above.

Typical uses:
- topology exploration
- retrieval and ranking support
- semantic or graph-oriented projections

These roles MAY consume outputs from the authoritative layers above, but must not silently replace them.

## Backend-role mapping posture

A single backend MAY implement more than one role, but each use must still be evaluated role-by-role.

Examples:
- SQLite or PostgreSQL may serve as state stores
- Redis may serve as cache
- MongoDB or CouchDB may serve as document stores
- Kafka or an event-native system may serve as event log

The same product name across workloads does not imply the same role fitness.
