# Tool: `escalate_authority`

## Mô tả
Chuyển tiếp câu hỏi lên Giảng viên, Ban Tổ Chức khi vượt thẩm quyền hỗ trợ của Trợ giảng.

## Parameters
- `message_id` (string, required): Mã tin nhắn cần leo thang.
- `reason` (string, required): Lý do leo thang (ví dụ: xin gia hạn deadline riêng).
- `target_role` (string, required): `[instructor, btc, head_ta]`.

## Output Schema
```json
{
  "status": "escalated",
  "message_id": "SYN-006",
  "reason": "Học viên xin lùi hạn nộp bài Lab 1",
  "escalated_to": "Ban Tổ Chức Khoá Học AI20k",
  "instruction_for_ta": "Ca này vượt quá thẩm quyền. Đã chuyển tiếp tới Ban Tổ Chức. TA không tự ý phê duyệt."
}
```
