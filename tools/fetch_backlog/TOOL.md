# Tool: `fetch_backlog_questions`

## Mô tả
Quét danh sách câu hỏi của học viên bị bỏ quên sau hơn $X$ giờ (mặc định > 4 giờ).

## Parameters
- `min_hours` (number, default: 4.0): Ngưỡng giờ tồn đọng.
- `topic` (string, default: "all"): Lọc theo chủ đề.
- `limit` (integer, default: 10): Số lượng tối đa trả về.

## Output Schema
```json
{
  "status": "success",
  "total_unanswered": 5,
  "items": [
    {
      "message_id": "REAL-M69081",
      "student_id": "D2313",
      "content": "có điểm danh ws không ạ",
      "unanswered_hours": 6.5
    }
  ]
}
```
