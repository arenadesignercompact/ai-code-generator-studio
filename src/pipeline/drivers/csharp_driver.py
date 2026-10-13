"""CSharpDriver — splits a fenced draft into .cs artifacts."""
from __future__ import annotations

import re
from pathlib import Path

from src.models.artifact import Artifact

_FENCE = re.compile(r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<body>.*?)```", re.DOTALL)


class CSharpDriver:
    name = "csharp_driver"
    language = "csharp"
    extension = ".cs"

    def parse(self, draft: str, *, target: str) -> list[Artifact]:
        out: list[Artifact] = []
        for idx, match in enumerate(_FENCE.finditer(draft)):
            lang = match.group("lang").lower()
            if lang not in {"csharp", "cs", "c#"}:
                continue
            body = match.group("body").rstrip() + "\n"
            out.append(Artifact(rel_path=Path(f"Type{idx:02d}{self.extension}"), language="csharp", content=body))
        return out