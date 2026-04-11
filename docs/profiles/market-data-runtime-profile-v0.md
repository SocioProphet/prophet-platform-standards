# Market Data Runtime Profile v0

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | v0 |
| Canonical runtime profile authority | `SocioProphet/prophet-platform-standards` |
| Canonical storage and contract authority | `SocioProphet/socioprophet-standards-storage` |
| Primary runtime consumer | `SocioProphet/prophet-platform` |
| Workspace governance surface | `SocioProphet/sociosphere` |
| Change class | Profile-layer constraint, not root storage authority |

## 1. Purpose

This document defines a **market data runtime profile** for platform services that ingest,
normalize, replay, store, and serve financial market data. It is intentionally scoped as a
**runtime profile** and **MUST NOT** be treated as a competing storage standard.

The storage contexts, canonical format choices, and baseline service posture remain anchored in
`SocioProphet/socioprophet-standards-storage`. This profile narrows those upstream standards for
market-data workloads and adds domain-specific invariants for determinism, replayability,
entitlements, lineage, and operator evidence.

## 2. Authority split

### 2.1 Non-negotiable authority rule

This profile **MUST** defer the following to `socioprophet-standards-storage`:

- storage context taxonomy
- canonical storage mappings
- data contract format families
- service-interface baseline expectations
- benchmark posture and workload-triggered store adoption rules

This profile **MAY** add stricter runtime rules for market-data services, but it **MUST NOT**
redefine the upstream storage contexts or create a second source of truth for storage semantics.

### 2.2 What this profile is allowed to define

This profile is allowed to define:

- market-data object classes and their runtime handling rules
- event-topic conventions for market-data flows
- determinism and replay constraints
- entitlement propagation rules
- lineage and audit evidence requirements
- market-data-specific benchmark gates and operational SLO targets

## 3. Scope

The profile applies to services handling any of the following object classes:

- `Instrument`
- `Venue`
- `TradingSession`
- `EntitlementGrant`
- `VendorFeedBinding`
- `CorporateAction`
- `Quote`
- `Trade`
- `Bar`
- `BookDelta`
- `Snapshot`
- `ReplayRequest`
- `ReplayReceipt`
- `GapAlert`
- `NormalizationReceipt`
- `DerivedIndicator`

## 4. Canonical domain split

### 4.1 Reference domain

The following are **reference-domain** objects:

- instruments
- venues
- trading calendars and session definitions
- symbol maps and vendor identifiers
- entitlement grants
- corporate actions

These objects are mutable over time and **MUST** be handled as governed reference state.

### 4.2 Event domain

The following are **event-domain** objects:

- quotes
- trades
- order-book deltas
- bar-close emissions
- snapshots
- normalization receipts
- replay receipts
- gap alerts

These objects are append-only and **MUST** preserve original event identity and ordering evidence.

### 4.3 Derived domain

The following are **derived-domain** objects:

- aggregated bars
- adjusted bars
- indicators
- signals produced from upstream market events

Derived objects **MUST** preserve explicit lineage to the exact upstream raw or normalized events
used to produce them.

## 5. Mapping to upstream storage contexts

This profile reuses the upstream storage-context taxonomy and constrains it as follows.

### 5.1 Event stream (hot path)

The event-stream context **MUST** carry append-only flows for:

- `Quote`
- `Trade`
- `BookDelta`
- `Snapshot`
- `Bar` close notifications
- `GapAlert`
- `NormalizationReceipt`
- `ReplayReceipt`

Raw feed events and normalized events **MUST** be separable by topic namespace and version.

### 5.2 Incident state / system of record

The system-of-record context **MUST** contain:

- instrument master and symbol registry state
- vendor feed configuration
- entitlements and access controls
- replay job state
- operator approvals and exception records
- policy and audit references for market-data service operation

### 5.3 Domain documents

The domain-document context **SHOULD** contain:

- feed adapter configs
- venue/session calendars
- field-mapping rules
- survivorship and symbol-roll policies
- vendor onboarding notes and operating runbooks

### 5.4 Artifacts

The artifacts context **MUST** contain large immutable payloads such as:

- raw vendor capture files
- pcap or binary feed captures
- parquet backfill shards
- columnar extracts
- signed proof bundles
- replay result packages

Raw binaries **MUST NOT** be stored inside relational blobs except for tiny control-plane payloads.

### 5.5 Search

The search context **SHOULD** support:

- instrument metadata lookup
- symbol and alias search
- replay/audit bundle discovery
- operator investigation of gaps and late events

### 5.6 Vectors

The vector context is **OFF by default** for this profile.

Vector indexing **MAY** be adopted only when benchmarked workloads justify it, such as semantic
search over issuer metadata, filings, commentary, or research notes. It **MUST NOT** be required
for canonical trade, quote, bar, or entitlement processing.

### 5.7 Graphs

The graph context **SHOULD** capture:

- vendor → adapter → normalized event lineage
- instrument crosswalks across vendors and internal identifiers
- corporate-action dependency links
- replay provenance and derived-indicator lineage
- operator decision and policy edges for market-data exceptions

### 5.8 Metrics / time series

The metrics context **MUST** track:

