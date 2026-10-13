"""Job — the unit of work that flows through the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.models.artifact import Artifact


@dataclass(slots=True)
class Job:
    prompt: str
    target: str = "python"
    job_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: dict[str, Any] = field(default_factory=dict)
    draft: str = ""
    artifacts: list[Artifact] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    scratch_dir: Path | None = None

    def fail(self, message: str) -> None:
        self.errors.append(message)