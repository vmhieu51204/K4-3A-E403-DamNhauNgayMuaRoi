"""
tools/draft_reply/tool.py — Soạn thảo bản nháp phản hồi có căn cứ cho Trợ giảng duyệt
"""

from typing import Any
from tools._shared import check_forged_payload, check_sensitive_data


def draft_grounded_reply(
    message_id: str,
    student_id: str,
    draft_content: str,
    citation: str = ""
) -> dict[str, Any]:
    """
    Soạn thảo bản nháp phản hồi hỗ trợ TA duyệt trước khi gửi lên Discord.
    Kiểm tra bảo mật: Không chấp nhận nội dung chứa payload tiêm chỉ thị hoặc API key rò rỉ.
    """
    if check_forged_payload(draft_content):
        return {
            "status": "error",
            "error_type": "security_violation",
            "message": "Nội dung phản hồi bị từ chối do chứa chỉ thị tiêm độc hại (Prompt Injection)."
        }

    if check_sensitive_data(draft_content):
        return {
            "status": "error",
            "error_type": "sensitive_data_leak",
            "message": "Cảnh báo an toàn: Phát hiện dữ liệu nhạy cảm hoặc API Key rò rỉ trong câu trả lời."
        }

    formatted_text = f"Chào @{student_id},\n{draft_content}"
    if citation:
        formatted_text += f"\n(Căn cứ: {citation})"
    formatted_text += "\n— Thân gửi từ Ban Trợ Giảng AI20k"

    return {
        "status": "success",
        "message_id": message_id,
        "student_id": student_id,
        "draft_text": formatted_text,
        "citation": citation,
        "ready_for_ta_review": True
    }
