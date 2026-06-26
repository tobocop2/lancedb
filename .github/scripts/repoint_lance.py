#!/usr/bin/env python3
"""Repoint every tobocop2/lance git dep in this Cargo.toml to a new -compat tag.

Deterministic line rewriter (no sed): for each line whose git points at
tobocop2/lance, update both the `tag = "..."` and the `version = "=..."`
requirement so they stay consistent with the lance crate version at that tag.
Every other line is byte-identical.

New tag `v9.0.0-beta.9-compat` -> version requirement `=9.0.0-beta.9`.
"""
import re
import sys
from pathlib import Path

_LANCE_GIT = "tobocop2/lance.git"
_TAG = re.compile(r'("tag"\s*=\s*")[^"]+(")')
_VER = re.compile(r'("version"\s*=\s*"=)[^"]+(")')


def base_version(new_tag: str) -> str:
    """v9.0.0-beta.9-compat -> 9.0.0-beta.9"""
    v = new_tag[1:] if new_tag.startswith("v") else new_tag
    return v[: -len("-compat")] if v.endswith("-compat") else v


def repoint(text: str, new_tag: str) -> str:
    ver = base_version(new_tag)
    out = []
    for line in text.splitlines(keepends=True):
        if _LANCE_GIT in line:
            line = _TAG.sub(rf"\g<1>{new_tag}\g<2>", line)
            line = _VER.sub(rf"\g<1>{ver}\g<2>", line)
        out.append(line)
    return "".join(out)


def main() -> int:
    path, new_tag = Path(sys.argv[1]), sys.argv[2]
    path.write_text(repoint(path.read_text(), new_tag))
    print(f"repointed lance deps in {path} -> {new_tag} (version =={base_version(new_tag)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
