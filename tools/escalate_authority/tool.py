"""
tools/escalate_authority/tool.py — Leo thang các ca vượt thẩm quyền TA
"""

from typing import Any


def escalate_authority(message_id: str, reason: str, target_role: str) -> dict[str, Any]:
    """
    Chuyển tiếp yêu cầu lên cấp có thẩm quyền (Giảng viên, Ban Tổ Chức, Head TA).
    Áp dụng khi học viên xin gia hạn deadline riêng, khiếu nại quy chế, hoặc nhờ giải bài thi.
    """
    role_names = {
        "instructor": "Giảng viên phụ trách môn học",
        "btc": "Ban Tổ Chức Khoá Học AI20k",
        "head_ta": "Trưởng Ban Trợ Giảng (Head TA)"
    }

    target_name = role_names.get(target_role, target_role)

    return {
        "status": "escalated",
        "message_id": message_id,
        "reason": reason,
        "escalated_to": target_name,
        "instruction_for_ta": f"Ca này vượt quá thẩm quyền. Đã chuyển tiếp tới {target_name}. TA không tự ý phê duyệt.",
        "must_not": "Không xác nhận cho phép lùi hạn hay giải bài hộ học viên."
    }
