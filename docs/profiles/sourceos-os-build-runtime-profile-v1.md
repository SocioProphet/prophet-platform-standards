# SourceOS OS Build Runtime Profile v1

| Field | Value |
| --- | --- |
| Status | Draft |
| Version | v1 |
| Canonical contract authority | `SourceOS-Linux/sourceos-spec` |
| Platform interpretation authority | `SocioProphet/prophet-platform-standards` |
| Primary runtime consumer | `SocioProphet/prophet-platform` |
| Primary runtime enforcement surface | `SocioProphet/agentplane` |
| Policy / release-gate surface | `SocioProphet/policy-fabric` |
| Change class | Additive runtime profile layered on upstream contract authority |

## 1. Purpose

This document defines how the SocioProphet platform consumes the SourceOS OS-build contract seam:

- `OSImage`
- `NodeBinding`
- `CyberneticAssignment`

It is a **runtime interpretation profile**, not a competing schema authority.

## 2. Non-negotiable authority split

### 2.1 Upstream authority

`SourceOS-Linux/sourceos-spec` remains authoritative for:

- schema names
- URN patterns
- required fields and object semantics
- additive vs breaking contract evolution

### 2.2 This profile may define

This profile may define:

- platform rollout expectations
- release-gate posture
- policy examples for boundary enforcement
- runtime consumer expectations in `prophet-platform` and `agentplane`
- observability and evidence expectations

## 3. Object interpretation

### 3.1 `OSImage`

`OSImage` is an immutable substrate artifact.

It SHOULD carry:

- `os-release` identity
- OCI image metadata
- boot/update posture
- attestation/provenance references
- substrate capability declarations

It MUST NOT carry:

- `deployment.environment.name`
- runtime service names
- site/customer identifiers
- cybernetic role words
- control objectives

### 3.2 `NodeBinding`

`NodeBinding` is the install/enrollment assignment object.

It SHOULD carry:

- topology or region
- fleet
- update ring
- installer profile
- registry mirror refs
- bootstrap trust roots

It MUST NOT redefine immutable image identity.

### 3.3 `CyberneticAssignment`

`CyberneticAssignment` is the runtime semantic layer.

It SHOULD carry:

- service identity
- deployment environment projection
- policy refs
- graph relations
- control profile refs
- objectives

It MUST NOT redefine immutable OS image identity.

## 4. Platform lifecycle mapping

| Lifecycle phase | Primary object | Primary repository surface |
| --- | --- | --- |
| image build and publication | `OSImage` | SourceOS build lanes / `prophet-platform` consumers |
| install / enrollment | `NodeBinding` | installer + enrollment surfaces |
| runtime activation | `CyberneticAssignment` | `agentplane` + runtime apps |
| release evidence / review | all three linked together | `policy-fabric` + `prophet-platform` |

## 5. Policy and validation expectations

The platform SHOULD implement denylist validation that rejects:

- environment strings inside immutable image IDs
- topology strings inside immutable image IDs
- runtime-role words inside immutable image IDs
- runtime service identity inside `OSImage`
- substrate-only fields appearing in `CyberneticAssignment`

## 6. Observability expectations

The OTEL identity split SHOULD align as follows:

- immutable image identity is tracked through `OSImage`
- install/enrollment drift is tracked through `NodeBinding`
- runtime service identity and environment are tracked through `CyberneticAssignment`

This preserves the difference between substrate drift and runtime semantic drift.

## 7. Release expectations

A platform release adopting this profile SHOULD include evidence proving:

1. the image matches the declared `OSImage`
2. the node assignment matches the declared `NodeBinding`
3. the runtime environment and policy posture match the declared `CyberneticAssignment`

## 8. Downstream consumers

- `SocioProphet/policy-fabric` should carry the corresponding release-gate tranche
- `SocioProphet/agentplane` should validate and emit evidence against the runtime seam
- `SocioProphet/prophet-platform` should pin the upstream contract release and consume generated artifacts through `standards.lock.yaml`
