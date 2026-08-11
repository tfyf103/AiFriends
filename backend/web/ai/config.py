"""Central AI runtime configuration.

Why this file exists
--------------------
Earlier versions of AiFriends hard-coded model names and implicitly required every
AI capability to be available at the same time. That is inconvenient for beginners:
a learner who only wants to study Vue/Django/SSE should not need a speech account.

The project now supports three learning-friendly modes:

``mock``
    No external AI service is required. Chat returns deterministic local text.
``text``
    Real chat model is used, while RAG/ASR/TTS are disabled unless explicitly enabled.
``full``
    Backwards-compatible mode: chat, RAG, ASR and TTS are enabled by default.

Existing deployments that do not define ``AI_MODE`` continue to behave like the old
project because the code default remains ``full``. New learners copying
``.env.example`` will start with ``AI_MODE=mock``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable with beginner-friendly spellings."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AISettings:
    mode: str
    enable_rag: bool
    enable_asr: bool
    enable_tts: bool
    chat_model: str
    memory_model: str
    embedding_model: str
    embedding_dimensions: int
    asr_model: str
    tts_model: str

    @property
    def is_mock(self) -> bool:
        return self.mode == "mock"

    @property
    def is_text(self) -> bool:
        return self.mode == "text"

    @property
    def is_full(self) -> bool:
        return self.mode == "full"


def get_ai_settings() -> AISettings:
    """Build settings from the *current* environment.

    This is intentionally a function instead of module-level constants. Tests and
    management commands can temporarily change environment variables and immediately
    observe the result without reloading the module.
    """
    mode = os.getenv("AI_MODE", "full").strip().lower()
    if mode not in {"mock", "text", "full"}:
        mode = "full"

    full_defaults = mode == "full"

    try:
        dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))
    except ValueError:
        dimensions = 1024

    return AISettings(
        mode=mode,
        enable_rag=env_bool("ENABLE_RAG", full_defaults),
        enable_asr=env_bool("ENABLE_ASR", full_defaults),
        enable_tts=env_bool("ENABLE_TTS", full_defaults),
        chat_model=os.getenv("CHAT_MODEL", "deepseek-v4-pro"),
        memory_model=os.getenv("MEMORY_MODEL", os.getenv("CHAT_MODEL", "deepseek-v4-pro")),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-v4"),
        embedding_dimensions=dimensions,
        asr_model=os.getenv("ASR_MODEL", "gummy-realtime-v1"),
        tts_model=os.getenv("TTS_MODEL", "cosyvoice-v3-flash"),
    )
