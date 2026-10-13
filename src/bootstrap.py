"""Entry point. Wires the pipeline graph and dispatches a single job or a watch loop."""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from src.config.settings import load_settings
from src.config.version import VERSION
from src.pipeline.graph import PipelineGraph
from src.pipeline.workers.prompt_ingest import PromptIngestWorker
from src.pipeline.workers.context_assembler import ContextAssemblerWorker
from src.pipeline.workers.code_synthesizer import CodeSynthesizerWorker
from src.pipeline.workers.language_router import LanguageRouterWorker
from src.pipeline.workers.artifact_writer import ArtifactWriterWorker
from src.utils.logging_setup import configure_logging

log = logging.getLogger("studio.bootstrap")


def build_graph(settings) -> PipelineGraph:
    graph = PipelineGraph()
    graph.register(PromptIngestWorker(settings))
    graph.register(ContextAssemblerWorker(settings))
    graph.register(LanguageRouterWorker(settings))
    graph.register(CodeSynthesizerWorker(settings))
    graph.register(ArtifactWriterWorker(settings))
    return graph


async def run_once(prompt: str, target: str, settings) -> int:
    graph = build_graph(settings)
    job = await graph.run(prompt=prompt, target=target)
    if job.errors:
        for err in job.errors:
            log.error("job error: %s", err)
        return 1
    log.info("wrote %d artifact(s) to %s", len(job.artifacts), settings.output_root)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai-code-generator-studio", description="Prompt-to-code studio")
    parser.add_argument("--prompt", required=False, help="natural-language prompt")
    parser.add_argument("--target", default="python", choices=["python", "cpp", "csharp", "java"])
    parser.add_argument("--watch", action="store_true", help="watch prompts/ dir for new files")
    parser.add_argument("--execute", action="store_true", help="run generated code after writing (opt-in)")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    settings = load_settings(args.config)
    configure_logging(settings.log_level)

    if args.watch:
        from src.services.watcher import watch_prompts
        return asyncio.run(watch_prompts(settings))

    if not args.prompt:
        parser.error("--prompt is required unless --watch is set")

    return asyncio.run(run_once(args.prompt, args.target, settings))


if __name__ == "__main__":
    sys.exit(main())