# Forensic Genesis Edge Schema Catalog

This directory holds the first-pass JSON Schemas for the Forensic Genesis edge ingress lane.

## Current topic schemas
- `topics/edge.forensic.snmp.observed.v1.schema.json`
- `topics/edge.forensic.mounts.observed.v1.schema.json`
- `topics/edge.forensic.verify.completed.v1.schema.json`
- `topics/edge.forensic.seal.completed.v1.schema.json`

## Design notes
- These schemas describe **edge structural facts**, not higher semantic claims.
- Compatibility should default to a backward-safe policy for additive evolution.
- Topic-specific key construction belongs to the runtime/import layer, not to these value schemas.

## Evolution examples
The `topics/evolution/` directory can carry explicit compatible and incompatible examples for review and registry testing.
