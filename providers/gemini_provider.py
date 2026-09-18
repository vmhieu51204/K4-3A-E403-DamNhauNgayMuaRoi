"""
providers/gemini_provider.py — Google Gemini Adapter
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


class GeminiProvider(Provider):
    """
    Adapter cho Google Gemini API (v1beta generateContent).
    Chuẩn hóa request/response sang format chung ModelResponse.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        default_model: str = "gemini-1.5-flash"
    ):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.base_url = (os.environ.get("GEMINI_BASE_URL") or base_url).rstrip("/")
        self.default_model = os.environ.get("GEMINI_MODEL", default_model)

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

        # Chuyển đổi OpenAI-style messages sang contents của Gemini
        contents = []
        system_instruction = None

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                system_instruction = {"parts": [{"text": content}]}
            elif role == "user":
                contents.append({
                    "role": "user",
                    "parts": [{"text": content}]
                })
            elif role == "assistant":
                contents.append({
                    "role": "model",
                    "parts": [{"text": content}]
                })

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
            }
        }
        if system_instruction:
            payload["systemInstruction"] = system_instruction

        # Chuyển đổi tools sang Gemini function declarations
        if tools:
            func_decls = []
            for t in tools:
                func = t.get("function", t)
                func_decls.append({
                    "name": func.get("name"),
                    "description": func.get("description", ""),
                    "parameters": func.get("parameters", {"type": "object", "properties": {}})
                })
            payload["tools"] = [{"functionDeclarations": func_decls}]

        url = f"{self.base_url}/models/{active_model}:generateContent?key={self.api_key}"
        req_data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"Gemini API Error ({e.code}): {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Gemini Request Failed: {e}")

        text_content = ""
        tool_calls: list[ToolCall] = []

        candidates = result.get("candidates", [])
        finish_reason = None
        if candidates:
            candidate = candidates[0]
            finish_reason = candidate.get("finishReason")
            content_obj = candidate.get("content", {})
            for part in content_obj.get("parts", []):
                if "text" in part:
                    text_content += part.get("text", "")
                elif "functionCall" in part:
                    fc = part["functionCall"]
                    tool_calls.append(ToolCall(
                        name=fc.get("name", ""),
                        args=fc.get("args", {})
                    ))

        return ModelResponse(
            text=text_content if text_content else None,
            tool_calls=tool_calls,
            raw=result,
            finish_reason=finish_reason
        )
