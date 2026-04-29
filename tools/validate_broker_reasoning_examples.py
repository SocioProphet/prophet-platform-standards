#!/usr/bin/env python3
"""Validate broker reasoning examples against their JSON Schemas."""

from __future__ import annotations

from pathlib import Path
import json

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    (
        ROOT / "schemas" / "broker-reasoning" / "provider-binding-selected-event.schema.json",
        ROOT / "examples" / "broker-reasoning" / "provider-binding-selected-event.example.json",
    ),
    (
        ROOT / "schemas" / "broker-reasoning" / "provider-binding-recommendation.schema.json",
        ROOT / "examples" / "broker-reasoning" / "provider-binding-recommendation.example.json",
    ),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_pair(schema_path: Path, example_path: Path) -> list[str]:
    errors: list[str] = []
    if not schema_path.exists():
        return [f"Missing schema: {schema_path}"]
    if not example_path.exists():
        return [f"Missing example: {example_path}"]

    schema = load_json(schema_path)
    example = load_json(example_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(example), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{example_path}: {location}: {error.message}")
    return errors


def main() -> int:
    failures: list[str] = []
    for schema_path, example_path in CASES:
        failures.extend(validate_pair(schema_path, example_path))

    if failures:
        print("Broker reasoning validation failed:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("Broker reasoning examples validate against their schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
