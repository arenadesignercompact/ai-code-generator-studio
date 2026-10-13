"""End-to-end pipeline tests against a stub provider."""
from __future__ import annotations

import pytest

from src.config.settings import Settings
from src.models.job import Job
from src.models.provider_response import ProviderResponse
from src.pipeline.workers.prompt_ingest import PromptIngestWorker
from src.pipeline.workers.language_router import LanguageRouterWorker
from src.pipeline.workers.code_synthesizer import CodeSynthesizerWorker
from src.pipeline.workers.artifact_writer import ArtifactWriterWorker


@pytest.mark.asyncio
async def test_prompt_ingest_rejects_empty() -> None:
    worker = PromptIngestWorker(Settings())
    job = await worker.process(Job(prompt="   "))
    assert job.errors == ["empty prompt"]


@pytest.mark.asyncio
async def test_language_router_unknown_target() -> None:
    worker = LanguageRouterWorker(Settings())
    job = await worker.process(Job(prompt="hi", target="rust"))
    assert any("no driver" in e for e in job.errors)


@pytest.mark.asyncio
async def test_artifact_writer_writes_python(monkeypatch, tmp_path) -> None:
    settings = Settings(output_root=tmp_path)
    draft = "```python\nprint('hi')\n```\n"
    job = Job(prompt="say hi", target="python", draft=draft)
    job.context["driver"] = "python_driver"
    monkeypatch.setattr(
        CodeSynthesizerWorker,
        "process",
        lambda self, j: _stub(j, draft),
    )
    worker = ArtifactWriterWorker(settings)
    out = await worker.process(job)
    assert len(out.artifacts) == 1
    assert (tmp_path / out.artifacts[0].rel_path).read_text(encoding="utf-8").startswith("print(")


async def _stub(job: Job, draft: str) -> Job:
    job.draft = draft
    return job


@pytest.mark.asyncio
async def test_provider_response_token_sum() -> None:
    resp = ProviderResponse(text="x", model="m", prompt_tokens=10, completion_tokens=5)
    assert resp.total_tokens == 15