"""ArtifactWriterWorker — parses the draft into files and writes them."""
from __future__ import annotations

from pathlib import Path

from src.models.artifact import Artifact
from src.models.job import Job
from src.pipeline.workers.base import BaseWorker
from src.services.driver_registry import get_driver
from src.utils.path_safety import safe_join


class ArtifactWriterWorker(BaseWorker):
    name = "artifact_writer"

    async def process(self, job: Job) -> Job:
        if not self._guard(job):
            return job
        driver = get_driver(job.context.get("driver", "python_driver"))
        artifacts: list[Artifact] = driver.parse(job.draft, target=job.target)
        if not artifacts:
            job.fail("driver produced no artifacts")
            return job
        root = self.settings.output_root
        for art in artifacts:
            dest = safe_join(root, art.rel_path) if self.settings.sandbox_writes else root / art.rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(art.content, encoding="utf-8")
            art.bytes_written = art.size()
            job.artifacts.append(art)
        return job