"""Runtime settings. Loaded from TOML, overlaid by environment variables."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]

TargetLang = Literal["python", "cpp", "csharp", "java"]


class Settings(BaseModel):
    output_root: Path = Field(default=Path("./generated"))
    log_level: str = "INFO"
    default_target: TargetLang = "python"
    max_prompt_chars: int = 8000
    provider: str = "local"
    provider_endpoint: str = "http://127.0.0.1:11434"
    model_name: str = "studio-coder-7b"
    temperature: float = 0.2
    max_tokens: int = 2048
    execute_generated: bool = False
    sandbox_writes: bool = True


def _env_overrides(raw: dict) -> dict:
    mapping = {
        "STUDIO_OUTPUT_ROOT": ("output_root", Path),
        "STUDIO_LOG_LEVEL": ("log_level", str),
        "STUDIO_PROVIDER": ("provider", str),
        "STUDIO_PROVIDER_ENDPOINT": ("provider_endpoint", str),
        "STUDIO_MODEL": ("model_name", str),
        "STUDIO_TEMPERATURE": ("temperature", float),
    }
    for env_key, (field, caster) in mapping.items():
        if (val := os.getenv(env_key)) is not None:
            raw[field] = caster(val)
    return raw


def load_settings(config_path: Path | None = None) -> Settings:
    raw: dict = {}
    if config_path and config_path.exists():
        with config_path.open("rb") as fh:
            raw = tomllib.load(fh).get("studio", {})
    raw = _env_overrides(raw)
    return Settings(**raw)