"""PromptIngestWorker — validates and normalizes the incoming prompt."""
from __future__ import annotations

import uuid

from src.models.job import Job
from src.pipeline.workers.base import BaseWorker


class PromptIngestWorker(BaseWorker):
    name = "prompt_ingest"

    async def process(self, job: Job) -> Job:
        if not self._guard(job):
            return job
        prompt = job.prompt.strip()
        if not prompt:
            job.fail("empty prompt")
            return job
        if len(prompt) > self.settings.max_prompt_chars:
            job.fail(f"prompt exceeds {self.settings.max_prompt_chars} chars")
            return job
        job.prompt = prompt
        job.job_id = uuid.uuid4().hex[:12]
        job.context["ingested"] = True
        return job