"""
providers/__init__.py — Provider Factory Function
Theo đúng mục 3.1 trong base_architecture.md.
"""

from __future__ import annotations

from providers.base import ModelResponse, Provider, ToolCall
from providers.openai_provider import OpenAIProvider
from providers.openrouter_provider import OpenRouterProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider
from providers.mock_provider import MockProvider


def make_provider(name: str = "openai", **kwargs) -> Provider:
    """
    Factory function khởi tạo LLM Provider dựa vào tên nhà cung cấp.
    Hỗ trợ: 'openai', 'openrouter', 'anthropic', 'gemini', 'mock', 'vnaipro'
    """
    prov_name = (name or "openai").lower().strip()
    if prov_name in ("openai", "vnaipro"):
        return OpenAIProvider(**kwargs)
    if prov_name == "openrouter":
        return OpenRouterProvider(**kwargs)
    if prov_name == "anthropic":
        return AnthropicProvider(**kwargs)
    if prov_name == "gemini":
        return GeminiProvider(**kwargs)
    if prov_name in ("mock", "offline", "test"):
        return MockProvider(**kwargs)
    raise ValueError(
        f"Unknown provider: '{name}'. Supported providers: ['openai', 'openrouter', 'anthropic', 'gemini', 'mock', 'vnaipro']"
    )


__all__ = [
    "make_provider",
    "Provider",
    "ToolCall",
    "ModelResponse",
    "OpenAIProvider",
    "OpenRouterProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "MockProvider",
]
