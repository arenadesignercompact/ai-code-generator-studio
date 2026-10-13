"""safe_join — prevent writes escaping the output root."""
from __future__ import annotations

from pathlib import Path


class PathEscapeError(ValueError):
    pass


def safe_join(root: Path, rel: Path) -> Path:
    root = root.resolve()
    candidate = (root / rel).resolve()
    if root not in candidate.parents and candidate != root:
        raise PathEscapeError(f"refusing to write outside {root}: {candidate}")
    return candidate