#!/usr/bin/env python3
"""Configurable external-attribution guard.

Usage:
  python tools/check_no_external_attribution.py TERM [TERM ...]

The script intentionally does not embed source-specific blocked terms. Pass terms from CI,
repo settings, or a local invocation.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs" / "NEXT_GEN_TOM_BROKER_DOCTRINE.md",
    ROOT / "docs" / "NEXT_GEN_TOM_SERVICE_PROVIDER_MATRIX.md",
    ROOT / "docs" / "NEXT_GEN_TOM_REFERENCE.md",
    ROOT / "docs" / "NEXT_GEN_TOM_CADENCE_AND_BENEFITS.md",
]


def main(argv: list[str]) -> int:
    terms = argv[1:]
    if not terms:
        print("No attribution terms supplied; nothing to check.")
        return 0

    hits = []
    for path in DOCS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower_text = text.lower()
        for term in terms:
            if term.lower() in lower_text:
                hits.append(f"{path}: contains blocked term")

    if hits:
        print("Blocked attribution terms found:")
        for hit in hits:
            print(f" - {hit}")
        return 1

    print("No blocked attribution terms found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
