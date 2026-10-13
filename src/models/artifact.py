"""Artifact — a file the pipeline produced."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Artifact:
    rel_path: Path
    language: str
    content: str
    bytes_written: int = 0

    def size(self) -> int:
        return len(self.content.encode("utf-8"))