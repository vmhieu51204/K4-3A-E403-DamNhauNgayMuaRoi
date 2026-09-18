# Hướng Dẫn Tích Hợp Frontend (FE Integration Guide) — TA Copilot

Tài liệu này dành cho đội ngũ Frontend (FE) để tích hợp giao diện người dùng với Backend (Agent Logic) của hệ thống TA Copilot. Toàn bộ logic xử lý nghiệp vụ, phân loại câu hỏi, và tạo câu trả lời đã được tách biệt (decoupled) hoàn toàn qua REST API.

## 1. Khởi động API Server (Backend)

Backend được viết bằng Python (FastAPI) để cung cấp endpoint cho FE.
Để chạy server ở local, sử dụng các lệnh sau trong thư mục gốc của dự án:

```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate

# Chạy server FastAPI (sẽ mở tại http://127.0.0.1:8000)
uvicorn api:app --reload
```

## 2. API Endpoints Chính

Server cung cấp sẵn Swagger UI để test API tại: **`http://127.0.0.1:8000/docs`**

### `GET /health`
Kiểm tra trạng thái hệ thống và phiên bản Agent đang chạy.

### `POST /chat`
Endpoint lõi để gửi tin nhắn của người dùng và nhận câu trả lời cùng chuỗi tư duy (tool traces) của Agent.

**Payload Request:**
```json
{
  "query": "Mai có đi học không?",
  "history": []
}
```
*Lưu ý: `history` là mảng các object `{"role": "user"|"assistant", "content": "..."}` để giữ ngữ cảnh hội thoại nếu cần thiết.*

**Response:**
```json
{
  "status": "success",
  "answer": "Theo lịch thì ngày mai lớp mình có buổi Workshop. Đây là buổi bắt buộc tính chuyên cần nhé!",
  "total_rounds": 2,
  "traces": [
    {
      "tool_name": "search_course_kb",
      "arguments": {"query": "lịch học mai"},
      "result": "Hidden"
    }
  ]
}
```

## 3. UI Prototype Tham Khảo (`codebase/index.html`)

Chúng tôi đã chuẩn bị sẵn một bản Prototype giao diện (HTML/Tailwind) tại `codebase/index.html`. 
FE có thể mở file này trực tiếp trên trình duyệt để "vibe" và lấy ý tưởng thiết kế.

### Các Tính Năng Đã Có Trên Prototype FE có thể tham khảo:
1. **Hệ thống Dashboard (Feed Câu hỏi tồn):**
   - Danh sách thẻ (Card) hiển thị tin nhắn.
   - Các badge phân loại độ khẩn cấp (SLA >24h, 4h-24h).
   - Bộ lọc theo Topic (Điểm danh, Lab, Ghép đội, v.v.).
2. **Luồng Xử lý (Workflow) & AI Hỗ Trợ:**
   - **Nút "💬 Xem Thread":** Mở Modal mô phỏng Discord để xem ngữ cảnh tin nhắn của học viên trước và sau khi nhắn.
   - **Nút "🔗 Tới Discord":** Redirect trực tiếp mở URL thực của Discord App (theo cấu trúc `https://discord.com/channels/{guild}/{channel}/{id}`).
   - **✨ TÍNH NĂNG MỚI: AI Gợi ý trả lời (Suggested Reply):** Khi mở Modal xử lý, khung soạn thảo sẽ tự động được điền sẵn một câu trả lời nháp do AI sinh ra (nằm trong trường `aiSuggestedReply` của dữ liệu). Điểm đặc biệt là AI tự động đọc hiểu **lịch sử trò chuyện trước đó** để chắt lọc đáp án cụ thể và xưng hô tự nhiên. 
     *Lưu ý cho FE: Nếu API trả về `aiSuggestedReply` rỗng hoặc null, phải handle cẩn thận để ô textarea hiển thị trống (dùng `placeholder="Nhập câu trả lời..."`) thay vì hiện chữ "undefined".*
   - **Nút "🚀 Reply & Đóng Case":** Xử lý gửi tin phản hồi (bản nháp của AI hoặc TA tự sửa) và ẩn thẻ câu hỏi khỏi feed.
3. **Bản tin Markdown:** Tự động tổng hợp danh sách câu hỏi tồn đọng để TA có thể copy/paste báo cáo tiến độ vào kênh nội bộ.

## 4. Kiến Trúc Hoạt Động (Frontend ↔ Backend)

* **Không nhúng Logic vào Frontend:** FE không cần phải xử lý các rule phức tạp như: "nếu chứa từ khóa A thì là topic B", hay "gọi AI để đánh giá". Hãy để API `/chat` hoặc các script Backend chạy nền tự sinh ra danh sách `MOCK_QUESTIONS.js` (hoặc trả qua một Endpoint lấy danh sách ticket).
* **Mock Data:** Trong giai đoạn phát triển, FE có thể sử dụng trực tiếp mock data có trong `codebase/data/mock_questions.js`.
* **Trạng thái (State):** Việc "Đóng case" (Dismiss/Resolve) hiện đang chạy local state trên JS prototype, khi ráp hệ thống thật, FE sẽ cần call một endpoint ví dụ `POST /ticket/{id}/resolve` để Backend cập nhật database.

---
*Mọi vướng mắc về API hoặc cấu trúc dữ liệu, vui lòng liên hệ trực tiếp Lead/Backend Engineer để được hỗ trợ!*
