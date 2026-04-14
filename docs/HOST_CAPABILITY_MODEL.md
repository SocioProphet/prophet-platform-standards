# Socios Host Capability Model

This guide defines the normative host capability placement model for Socios on immutable Linux systems.

It replaces vague notions of ad hoc control modules with a bounded placement discipline aligned to bootc and OSTree-style transactional hosts.

---

## Purpose

The design goal is straightforward:

> The host program tree is immutable at runtime, configuration is declarative and bounded, and authoritative mutable state is isolated from the image.

This guide defines:

- the deployment classes available to Socios;
- how each class maps to host capabilities;
- where code, configuration, and state must live;
- what may move independently and what must move with the host lifecycle;
- how rollback, staged upgrades, and privileged Linux adapters interact.

---

## Requirements Language

Per RFC 2119:

- **MUST** = mandatory
- **SHOULD** = recommended
- **MAY** = optional

---

## Architectural Axioms

### 1. Immutable Host Axiom

The host operating system tree MUST be delivered as a transactional image deployment and MUST NOT be mutated in steady-state production operation.

### 2. Config and State Separation Axiom

`/etc` MUST be treated as declarative machine-local configuration, not as an authoritative mutable database.

`/var` MUST be treated as the authoritative mutable state surface for Socios.

### 3. Placement Discipline Axiom

Every Socios capability MUST be assigned to exactly one primary placement class:

1. image-baked host capability;
2. sysext host capability;
3. confext policy/config capability;
4. Quadlet-bound service workload;
5. Quadlet-floating service workload;
6. `/var` state object.

A capability MAY depend on adjacent classes, but it MUST have one canonical home.

### 4. Least-Privilege Host Axiom

Socios MUST remain user-space-first. Kernel-adjacent behavior SHOULD prefer established Linux control surfaces such as eBPF, nftables, Linux Audit, systemd, cgroups, namespaces, and standard kernel/user-space IPC over custom kernel modules.

---

## Deployment Classes

### Image-Baked Host Capability

This class is for code and configuration tightly coupled to boot, trust establishment, kernel/runtime compatibility, or the invariant host control plane.

Examples:

- `socios-supervisor`
- `socios-attestor`
- `socios-bpf-loader`
- `socios-netpolicy-renderer`
- `socios-audit-bridge`
- baseline systemd units
- immutable helper binaries under `/usr/libexec/socios/`

Requirements:

- Image-baked capabilities MUST be composed in CI and promoted as part of the host image.
- They MUST NOT be introduced in production through drift-inducing live host mutation.
- They SHOULD be minimal, reviewable, and bounded to host-trust concerns.

### sysext Host Capability

This class is for additive host-level features that extend `/usr` or `/opt` without redefining the base trust envelope.

Examples:

- `socios-observe.sysext`
- `socios-forensics.sysext`
- `socios-dlp.sysext`
- optional hardware or environment-specific inspection packs

Requirements:

- sysext features MUST remain additive.
- A sysext MUST NOT become the hidden canonical home for baseline host trust logic.
- sysext versions SHOULD be promoted through the same review pipeline as the base image.

### confext Policy/Config Capability

This class is for declarative overlays that extend `/etc` and tune site, environment, or compliance posture.

Examples:

- `socios-baseline.confext`
- `socios-fedramp.confext`
- `socios-site-<env>.confext`
- service drop-ins and policy bundles

Requirements:

- confext content MUST remain declarative.
- confext SHOULD prefer drop-ins over whole-file replacement.
- `/etc/socios` MUST NOT become the mutable operational truth database.

### Quadlet-Bound Service Workload

This class is for critical system services that run as containers but are lifecycle-coupled to the host release.

Examples:

- `socios-agentplane.container`
- `socios-evidence.container`
- other mandatory node services whose compatibility must track the host release

Requirements:

- Bound services MUST be defined as system-level Quadlet units.
- Bound services SHOULD be pinned by digest.
- Bound services MUST be reviewed together with host promotions and rollback tests.

### Quadlet-Floating Service Workload

This class is for optional or loosely coupled services that may move independently of the host image.

Examples:

- `socios-model-gateway.container`
- optional enrichers or local model workers
- noncritical adapters and experimental services

Requirements:

