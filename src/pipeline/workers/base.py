"""BaseWorker — shared plumbing for every stage."""
from __future__ import annotations

from abc import ABC, abstractmethod

from src.config.settings import Settings
from src.models.job import Job


class BaseWorker(ABC):
    name: str = "base"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @abstractmethod
    async def process(self, job: Job) -> Job: ...

    def _guard(self, job: Job) -> bool:
        """Return True if the job is still valid to process."""
        return not job.errors