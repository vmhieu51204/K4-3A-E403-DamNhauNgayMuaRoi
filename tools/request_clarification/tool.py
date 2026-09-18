"""
tools/request_clarification/tool.py — Kích hoạt HAX G10 khi tin nhắn mơ hồ
Trả về cờ 'awaiting_user: True' để Agent Loop tự động dừng và hỏi lại người dùng.
"""

from typing import Any


def request_clarification(message_id: str, clarification_question: str) -> dict[str, Any]:
    """
    Tạm dừng phiên xử lý của Agent và tạo câu hỏi làm rõ gửi tới học viên.
    Theo đúng mục 3.3 trong base_architecture.md:
    Loop nhận cờ 'awaiting_user: True' sẽ dừng quay vòng và trả quyền tương tác cho người dùng.
    """
    return {
        "status": "awaiting_user",
        "awaiting_user": True,
        "message_id": message_id,
        "clarification_question": clarification_question,
        "guideline_applied": "HAX G10 (Thu hẹp phạm vi khi không chắc chắn)"
    }
