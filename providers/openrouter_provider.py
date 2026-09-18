"""
providers/openrouter_provider.py — OpenRouter Adapter
Kế thừa từ OpenAIProvider, tuân thủ Strategy Pattern theo base_architecture.md.
"""

from __future__ import annotations

import os
from typing import Any
from providers.openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """
    Adapter cho OpenRouter (https://openrouter.ai).
    Hỗ trợ truy cập đa dạng mô hình thông qua cùng một OpenAI-compatible API.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://openrouter.ai/api/v1",
        default_model: str = "anthropic/claude-3.5-sonnet"
    ):
        key = api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        model = os.environ.get("OPENROUTER_MODEL") or default_model
        super().__init__(api_key=key, base_url=base_url, default_model=model)
