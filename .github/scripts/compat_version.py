#!/usr/bin/env python3
"""Stamp the lancedb python crate version with a +compat local version.

maturin reads the wheel version from python/Cargo.toml (pyproject marks it
dynamic). Cargo needs valid semver, so we append the `+compat` build-metadata
to the existing version (e.g. 0.34.0-beta.3 -> 0.34.0-beta.3+compat). maturin
renders that as the PEP 440 wheel version 0.34.0b3+compat. Idempotent.
"""
import os
import re
import sys
from pathlib import Path

CARGO = Path("python/Cargo.toml")


def pep440(base: str) -> str:
    """Convert a Cargo semver pre-release to its PEP 440 form (maturin's mapping)."""
    base = re.sub(r"-alpha\.(\d+)", r"a\1", base)
    base = re.sub(r"-beta\.(\d+)", r"b\1", base)
    base = re.sub(r"-rc\.(\d+)", r"rc\1", base)
    return base


def main() -> int:
    text = CARGO.read_text()
    m = re.search(r'^version = "([^"]+)"', text, re.M)
    if not m:
        print("no version line in python/Cargo.toml", file=sys.stderr)
        return 1
    base = m.group(1).split("+", 1)[0]  # strip any existing +compat (idempotent)
    cargo_version = f"{base}+compat"
    CARGO.write_text(text.replace(m.group(0), f'version = "{cargo_version}"', 1))

    wheel_version = f"{pep440(base)}+compat"
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"compat_version={wheel_version}\n")
    print(f"stamped python/Cargo.toml -> {cargo_version}  (wheel: lancedb-{wheel_version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
