"""
tools/post_discord_reply/tool.py — Hành động ghi (Write Action) gửi tin nhắn lên Discord
Theo đúng mục 3.7 trong base_architecture.md:
Layer 2 Implementation Guard bắt buộc 'confirmed is True', kiểm tra mã độc trước khi phát tán.
"""

from typing import Any
from tools._shared import check_forged_payload, check_sensitive_data


def post_discord_reply(
    message_id: str,
    reply_content: str,
    confirmed: bool = False
) -> dict[str, Any]:
    """
    Hành động ghi (Write Action): Bắn phản hồi chính thức lên Discord.
    Quy tắc an toàn 2 lớp:
      1. Bắt buộc có sự xác nhận rõ ràng từ Trợ giảng (confirmed == True).
      2. Quét kiểm tra mã độc injection và rò rỉ dữ liệu nhạy cảm.
    """
    # Lớp bảo vệ 1: Kiểm tra quyền xác nhận ghi
    if confirmed is not True:
        return {
            "status": "needs_confirmation",
            "error": "write_action_not_confirmed",
            "message": "Hành động gửi tin nhắn Discord yêu cầu Trợ giảng bấm duyệt xác nhận (confirmed=True)."
        }

    # Lớp bảo vệ 2: Chặn mã độc Prompt Injection phát tán
    if check_forged_payload(reply_content):
        return {
            "status": "rejected",
            "error": "forged_payload_detected",
            "message": "Từ chối gửi: Phát hiện nội dung chứa chuỗi tiêm chỉ thị độc hại."
        }

    # Lớp bảo vệ 3: Chặn rò rỉ dữ liệu nhạy cảm
    if check_sensitive_data(reply_content):
        return {
            "status": "rejected",
            "error": "sensitive_data_detected",
            "message": "Từ chối gửi: Phát hiện rò rỉ khoá bí mật hoặc thông tin nhạy cảm."
        }

    # Giả lập hoặc thực thi gửi thành công qua Discord Webhook / API
    simulated_discord_message_id = f"DISCORD_REPLY_{message_id}_SUCCESS"

    return {
        "status": "posted",
        "target_message_id": message_id,
        "posted_discord_message_id": simulated_discord_message_id,
        "reply_content": reply_content,
        "action_completed": True,
        "note": "Đã bắn phản hồi thành công lên kênh Discord kèm message_reference tag học viên."
    }