- Floating services MAY move independently.
- Floating services MUST declare compatibility with the active host release.
- Auto-update SHOULD be policy-gated rather than blindly timer-driven in governed environments.

### `/var` State Object

This class is for durable mutable state that must survive host upgrades and rollback.

Examples:

- `/var/lib/socios/desired-state`
- `/var/lib/socios/evidence`
- `/var/lib/socios/checkpoints`
- `/var/lib/socios/models`
- rebuildable caches under `/var/cache/socios`

Requirements:

- Authoritative mutable state MUST live under `/var/lib/socios/`.
- `/var` schema and replay compatibility MUST be explicitly versioned.
- Readers SHOULD support N and N-1 generation compatibility where rollback matters.

---

## Canonical Placement Rules

### Rule 1: Boot- and trust-coupled logic goes in the image

If the capability is coupled to boot ordering, kernel/runtime compatibility, trust establishment, or the invariant host control plane, it MUST be image-baked.

### Rule 2: Optional additive host logic goes in sysext

If the capability is host-level but optional and additive, it SHOULD use sysext.

### Rule 3: Declarative site policy goes in confext or `/etc/*.d`

If the capability is environment or policy specific and declarative, it SHOULD live in confext or ordinary drop-ins under `/etc`.

### Rule 4: Most user-space services belong in Quadlet

If the capability is ordinary service logic, it SHOULD run as a Quadlet-managed service workload rather than being baked into the host image.

### Rule 5: Durable mutable truth goes only in `/var`

Authoritative runtime state MUST NOT live in `/usr` and MUST NOT treat `/etc` as an operational database.

---

## Linux Privileged Surfaces

Socios should use existing Linux surfaces rather than inventing a bespoke kernel control fabric.

### eBPF

Preferred for:

- runtime observability;
- selected enforcement hooks;
- kernel/user-space shared maps;
- bounded attach-point policy under review.

### nftables

Preferred for:

- host packet policy realization;
- reviewable ingress and egress control;
- explicit rendered rules from declarative policy.

### Linux Audit

Preferred for:

- compliance-grade watch rules;
- host mutation evidence;
- supporting evidence streams for review and export.

### systemd

Preferred for:

- service lifecycle;
- credentials;
- tmpfiles;
- unit hardening;
- runtime rendering;
- ordered activation.

### Quadlet

Preferred for:

- system-managed containers;
- host-coupled service units;
- reviewable system/service topology.

Custom kernel modules SHOULD be rejected by default unless an exception case is documented and approved.

---

## Reference Filesystem Posture

### Immutable program tree

Examples:

- `/usr/libexec/socios/`
- `/usr/lib/socios/`
- `/usr/lib/systemd/system/`
- `/usr/share/containers/systemd/`
- `/usr/lib/bootc/bound-images.d/`

### Declarative config plane

Examples:

- `/etc/socios/`
- `/etc/containers/systemd/`
- `/etc/systemd/system/*.d/`
- confext overlays

### Durable mutable state

Examples:

- `/var/lib/socios/desired-state`
- `/var/lib/socios/evidence`
- `/var/lib/socios/checkpoints`
- `/var/lib/socios/models`
- `/var/cache/socios/`

### Ephemeral runtime materialization

Examples:

- `/run/socios/rendered`
- `/run/socios/sockets`
- `/run/socios/credentials`
- `/run/socios/network`

---

## Rollout and Rollback Guidance

1. Production hosts MUST use transactional image upgrades.
2. Staged deployment workflows SHOULD be the default upgrade path.
3. Live mutation of `/usr` in production MUST NOT be the default path.
4. Bound service images MUST be reviewed together with host promotions.
5. Floating service promotions MUST be policy-gated.
6. Rollback tests MUST verify both host bootability and state-reader compatibility.

---

## Minimum Review Checklist

Before a new capability lands, reviewers SHOULD be able to answer:

1. What is the capability’s canonical placement class?
2. Why does that class fit better than the alternatives?
3. Does the capability mutate `/etc` or `/var`, and if so under what rules?
4. Is the capability host-critical or service-level?
5. What happens during rollback?
6. What evidence surfaces or policy gates are required?

---

## Companion Documents

- `adr/ADR-070-immutable-node-host-capability-model.md`
- `docs/IMMUTABLE_NODE_GUIDE.md`
