"""LLM access for the matching agent (OpenRouter via the OpenAI-compatible API).

Config (env or .env):
  OPENROUTER_API_KEY      required for live LLM calls
  OPENROUTER_MODEL        default anthropic/claude-sonnet-4.5
  OPENROUTER_MAX_TOKENS   default 2048 for chat replies (always capped — unset
                          means model max, which can 402 on small balances).
                          Structured calls (analysis, verdicts) use at most 1024.
  MATCHING_AGENT_OFFLINE  "1" forces offline mode: every LLM step falls back
                          to its deterministic heuristic (used by tests and
                          when the API quota is exhausted)
"""

from __future__ import annotations

import os
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"
DEFAULT_MAX_TOKENS = 2048
STRUCTURED_MAX_TOKENS = 1024


class LLMUnavailable(RuntimeError):
    """Raised when no live LLM is configured; callers fall back to heuristics."""


def _load_env_file(path: str = os.path.join(BASE_DIR, ".env")) -> None:
    """Minimal .env loader (same as Milestone 1): KEY=VALUE lines, no overrides."""
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()


def is_offline() -> bool:
    return (os.environ.get("MATCHING_AGENT_OFFLINE") == "1"
            or not os.environ.get("OPENROUTER_API_KEY"))


def model_name() -> str:
    return os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)


@lru_cache(maxsize=4)
def _chat_model(model: str, max_tokens: int):
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model,
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url=OPENROUTER_BASE_URL,
        max_tokens=max_tokens,
        temperature=0,
        timeout=120,
        max_retries=2,
        default_headers={"HTTP-Referer": "https://github.com/airtribe",
                         "X-Title": "Resume Matching Agent"},
    )


def get_llm(max_tokens: int | None = None):
    """Return the configured chat model, or raise LLMUnavailable."""
    if is_offline():
        raise LLMUnavailable("offline mode (no OPENROUTER_API_KEY or MATCHING_AGENT_OFFLINE=1)")
    cap = int(os.environ.get("OPENROUTER_MAX_TOKENS", DEFAULT_MAX_TOKENS))
    return _chat_model(model_name(), min(cap, max_tokens) if max_tokens else cap)


def structured(schema, messages):
    """Invoke the LLM and parse its reply into a pydantic `schema` instance."""
    return (get_llm(STRUCTURED_MAX_TOKENS)
            .with_structured_output(schema, method="function_calling").invoke(messages))


def structured_batch(schema, batches: list, max_concurrency: int = 3) -> list:
    """Run several structured calls concurrently. Failed items come back as the
    exception instance so callers can fall back per item."""
    runnable = get_llm(STRUCTURED_MAX_TOKENS).with_structured_output(schema, method="function_calling")
    return runnable.batch(batches, config={"max_concurrency": max_concurrency},
                          return_exceptions=True)
