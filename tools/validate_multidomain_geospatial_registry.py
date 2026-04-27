#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TOP = [
    "registry_id",
    "version",
    "status",
    "updated_at",
    "standards_authorities",
    "domain_lanes",
    "implementation_consumers",
    "minimum_conformance",
]

REQUIRED_AUTHORITY = ["repo", "authority", "primary_standard", "validation_target"]
REQUIRED_LANES = {
    "geo-platform-parity",
    "earth-observation",
    "space-telemetry",
    "maritime-domain-awareness",
    "air-domain-awareness",
    "defense-public-safety",
    "smart-spaces-built-environment",
    "sensor-fusion",
}
REQUIRED_REPOS = {
    "SocioProphet/prophet-platform-standards",
    "SocioProphet/socioprophet-standards-storage",
    "SocioProphet/socioprophet-standards-knowledge",
    "SocioProphet/socioprophet-agent-standards",
}


def fail(msg: str) -> None:
    print(f"ERR: {msg}", file=sys.stderr)
    raise SystemExit(2)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path}: invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path}: expected top-level object")
    return data


def require_keys(obj: dict, keys: list[str], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        fail(f"{where}: missing required keys: {', '.join(missing)}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = root / "registry/multidomain-geospatial-standards-map.v1.json"
    standard = root / "docs/standards/070-multidomain-geospatial-standards-alignment.md"
    if not registry.exists():
        fail("missing registry/multidomain-geospatial-standards-map.v1.json")
    if not standard.exists():
        fail("missing docs/standards/070-multidomain-geospatial-standards-alignment.md")
    data = load_json(registry)
    require_keys(data, REQUIRED_TOP, "registry")
    authorities = data["standards_authorities"]
    if not isinstance(authorities, list) or not authorities:
        fail("registry.standards_authorities must be a non-empty array")
    repos = set()
    for idx, authority in enumerate(authorities):
        if not isinstance(authority, dict):
            fail(f"registry.standards_authorities[{idx}] must be object")
        require_keys(authority, REQUIRED_AUTHORITY, f"registry.standards_authorities[{idx}]")
        repos.add(authority["repo"])
    missing_repos = sorted(REQUIRED_REPOS - repos)
    if missing_repos:
        fail(f"registry missing standards authority repos: {', '.join(missing_repos)}")
    lanes = set(data["domain_lanes"])
    missing_lanes = sorted(REQUIRED_LANES - lanes)
    if missing_lanes:
        fail(f"registry missing domain lanes: {', '.join(missing_lanes)}")
    conformance = data["minimum_conformance"]
    if not isinstance(conformance, dict):
        fail("registry.minimum_conformance must be object")
    for key, value in conformance.items():
        if not isinstance(value, bool):
            fail(f"registry.minimum_conformance.{key} must be boolean")
    print("OK: multidomain geospatial standards registry is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
