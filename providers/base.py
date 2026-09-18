"""
providers/base.py — Contract chung cho Provider Layer (Strategy Pattern)
Theo đúng mục 3.1 trong base_architecture.md.
Quy tắc: Toàn bộ downstream code chỉ giao tiếp qua ToolCall, ModelResponse và Provider Protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass
class ToolCall:
    """Đại diện cho một lời gọi công cụ do mô hình sinh ra."""
    name: str                       # Tên công cụ mô hình muốn gọi
    args: dict[str, Any]            # Tham số đối số mô hình truyền vào
    id: str | None = None           # ID lời gọi nếu vendor cung cấp (OpenAI tool_call_id)


@dataclass
class ModelResponse:
    """Kết quả phản hồi chuẩn hoá từ LLM."""
    text: str | None = None                                    # Phản hồi văn bản trực tiếp
    tool_calls: list[ToolCall] = field(default_factory=list)  # Danh sách công cụ được yêu cầu gọi
    raw: Any | None = None                                     # Đối tượng thô từ vendor phục vụ debug
    finish_reason: str | None = None                           # Lý do kết thúc (stop, tool_calls, length...)


@runtime_checkable
class Provider(Protocol):
    """Giao diện hợp đồng (Interface Protocol) mà mọi LLM Adapter bắt buộc phải tuân thủ."""
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
        """Gửi messages và tools tới LLM, trả về ModelResponse chuẩn hóa."""
        ...
