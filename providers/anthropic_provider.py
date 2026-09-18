"""
providers/anthropic_provider.py — Anthropic Claude Adapter
Tuân thủ Strategy Pattern theo base_architecture.md.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.request
import urllib.error
from typing import Any

from providers.base import ModelResponse, Provider, ToolCall


class AnthropicProvider(Provider):
    """
    Adapter cho Anthropic API (/v1/messages).
    Chuẩn hóa request/response sang format chung ModelResponse.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.anthropic.com/v1",
        default_model: str = "claude-3-5-sonnet-20241022"
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.base_url = (os.environ.get("ANTHROPIC_BASE_URL") or base_url).rstrip("/")
        self.default_model = os.environ.get("ANTHROPIC_MODEL", default_model)

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.1,
        tool_choice: str | dict[str, Any] = "auto",
        **kwargs: Any
    ) -> ModelResponse:
        active_model = model or self.default_model

        # Tách system prompt và messages
        system_content = ""
        anthropic_messages = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                system_content += f"\n{content}"
            else:
                anthropic_messages.append({
                    "role": "user" if role == "user" else "assistant",
                    "content": content
                })

        # Chuẩn hóa tools sang schema của Anthropic
        formatted_tools = None
        if tools:
            formatted_tools = []
            for t in tools:
                func = t.get("function", t)
                formatted_tools.append({
                    "name": func.get("name"),
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {"type": "object", "properties": {}})
                })

        payload: dict[str, Any] = {
            "model": active_model,
            "max_tokens": 4096,
            "temperature": temperature,
            "messages": anthropic_messages,
        }
        if system_content.strip():
            payload["system"] = system_content.strip()
        if formatted_tools:
            payload["tools"] = formatted_tools

        req_data = json.dumps(payload).encode("utf-8")
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{self.base_url}/messages",
            data=req_data,
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"Anthropic API Error ({e.code}): {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Anthropic Request Failed: {e}")

        text_content = ""
        tool_calls: list[ToolCall] = []

        for block in result.get("content", []):
            b_type = block.get("type")
            if b_type == "text":
                text_content += block.get("text", "")
            elif b_type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.get("id"),
                    name=block.get("name", ""),
                    args=block.get("input", {})
                ))

        return ModelResponse(
            text=text_content if text_content else None,
            tool_calls=tool_calls,
            raw=result,
            finish_reason=result.get("stop_reason")
        )
