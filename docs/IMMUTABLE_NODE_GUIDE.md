# Socios Immutable Node Guide

This guide defines the reference immutable-node posture for Socios on bootc-first, OSTree-compatible Linux systems.

It is the concrete companion to `docs/HOST_CAPABILITY_MODEL.md` and turns the placement model into a reference node profile with files, services, state roots, and rollout rules.

---

## Scope

This guide covers:

- base host layout;
- host services that belong in the image;
- Quadlet workloads split into bound and floating lanes;
- state roots under `/var/lib/socios`;
- runtime rendering under `/run`;
- rollback and upgrade expectations.

It does not define application-specific logic, service APIs, or final image names for all future node roles.

---

## Reference Node Planes

### 1. Host Trust Plane

This plane contains image-baked code and units that are required for invariant node behavior.

Examples:

- `socios-render-config.service`
- `socios-bpf-loader.service`
- `socios-supervisor.service`
- immutable helpers under `/usr/libexec/socios/`
- BPF objects under `/usr/lib/socios/bpf/`

Requirements:

- The host trust plane MUST be image-baked.
- It MUST move with the host lifecycle.
- It MUST be small enough to review and test coherently.

### 2. Host Extension Plane

This plane contains additive host-level features and environment policy overlays.

Examples:

- sysext bundles for optional observability or forensic features
- confext bundles for site policy or compliance overlays
- drop-ins under `/etc/*.d`

Requirements:

- Extensions MUST remain additive.
- Extensions MUST NOT become the hidden canonical home for baseline host trust logic.

### 3. Service Plane

This plane contains system-managed container workloads expressed through Quadlet.

#### Bound services

These are critical services that track the host lifecycle.

Examples:

- `socios-agentplane.container`
- `socios-evidence.container`

#### Floating services

These are optional or independently promoted services.

Examples:

- `socios-model-gateway.container`
- optional enrichers and experimental services

Requirements:

- Critical services SHOULD be bound to the host lifecycle.
- Floating services MUST declare compatibility with the active host release.

### 4. State Plane

This plane contains durable mutable state and caches.

Examples:

- `/var/lib/socios/desired-state`
- `/var/lib/socios/evidence`
- `/var/lib/socios/checkpoints`
- `/var/lib/socios/models`
- `/var/cache/socios/*`

Requirements:

- Authoritative mutable truth MUST live under `/var/lib/socios/`.
- State schema compatibility MUST be explicit.

---

## Reference Filesystem Layout

```text
/usr/libexec/socios/
  supervisor
  render-config
  bpf-loader
  attestor

/usr/lib/socios/
  bpf/
    exec_guard.bpf.o
    net_observe.bpf.o
    fs_watch.bpf.o

/usr/lib/systemd/system/
  socios-render-config.service
  socios-bpf-loader.service
  socios-supervisor.service

/usr/share/containers/systemd/
  socios-agentplane.container
  socios-evidence.container
  socios-model-gateway.container

/usr/lib/bootc/bound-images.d/
  socios-agentplane.container
  socios-evidence.container

/etc/socios/
  config.d/
  policy.d/
  node.d/

/var/lib/socios/
  desired-state/
  evidence/
  queue/
  index/
  replay/
  checkpoints/
  models/

/var/cache/socios/
  pulls/
  embeddings/
  model-downloads/

/run/socios/
  rendered/
  sockets/
  credentials/
  network/
```

This layout is normative in spirit even where exact file names may evolve.

---

## Reference Host Services

### `socios-render-config.service`

Purpose:

- render declarative desired state plus machine-local config into runtime material under `/run/socios/rendered`.

Requirements:

- MUST run before dependent host services.
- MUST treat `/var/lib/socios/desired-state` as the durable truth source.
- MUST treat `/etc/socios` as declarative input, not mutable truth.

### `socios-bpf-loader.service`

Purpose:

- load and attach reviewed BPF objects according to rendered policy.

Requirements:

- MUST read immutable BPF objects from `/usr/lib/socios/bpf/`.
- MUST read runtime policy from `/run/socios/rendered/`.
- SHOULD run as a bounded privileged service with explicit capabilities.

### `socios-supervisor.service`

Purpose:

- supervise host-local control flow, evidence emission, health surfaces, and orchestration handoff.

Requirements:

- MUST start after runtime config render.
- MUST use hardened unit defaults.
- SHOULD own the node-local control socket and status surface.

---

## Reference Quadlet Workloads

### `socios-agentplane.container`

Role: critical bound control-plane service.

Requirements:

- SHOULD be digest-pinned.
- SHOULD run with read-only rootfs.
- MUST mount only the state roots and runtime material it needs.

### `socios-evidence.container`

Role: critical bound evidence concentrator or exporter.

Requirements:

- SHOULD be digest-pinned.
- MUST have access to evidence roots and rendered runtime config.
- MUST participate in rollback and compatibility testing.

### `socios-model-gateway.container`

Role: optional floating workload for local model serving or model access mediation.

Requirements:

- MAY move independently.
- MUST declare compatibility with the active host release.
- SHOULD use policy-gated update flow rather than blind timer-driven rollout.

---

## State Schema Expectations

The immutable node MUST define explicit expectations for at least these roots:

- `/var/lib/socios/desired-state` → durable declarative truth
- `/var/lib/socios/evidence` → append-only evidence journal
- `/var/lib/socios/checkpoints` → replay and restore checkpoints
- `/var/lib/socios/models` → rebuildable or replaceable model artifacts

General rules:

1. State readers SHOULD support N and N-1 generation compatibility where rollback matters.
2. Append-only evidence roots SHOULD preserve monotonic sequencing.
3. Desired-state roots SHOULD require auditable writes.
4. `/etc/socios` MUST NOT be treated as the authoritative state database.

---

## Upgrade and Rollback Posture

### Host upgrades

- MUST use transactional image upgrades.
- SHOULD use staged deployment flows by default.
- MUST NOT rely on live mutation of `/usr` as the production baseline.

### Bound service upgrades

- SHOULD be reviewed together with host upgrades.
- MUST be included in rollback testing.
- SHOULD use digest-pinned references.

### Floating service upgrades

- MAY be promoted independently.
- MUST be compatibility-gated.
- SHOULD be visible to policy and evidence surfaces.

### Rollback tests

A rollback test SHOULD verify:

1. the host still boots;
2. runtime rendering still succeeds;
3. critical services still start;
4. durable state readers still function;
5. evidence emission remains coherent.

---

## Minimum Acceptance Criteria

An implementation claiming conformance to this guide SHOULD be able to answer all of the following:

1. Which host services are image-baked and why?
2. Which services are bound vs floating and why?
3. What are the durable state roots under `/var/lib/socios/`?
4. What renders runtime config into `/run/socios/rendered`?
5. What is the rollback compatibility policy for durable state?
6. Which Linux privileged surfaces are used and why?

---

## Companion Files

The reference implementation skeleton for this guide is expected to include:

- `bootc/Containerfile.example`
- `bootc/README.md`
- `quadlet/*.container`
- `systemd/*.service`
- `tmpfiles/socios.conf`
- `nftables/socios-default.nft`
- `audit/80-socios.rules`
- `manifests/immutable-node/profile.yaml`
- `manifests/immutable-node/state-schema.yaml`
