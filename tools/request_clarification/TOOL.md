# Tool: `request_clarification`

## Mô tả
Kích hoạt nguyên lý HAX G10: Tạm dừng phiên Agent và hỏi lại học viên khi câu hỏi quá cộc lốc hoặc thiếu thông tin định danh sự cố.

## Parameters
- `message_id` (string, required): Mã tin nhắn cần hỏi lại.
- `clarification_question` (string, required): Câu hỏi cụ thể hướng dẫn học viên cung cấp thông tin.

## Output Schema
Trả về cờ `awaiting_user: true` để Agent Loop tự động dừng:
```json
{
  "status": "awaiting_user",
  "awaiting_user": true,
  "message_id": "REAL-M33885",
  "clarification_question": "Chào bạn, bạn đang truy cập vào Zoom, Portal nộp bài hay Discord vậy ạ? Màn hình báo lỗi gì bạn chụp giúp mình nhé!",
  "guideline_applied": "HAX G10 (Thu hẹp phạm vi khi không chắc chắn)"
}
```
