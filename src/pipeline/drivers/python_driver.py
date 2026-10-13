"""PythonDriver — splits a fenced draft into .py artifacts."""
from __future__ import annotations

import re
from pathlib import Path

from src.models.artifact import Artifact

_FENCE = re.compile(r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<body>.*?)```", re.DOTALL)


class PythonDriver:
    name = "python_driver"
    language = "python"
    extension = ".py"

    def parse(self, draft: str, *, target: str) -> list[Artifact]:
        out: list[Artifact] = []
        for idx, match in enumerate(_FENCE.finditer(draft)):
            lang = match.group("lang").lower()
            if lang not in {"python", "py", ""}:
                continue
            body = match.group("body").rstrip() + "\n"
            out.append(Artifact(rel_path=Path(f"module_{idx:02d}{self.extension}"), language=self.language, content=body))
        return out