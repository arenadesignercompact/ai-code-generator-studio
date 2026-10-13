"""LanguageRouterWorker — picks the output driver from target + hints."""
from __future__ import annotations

from src.models.job import Job
from src.pipeline.workers.base import BaseWorker

_DRIVERS = {
    "python": "python_driver",
    "cpp": "cpp_driver",
    "csharp": "csharp_driver",
    "java": "java_driver",
}


class LanguageRouterWorker(BaseWorker):
    name = "language_router"

    async def process(self, job: Job) -> Job:
        if not self._guard(job):
            return job
        driver = _DRIVERS.get(job.target)
        if driver is None:
            job.fail(f"no driver for target={job.target}")
            return job
        job.context["driver"] = driver
        return job