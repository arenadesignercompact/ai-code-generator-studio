"""CppDriver — splits a fenced draft into .cpp / .hpp artifacts."""
from __future__ import annotations

import re
from pathlib import Path

from src.models.artifact import Artifact

_FENCE = re.compile(r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<body>.*?)```", re.DOTALL)
_EXT = {"cpp": ".cpp", "c++": ".cpp", "hpp": ".hpp", "h": ".h"}


class CppDriver:
    name = "cpp_driver"
    language = "cpp"
    extension = ".cpp"

    def parse(self, draft: str, *, target: str) -> list[Artifact]:
        out: list[Artifact] = []
        for idx, match in enumerate(_FENCE.finditer(draft)):
            lang = match.group("lang").lower()
            ext = _EXT.get(lang)
            if ext is None:
                continue
            body = match.group("body").rstrip() + "\n"
            out.append(Artifact(rel_path=Path(f"unit_{idx:02d}{ext}"), language="cpp", content=body))
        return out