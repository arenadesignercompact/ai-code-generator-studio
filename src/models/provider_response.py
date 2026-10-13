"""Normalized response shape returned by every provider adapter."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProviderResponse:
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "stop"

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens