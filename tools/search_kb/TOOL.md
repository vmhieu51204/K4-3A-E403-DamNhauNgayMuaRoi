# Tool: `search_course_kb`

## Mô tả
Tra cứu thông tin chính thức từ cơ sở dữ liệu quy chế khoá học K4 (chuyên cần, bài lab, ghép đội, thi cử).

## Parameters
- `query` (string, required): Câu hỏi hoặc từ khoá cần tra cứu.
- `category` (string, optional): Lọc theo nhóm `[attendance, lab_deadline, team_rule, general_policy]`.

## Output Schema
```json
{
  "status": "success",
  "query": "hạn nộp lab 1",
  "results_count": 1,
  "results": [
    {
      "id": "KB-LAB-01",
      "title": "Hạn nộp và quy định chấm bài Lab 1",
      "content": "Hạn nộp Lab 1 chính thức là 23:59 ngày 17/09/2026 trên Portal...",
      "citation": "Thông báo môn học #lab-announcements"
    }
  ]
}
```
