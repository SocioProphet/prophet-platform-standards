# Immutable Node Validation Guide

This guide defines the minimum validation posture for the Socios immutable-node tranche.

It exists so the repository stores not only templates, but also the expected checks that keep those templates from drifting into decorative documentation.

---

## Scope

This guide applies to the immutable-node tranche introduced by:

- `adr/ADR-070-immutable-node-host-capability-model.md`
- `docs/HOST_CAPABILITY_MODEL.md`
- `docs/IMMUTABLE_NODE_GUIDE.md`
- `bootc/`
- `quadlet/`
- `systemd/`
- `tmpfiles/`
- `audit/`
- `manifests/immutable-node/`

---

## Validation Objectives

The immutable-node lane SHOULD verify at least the following:

1. required files exist;
2. systemd unit files contain the required sections;
3. Quadlet unit files contain the required sections;
4. manifest files parse as YAML;
5. docs and implementation skeletons remain aligned enough to review coherently.

---

## Minimum Local Checks

### 1. Validate systemd service structure

```bash
for f in systemd/*.service; do
  grep -q '^\[Unit\]' "$f" || { echo "$f missing [Unit]"; exit 1; }
  grep -q '^\[Service\]' "$f" || { echo "$f missing [Service]"; exit 1; }
  grep -q '^\[Install\]' "$f" || { echo "$f missing [Install]"; exit 1; }
done
```

### 2. Validate Quadlet structure

```bash
for f in quadlet/*.container; do
  grep -q '^\[Unit\]' "$f" || { echo "$f missing [Unit]"; exit 1; }
  grep -q '^\[Container\]' "$f" || { echo "$f missing [Container]"; exit 1; }
  grep -q '^\[Service\]' "$f" || { echo "$f missing [Service]"; exit 1; }
  grep -q '^\[Install\]' "$f" || { echo "$f missing [Install]"; exit 1; }
done
```

### 3. Validate YAML syntax

```bash
python3 - <<'PY'
import pathlib, sys, yaml
for path in pathlib.Path('manifests/immutable-node').glob('*.yaml'):
    with open(path, 'r', encoding='utf-8') as fh:
        yaml.safe_load(fh)
    print(f"{path}: OK")
PY
```

### 4. Validate tmpfiles presence

```bash
test -f tmpfiles/socios.conf
```

---

## Review Expectations

Reviewers SHOULD confirm:

1. new immutable-node files are reflected in repository documentation;
2. placeholder image references are clearly marked as placeholders;
3. state roots remain under `/var/lib/socios` rather than drifting into `/etc`;
4. bound services and floating services remain explicitly distinguishable.

---

## Follow-on Hardening

The next validation tranche SHOULD add:

- systemd-analyze verification where available;
- Quadlet-to-generated-unit validation where available;
- stricter schema checks for immutable-node manifests;
- CI wiring for the checks above.
