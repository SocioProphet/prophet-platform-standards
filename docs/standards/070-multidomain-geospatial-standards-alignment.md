# 070 — Multi-Domain Geospatial Standards Alignment

Status: Draft v0.1
Scope: GAIA / Prophet Platform / SocioSphere / Sherlock / Agentplane / Lattice Forge

## Purpose

This standard defines where multi-domain geospatial intelligence specifications belong across the SocioProphet standards repositories and implementation repositories.

The platform must not scatter normative contracts directly into implementation repos without a standards authority. Implementation repos may contain adapters, fixtures, examples, and runtime proofs, but reusable schemas, compatibility rules, and governance semantics must originate from the appropriate standards repository.

## Normative repository ownership

| Concern | Standards authority | Implementation consumers |
| --- | --- | --- |
| Platform product requirements, acceptance gates, CI/CD, observability, deployment and API posture | `SocioProphet/prophet-platform-standards` | `SocioProphet/prophet-platform`, `SocioProphet/sociosphere`, `SocioProphet/sherlock-search` |
| Storage contracts, event streams, analytics payloads, benchmark methodology, FIPS/NIST/data-layer governance | `SocioProphet/socioprophet-standards-storage` | GAIA ingest/catalog/query repos, storage engines, Sherlock, SocioSphere |
| Knowledge context, ontology, provenance, JSON-LD, meriotopographics, evidence/claim/annotation semantics | `SocioProphet/socioprophet-standards-knowledge` | `prophet-domain-gaia-ontology`, `gaia-world-model`, Sherlock, knowledge services |
| Agent execution, approval gates, runtime evidence, replay, conformance, SourceOS/AgentOS compatibility | `SocioProphet/socioprophet-agent-standards` | `SocioProphet/agentplane`, `SocioProphet/lattice-forge`, SourceOS repos |
| GAIA domain contracts and fixtures after standards are defined | Standards above plus GAIA domain repos | `prophet-core-contracts`, `prophet-core-ingest`, `prophet-core-catalog`, `prophet-core-query`, `prophet-core-policy`, `prophet-domain-gaia-ontology`, `gaia-world-model` |

## Multi-domain standards lanes

The following lanes are now in-scope for the platform standards surface.

1. `geo-platform-parity`: ESRI, OGC, Google Maps-like, Google Earth-like, OSM, MapLibre, 3D Tiles/I3S/KML/KMZ compatibility requirements.
2. `earth-observation`: STAC, COG, Zarr, NetCDF, SAR, optical, thermal, hyperspectral, RF-derived products, ML labels, confidence metadata.
3. `space-telemetry`: satellite assets, constellations, ephemerides, ground station contacts, spacecraft telemetry, command events, mission timeline, anomaly events.
4. `maritime-domain-awareness`: AIS, LRIT-authorized data, vessel tracks, ports, terminals, shipping lanes, cargo/risk events, sea-state/weather overlays.
5. `air-domain-awareness`: ADS-B, airports, airspace, drones, NOTAM-like events, aviation weather, emergency corridors.
6. `defense-public-safety`: authorized defense, humanitarian, disaster response, sensitive-site masking, redaction, role controls, source protection.
7. `smart-spaces-built-environment`: indoor/campus/facility maps, sensors, rooms, floors, assets, occupancy, accessibility, smart-city interfaces.
8. `sensor-fusion`: SensorThings/STAplus, SOSA/SSN, OSM, STAC, AIS/LRIT/ADS-B, CCSDS-like telemetry, field observations, and provenance fusion.

## Placement rule

A new multi-domain geospatial spec MUST be placed as follows:

- Product acceptance, user/API surface, dashboard, deployment, CI/CD, observability, and release gates go here in `prophet-platform-standards`.
- Data model, file/event/stream payload, storage benchmark, FIPS/NIST, and retention standards go to `socioprophet-standards-storage`.
- Ontology, JSON-LD, provenance, claim/evidence semantics, entity-resolution, masking semantics, and meriotopographic relations go to `socioprophet-standards-knowledge`.
- Agent/runtime execution policy, approval gates, runtime replay, evidence bundles, and conformance rules go to `socioprophet-agent-standards`.
- Implementation repos consume standards and may add examples, validators, adapters, and runtime boundary proofs.

## Safety boundary

Defense and public-safety geospatial support MUST be policy-gated. The platform may support authorized customer-owned, public, humanitarian, disaster-response, compliance, logistics, infrastructure, and training data. It MUST NOT define ungoverned targeting, evasion, or sensitive-site exploitation workflows as open runtime capabilities.

## Minimum implementation cross-reference

Every implementation repo that consumes this standard MUST add a `Complies with Standards` section linking to this file and the relevant storage, knowledge, and agent standards documents.
