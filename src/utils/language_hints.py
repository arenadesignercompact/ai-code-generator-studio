"""Cheap language detection from prompt text."""
from __future__ import annotations

_HINTS = {
    "python": ("python", "fastapi", "django", "pandas", "numpy", "pytest"),
    "cpp": ("c++", "cpp", "cmake", "stl", "template<", "std::"),
    "csharp": ("c#", "csharp", ".net", "dotnet", "linq", "nuget"),
    "java": ("java", "spring", "maven", "gradle", "jvm", "jdk"),
}


def detect_language_hints(prompt: str) -> list[str]:
    low = prompt.lower()
    hits: list[str] = []
    for lang, tokens in _HINTS.items():
        if any(tok in low for tok in tokens):
            hits.append(lang)
    return hits