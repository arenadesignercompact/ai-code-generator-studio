"""CodeSynthesizerWorker — calls the provider and stores the raw draft."""
from __future__ import annotations

from src.models.job import Job
from src.pipeline.workers.base import BaseWorker
from src.services.provider_router import ProviderRouter


class CodeSynthesizerWorker(BaseWorker):
    name = "code_synthesizer"

    async def process(self, job: Job) -> Job:
        if not self._guard(job):
            return job
        router = ProviderRouter(self.settings)
        try:
            response = await router.complete(prompt=job.prompt, target=job.target)
        except Exception as exc:  # noqa: BLE001 — surface as job error
            job.fail(f"synthesis failed: {exc}")
            return job
        job.draft = response.text
        job.context["model"] = response.model
        job.context["tokens"] = response.total_tokens
        return job