"""
providers/openai_provider.py — OpenAI & OpenAI-Compatible Adapter
Theo đúng mục 3.1 & 7 trong base_architecture.md.
Tương thích với OpenAI, OpenRouter, vnaipro proxy, và các endpoint tương thích v1/chat/completions.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.request
import urllib.error
from typing import Any

from providers.base import ModelResponse, Provider, ToolCall


class OpenAIProvider(Provider):
    """
    Adapter cho các dịch vụ hỗ trợ OpenAI Chat Completion API.
    Sử dụng urllib chuẩn để đảm bảo chạy mượt mà không bị phụ thuộc phiên bản thư viện.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        default_model: str = "gpt-4o-mini"
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.default_model = os.environ.get("OPENAI_MODEL", default_model)

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

        # Chuyển đổi tool schema sang định dạng chuẩn OpenAI Function Calling
        formatted_tools = None
        if tools:
            formatted_tools = []
            for t in tools:
                if "type" in t and "function" in t:
                    formatted_tools.append(t)
                else:
                    formatted_tools.append({
                        "type": "function",
                        "function": {
                            "name": t.get("name"),
                            "description": t.get("description", ""),
                            "parameters": t.get("parameters", {"type": "object", "properties": {}})
                        }
                    })

        payload: dict[str, Any] = {
            "model": active_model,
            "messages": messages,
            "temperature": temperature,
        }

        if formatted_tools:
            payload["tools"] = formatted_tools
            payload["tool_choice"] = tool_choice

        # Thêm các tùy chọn kwargs khác nếu có
        for k, v in kwargs.items():
            payload[k] = v

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        ctx = ssl._create_unverified_context()

        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                res_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAIProvider HTTP {e.code} Error: {err_body}") from e
        except Exception as e:
            raise RuntimeError(f"OpenAIProvider Network Error: {str(e)}") from e

        choice = res_data.get("choices", [{}])[0]
        msg = choice.get("message", {})
        finish_reason = choice.get("finish_reason")

        raw_text = msg.get("content")
        tool_calls: list[ToolCall] = []

        # Trích xuất danh sách tool calls nếu có
        raw_tool_calls = msg.get("tool_calls", [])
        for rtc in raw_tool_calls:
            fn = rtc.get("function", {})
            fn_name = fn.get("name", "")
            raw_args = fn.get("arguments", "{}")
            try:
                parsed_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            except json.JSONDecodeError:
                parsed_args = {"_raw_arguments": raw_args}

            tool_calls.append(ToolCall(
                name=fn_name,
                args=parsed_args,
                id=rtc.get("id")
            ))

        return ModelResponse(
            text=raw_text,
            tool_calls=tool_calls,
            raw=res_data,
            finish_reason=finish_reason
        )
