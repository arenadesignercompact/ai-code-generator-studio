"""ContextAssemblerWorker — pulls repo context, language hints, and conventions."""
from __future__ import annotations

from src.models.job import Job
from src.pipeline.workers.base import BaseWorker
from src.utils.language_hints import detect_language_hints


class ContextAssemblerWorker(BaseWorker):
    name = "context_assembler"

    async def process(self, job: Job) -> Job:
        if not self._guard(job):
            return job
        job.context["language_hints"] = detect_language_hints(job.prompt)
        job.context["target"] = job.target
        job.context["style"] = "staff-level"
        return job