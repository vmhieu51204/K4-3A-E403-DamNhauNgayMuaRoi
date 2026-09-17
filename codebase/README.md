# Prototype — TA Copilot (Track B2: Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp)
**Nhóm:** K4-3A-DamNhauNgayMuaRoi · Zone 2  
**Mốc:** Checkpoint 2 (CP2) — Prototype Bấm Được (Mock / Interactive Flow)

---

## 🎯 Lát cắt 1 câu được hiện thực hoá
> *"Một Trợ giảng (TA) · cuối ca trực mở bản tin tổng hợp · AI trích xuất danh sách các câu hỏi chưa được giải đáp sau 4 giờ và gom nhóm theo chủ đề kèm link tin nhắn trực tiếp · TA bấm link nhảy đến Discord và trả lời dứt điểm từng câu hỏi."*

---

## 🚀 Cách chạy Demo (Trong 5 giây)

### Cách 1: Mở trực tiếp bằng trình duyệt
Chỉ cần nhấp đúp vào file `index.html` hoặc chạy lệnh sau trên terminal Mac:
```bash
open codebase/index.html
```

### Cách 2: Chạy qua Python Local Server
```bash
cd codebase
python3 -m http.server 8080
```
Sau đó truy cập: [http://localhost:8080](http://localhost:8080)

---

## 🎬 Kịch bản Demo 5 Bước cho TA & Giám Khảo (CP2)

1. **Bước 1: Đọc tổng quan ca trực & KPI:**
   - TA mở Dashboard, nhìn ngay vào 4 chỉ số: *Tổng câu hỏi tồn (9)*, *Báo động SLA >24h (2)*, *Tồn đọng 4h-24h (7)*, *Đã xử lý (0)*.
2. **Bước 2: Lọc theo chủ đề & Lớp chỗ khó (Taxonomy):**
   - Bấm chọn các tab: *Điểm danh & WS*, *Lab & Code*, *Ghép đội*, *Quy chế*.
   - Lọc theo 4 lớp chỗ khó: ① Nguồn sự thật, ② Mơ hồ / Thiếu thông tin, ③ Ngoài phạm vi, ④ Đặc thù domain.
3. **Bước 3: Xem chi tiết câu hỏi & HAX / PAIR:**
   - Quan sát các thẻ câu hỏi thực tế được trích xuất từ dataset `k4_messages.csv` (ví dụ `M69081`, `M30246`, `M33885`).
   - Kiểm tra các nguyên tắc HAX được cài cắm:
     - **HAX G1:** Làm rõ phạm vi hệ thống ở banner đầu trang.
     - **HAX G2:** Hiển thị độ tin cậy của AI (ví dụ: 96%).
     - **HAX G11:** Giải thích lý do AI gom nhóm và phát hiện câu hỏi chưa giải đáp.
     - **HAX G9:** Khung câu trả lời gợi ý cho phép TA chỉnh sửa trực tiếp.
     - **HAX G8:** Nút "Bỏ qua" giúp gạt bỏ dễ dàng.
4. **Bước 4: Bấm "🔗 Nhảy tới Discord (Jump URL)" (Điểm nhấn của Lát Cắt):**
   - Click nút Jump URL trên câu hỏi `M69081` hoặc `M30246`.
   - Hệ thống hiển thị Modal giả lập giao diện Discord `#channel_02` với đúng ngữ cảnh tin nhắn trước và sau, tin nhắn cần giải quyết được làm nổi bật màu vàng (amber highlight).
   - Ô phản hồi được điền sẵn bản nháp AI, TA có thể sửa hoặc bấm **"🚀 Gửi Phản Hồi & Đóng Case"**.
5. **Bước 5: Hoàn tất & Cập nhật số liệu:**
   - Câu hỏi được đóng, biến mất khỏi danh sách chờ, số đếm *Đã xử lý* nhảy lên +1.
   - Chuyển sang chế độ **"📑 Bản Tin Discord"** ở góc phải trên để xem giao diện bản tin Markdown được gửi tự động vào kênh nội bộ TA.
