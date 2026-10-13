"""PipelineGraph — ordered worker chain over a single Job."""
from __future__ import annotations

import logging
from typing import Protocol

from src.models.job import Job

log = logging.getLogger("studio.pipeline.graph")


class Worker(Protocol):
    name: str

    async def process(self, job: Job) -> Job: ...


class PipelineGraph:
    """A linear worker chain. Order of registration is order of execution.

    Workers may short-circuit by returning a job with `errors` populated; the
    graph stops and returns immediately. This keeps failure semantics simple —
    no partial artifact writes after a synthesis failure.
    """

    def __init__(self) -> None:
        self._workers: list[Worker] = []

    def register(self, worker: Worker) -> "PipelineGraph":
        self._workers.append(worker)
        return self

    async def run(self, *, prompt: str, target: str) -> Job:
        job = Job(prompt=prompt, target=target)
        for worker in self._workers:
            log.debug("running worker=%s", worker.name)
            job = await worker.process(job)
            if job.errors:
                log.warning("worker=%s failed, halting pipeline", worker.name)
                break
        return job