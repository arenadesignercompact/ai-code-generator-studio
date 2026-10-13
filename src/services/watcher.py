"""Watch the prompts/ directory and run the pipeline on each new file."""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.bootstrap import run_once
from src.config.settings import Settings

log = logging.getLogger("studio.services.watcher")
PROMPTS_DIR = Path("prompts")


class _PromptHandler(FileSystemEventHandler):
    def __init__(self, settings: Settings, loop: asyncio.AbstractEventLoop) -> None:
        self.settings = settings
        self.loop = loop

    def on_created(self, event) -> None:  # type: ignore[override]
        if event.is_directory or not str(event.src_path).endswith(".txt"):
            return
        prompt = Path(event.src_path).read_text(encoding="utf-8")
        log.info("picked up %s", event.src_path)
        asyncio.run_coroutine_threadsafe(
            run_once(prompt, self.settings.default_target, self.settings), self.loop
        )


async def watch_prompts(settings: Settings) -> int:
    PROMPTS_DIR.mkdir(exist_ok=True)
    loop = asyncio.get_running_loop()
    observer = Observer()
    observer.schedule(_PromptHandler(settings, loop), str(PROMPTS_DIR), recursive=False)
    observer.start()
    log.info("watching %s", PROMPTS_DIR)
    try:
        while True:
            await asyncio.sleep(1.0)
    finally:
        observer.stop()
        observer.join()
    return 0