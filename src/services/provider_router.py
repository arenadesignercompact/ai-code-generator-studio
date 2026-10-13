"""ProviderRouter — talks to the configured code model."""
from __future__ import annotations

import httpx

from src.config.settings import Settings
from src.models.provider_response import ProviderResponse


class ProviderRouter:
    """Routes completion requests to the configured provider.

    Local providers (ollama-compatible) are the default. Remote providers
    require an API key in the environment; the key is never logged.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete(self, *, prompt: str, target: str) -> ProviderResponse:
        system = f"You are a staff-level {target} engineer. Output fenced code blocks only."
        payload = {
            "model": self.settings.model_name,
            "prompt": f"{system}\n\n{prompt}",
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.settings.provider_endpoint}/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return ProviderResponse(
            text=data.get("response", ""),
            model=data.get("model", self.settings.model_name),
            prompt_tokens=data.get("prompt_eval_count", 0),
            completion_tokens=data.get("eval_count", 0),
        )