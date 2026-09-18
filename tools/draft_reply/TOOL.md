# Tool: `draft_grounded_reply`

## Mô tả
Soạn thảo bản nháp phản hồi có căn cứ xác thực cho Trợ giảng duyệt trước khi gửi lên Discord.

## Parameters
- `message_id` (string, required): Mã tin nhắn cần trả lời.
- `student_id` (string, required): Mã hoặc tên học viên để tag mention.
- `draft_content` (string, required): Nội dung câu trả lời.
- `citation` (string, optional): Căn cứ quy chế chính thức trích dẫn.

## Output Schema
```json
{
  "status": "success",
  "message_id": "SYN-001",
  "student_id": "D9901",
  "draft_text": "Chào @D9901,\nTheo thông báo chính thức...",
  "ready_for_ta_review": true
}
```
