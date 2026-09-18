# Tool: `post_discord_reply`

## Mô tả
Hành động ghi (Write Action): Gửi phản hồi chính thức lên Discord tag đúng học viên.

## Parameters
- `message_id` (string, required): Mã tin nhắn cần reply.
- `reply_content` (string, required): Nội dung câu trả lời.
- `confirmed` (boolean, required, default: false): Xác nhận từ Trợ giảng.

## Output Schema
- Nếu chưa xác nhận (`confirmed=false`):
```json
{
  "status": "needs_confirmation",
  "error": "write_action_not_confirmed"
}
```

- Nếu đã xác nhận (`confirmed=true`):
```json
{
  "status": "posted",
  "target_message_id": "SYN-001",
  "action_completed": true
}
```
