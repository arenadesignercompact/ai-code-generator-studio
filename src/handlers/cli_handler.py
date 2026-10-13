"""CLIHandler — parses argv and delegates to bootstrap."""
from __future__ import annotations

from src.bootstrap import main as _main


class CLIHandler:
    def run(self, argv: list[str] | None = None) -> int:
        return _main(argv)