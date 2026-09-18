"""
providers/mock_provider.py — Mock / Offline Provider
Phục vụ chạy thử nghiệm cục bộ, unit test và demo khi không có kết nối API internet.
"""

from __future__ import annotations

from typing import Any
from providers.base import ModelResponse, Provider, ToolCall


class MockProvider(Provider):
    """
    Mock Provider lập luận giả lập theo rule-based heuristics.
    Hỗ trợ phát sinh tool_calls hợp lệ tương ứng với nội dung tin nhắn.
    """

    def __init__(self, **kwargs: Any):
        self.default_model = "mock-agent-v1"

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
        # Lấy message cuối cùng
        last_msg = messages[-1] if messages else {}
        content = last_msg.get("content", "").lower()

        # Nếu tin nhắn cuối là kết quả từ Tool -> Mô phỏng LLM tổng hợp câu trả lời
        if "tool_results_json" in content:
            return ModelResponse(
                text=(
                    "Dựa trên kết quả tra cứu dữ liệu:\n"
                    "- Đã quét và ghi nhận các thông tin cần thiết.\n"
                    "- Quy chế VinUni K4 quy định rõ ràng về hạn chót và điều kiện điểm danh.\n"
                    "Trợ giảng có thể xem xét và nhấn Duyệt gửi trực tiếp cho học viên."
                ),
                finish_reason="stop"
            )

        # Nếu user hỏi về tồn đọng/backlog -> Kích hoạt fetch_backlog_questions
        if any(k in content for k in ["tồn", "backlog", "chưa trả lời", "quét"]):
            return ModelResponse(
                text=None,
                tool_calls=[
                    ToolCall(
                        name="fetch_backlog_questions",
                        args={"min_hours": 4.0, "topic": "all", "limit": 5}
                    )
                ],
                finish_reason="tool_calls"
            )

        # Nếu hỏi về quy chế/deadline/nộp bài -> Kích hoạt search_course_kb
        if any(k in content for k in ["quy chế", "điểm danh", "vắng", "deadline", "quy định", "hạn"]):
            return ModelResponse(
                text=None,
                tool_calls=[
                    ToolCall(
                        name="search_course_kb",
                        args={"query": content[:60]}
                    )
                ],
                finish_reason="tool_calls"
            )

        # Nếu cần làm rõ -> Kích hoạt request_clarification
        if any(k in content for k in ["mơ hồ", "chưa rõ", "làm rõ"]):
            return ModelResponse(
                text=None,
                tool_calls=[
                    ToolCall(
                        name="request_clarification",
                        args={"question_id": "MSG_UNKNOWN", "missing_aspect": "Cần thêm ngữ cảnh cụ thể"}
                    )
                ],
                finish_reason="tool_calls"
            )

        # Mặc định trả lời trực tiếp
        return ModelResponse(
            text="Chào bạn, tôi là TA Copilot (Mock Provider). Tôi có thể giúp quét câu hỏi tồn đọng, tra cứu quy chế và soạn câu trả lời 1-click.",
            finish_reason="stop"
        )