- ingest latency
- normalization latency
- end-to-end publication latency
- sequence-gap rate
- out-of-order event rate
- staleness by symbol / venue / feed
- replay throughput
- adjustment drift between raw and adjusted outputs

## 6. Canonical object rules

### 6.1 Instrument identity

An `Instrument` **MUST** have a stable internal identifier separate from vendor identifiers.
Vendor symbology **MUST** be modeled as mapped aliases, not as the canonical identity.

### 6.2 Venue identity

A `Venue` **MUST** be explicit on every event when venue semantics are meaningful.
Synthetic or consolidated events **MUST** declare their consolidation source.

### 6.3 Raw versus normalized distinction

Raw events and normalized events **MUST** be distinguishable at both schema and topic level.
A normalized event **MUST** preserve a reference to the exact raw source event or source batch.

### 6.4 Bar derivation

A `Bar` **MUST** declare:

- interval
- session alignment rule
- timezone/session reference
- derivation source set (`trade`, `quote`, or mixed)
- adjustment posture (`raw`, `split_adjusted`, `fully_adjusted`, etc.)

### 6.5 Corporate actions

Corporate actions **MUST NOT** mutate raw historical trades or raw historical quotes.
They **MAY** affect derived bars or downstream adjusted analytics, but the adjustment policy
**MUST** be explicit and replayable.

## 7. Timestamp, ordering, and determinism

### 7.1 Timestamp posture

Every event **MUST** carry:

- source event timestamp
- ingest timestamp
- normalization timestamp when applicable
- a declared timezone posture of UTC for canonical persisted timestamps

If nanosecond precision is not available, the service **MUST** preserve the highest available
source precision and declare the precision downgrade explicitly.

### 7.2 Ordering posture

Event identity **MUST** preserve enough information to reconstruct vendor ordering semantics,
including sequence number, batch position, or equivalent ordering evidence when available.

### 7.3 Deterministic replay

Given the same raw inputs, session calendar, mapping rules, entitlement posture, and adjustment
policy, normalized market-data outputs **MUST** be replayable deterministically.

### 7.4 Late and out-of-order data

Late and out-of-order events **MUST NOT** be silently dropped. The runtime **MUST** either:

- merge them under a declared lateness rule,
- quarantine them for review,
- or emit an explicit gap / correction event.

## 8. Topic conventions

The following topic families are RECOMMENDED for async event flows:

- `marketdata.raw.quote.v1`
- `marketdata.raw.trade.v1`
- `marketdata.raw.book_delta.v1`
- `marketdata.norm.quote.v1`
- `marketdata.norm.trade.v1`
- `marketdata.bar.1m.v1`
- `marketdata.bar.5m.v1`
- `marketdata.bar.1d.v1`
- `marketdata.ref.instrument.v1`
- `marketdata.ref.corporate_action.v1`
- `marketdata.audit.replay.v1`
- `marketdata.audit.gap_alert.v1`

Raw and normalized topic families **MUST NOT** be collapsed into a single undifferentiated stream.

## 9. Entitlements and policy propagation

### 9.1 Entitlement carriage

Any event or artifact subject to vendor or tenant restrictions **MUST** carry an entitlement or
policy reference sufficient to enforce downstream access decisions.

### 9.2 No silent declassification

A service **MUST NOT** publish restricted market data into a less restrictive topic, cache,
artifact store, or derived output without an explicit policy decision and evidence receipt.

### 9.3 Derived-output inheritance

Derived outputs **MUST** inherit the strictest applicable entitlement posture of their upstream
inputs unless a stricter policy layer overrides it.

## 10. Evidence and audit requirements

Every market-data service conforming to this profile **MUST** emit evidence for:

- feed binding and vendor source
- normalization rule version
- session/calendar version
- entitlement posture used during emission
- replay input set and replay output hash
- gap detection events and operator actions
- derived output lineage

Evidence receipts **SHOULD** be exportable as signed proof bundles.

## 11. Benchmark gates

Before adopting optional stores or relaxing defaults, the following benchmark classes **SHOULD**
be measured for representative workloads:

- hot-path quote/trade ingest latency
- backfill throughput on multi-day or multi-symbol replays
- symbol lookup latency under alias-heavy reference maps
- gap-detection false-positive / false-negative rates
- replay determinism under raw + normalized comparison
- adjusted-bar regeneration cost after corporate-action updates

Optional vector or graph adoption **MUST** remain workload-triggered rather than assumed.

## 12. Exclusions

This profile does not standardize:

- trading strategy semantics
- portfolio accounting
- risk engines
- order routing or execution control
- proprietary vendor licensing terms beyond entitlement propagation requirements

Those may build on top of this profile, but they are outside this document’s scope.

## 13. Minimal conformance statement

A service claiming conformance to this profile **MUST** be able to state all of the following:

1. which upstream storage standard version it inherits from
2. which market-data object classes it handles
3. how it separates raw from normalized events
4. how it preserves ordering and sequence evidence
5. how it performs deterministic replay
6. how it propagates entitlements
7. what evidence bundle it emits for replay and corrections

## 14. Implementation note for downstream repos

- `prophet-platform` should consume this profile through its standards lock.
- `sociosphere` should register the authority chain for `standards/market-data`.
- `socioprophet-standards-storage` remains the root authority for storage contexts,
  data-format families, and benchmark posture.
