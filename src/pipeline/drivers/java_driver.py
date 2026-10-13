"""JavaDriver — splits a fenced draft into .java artifacts."""
from __future__ import annotations

import re
from pathlib import Path

from src.models.artifact import Artifact

_FENCE = re.compile(r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<body>.*?)```", re.DOTALL)


class JavaDriver:
    name = "java_driver"
    language = "java"
    extension = ".java"

    def parse(self, draft: str, *, target: str) -> list[Artifact]:
        out: list[Artifact] = []
        for idx, match in enumerate(_FENCE.finditer(draft)):
            lang = match.group("lang").lower()
            if lang not in {"java"}:
                continue
            body = match.group("body").rstrip() + "\n"
            out.append(Artifact(rel_path=Path(f"Class{idx:02d}{self.extension}"), language="java", content=body))
        return out