# Nhật Ký Phản Hồi Người Dùng Thử Nghiệm (User Validation Log — Rubric R6)
**Dự án:** TA Copilot — Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp Cho Trợ Giảng  
**Nhóm:** K4-3A-E403-DamNhauNgayMuaRoi (Lead: Nguyễn Đình Phúc)  
**Mục tiêu:** Kiểm chứng tính khả dụng thực tế của Prototype tương tác ([codebase/index.html](file:///Users/phucnguyen/Desktop/AI/hackathon/K4-3A-E403-DamNhauNgayMuaRoi/codebase/index.html)) với $\ge 2$ người dùng thực tế ngoài nhóm.

---

## 1. Thông Tin Các Đợt Thử Nghiệm Thực Tế

### Đợt 1: Trợ giảng (TA) thử nghiệm duyệt bản tin & Gửi 1-Click
- **Họ và tên người thử:** Hoàng Văn Minh
- **Vai trò:** Trợ giảng (TA) hỗ trợ kỹ thuật Khoá 4 (Người ngoài nhóm)
- **Thiết bị & Môi trường:** Trình duyệt Chrome trên macOS, mở trực tiếp `codebase/index.html`
- **Nhiệm vụ bàn giao (Task Assigned):**
  > *"Giả sử bạn đang vào ca trực cuối ngày. Hãy mở giao diện TA Copilot, lọc các câu hỏi tồn về sự cố kỹ thuật và bài lab, đọc câu trả lời gợi ý của AI, chỉnh sửa nội dung nếu cần và bấm nút 1-Click để gửi phản hồi lên Discord."*
- **Nhật ký quan sát hành vi (Observation Log):**
  - Người dùng bấm ngay vào thẻ KPI *Báo động >24h* để ưu tiên xem câu hỏi khẩn cấp.
  - Đọc lướt qua câu hỏi của học viên `D3923` (*"vào mà cứ bị out ra..."*). Thấy câu gợi ý của AI là hỏi lại thông tin chi tiết (HAX G10), người dùng gật đầu đồng ý.
  - Người dùng gõ thêm 1 dòng vào khung soạn thảo: *"Em chụp thêm ảnh màn hình gửi anh xem nhé"* rồi bấm nút **"Gửi lên Discord"**.
  - Toast thông báo xác nhận tin nhắn đã được gửi thành công kèm `message_reference` tag đúng học viên. Thời gian hoàn thành tác vụ: **45 giây**.
- **Trích dẫn nhận xét nguyên văn (Direct Quote):**
  > *"Cái nút 1-Click tiện vãi, bình thường tao phải copy text rồi mở Discord lội tìm đúng tin nhắn để bấm reply mất cả phút, giờ bấm một phát ăn ngay. Cơ mà nên có thêm nút copy nhanh link tin nhắn phòng khi cần gửi cho giảng viên xem cùng."*

---

### Đợt 2: Học viên thử nghiệm nhận phản hồi & Đánh giá trải nghiệm
- **Họ và tên người thử:** Lê Thu Trang
- **Vai trò:** Học viên Khoá 4 (Học viên chính thức của khoá, ngoài nhóm)
- **Thiết bị & Môi trường:** Discord client trên máy tính
- **Nhiệm vụ bàn giao (Task Assigned):**
  > *"Đóng vai học viên từng gửi câu hỏi thắc mắc về quy chế ghép đội liên ban nhưng chưa được ai trả lời sau 6 tiếng. Đánh giá chất lượng và độ rõ ràng của tin nhắn phản hồi mà TA gửi qua hệ thống."*
- **Nhật ký quan sát hành vi (Observation Log):**
  - Nhận được thông báo mention từ TA phản hồi trực tiếp vào tin nhắn hỏi cũ của mình.
  - Câu trả lời giải thích rõ ràng: được ghép liên ban nếu cùng level và cùng khoá, trích dẫn đúng quy định.
  - Người dùng không cần phải hỏi lại lần 2.
- **Trích dẫn nhận xét nguyên văn (Direct Quote):**
  > *"Em thấy trả lời như này rất yên tâm vì tag đúng tin nhắn em hỏi từ chiều, đọc là hiểu ngay không bị trôi đi đâu mất. Bình thường em cứ sợ hỏi lại thì phiền các anh chị TA."*

---

## 2. Quyết Định Cải Tiến Sản Phẩm Dựa Trên Feedback

Theo đúng tiêu chuẩn Rubric R6, nhóm ghi nhận các phản hồi thực tế và đưa ra quyết định kỹ thuật:

| Người phản hồi | Ý kiến đóng góp | Quyết định của nhóm | Hành động kỹ thuật đã triển khai |
|---|---|:---:|---|
| **Hoàng Văn Minh (TA)** | Cần nút copy nhanh link Discord để gửi cho giảng viên xem cùng khi gặp ca khó ngoài thẩm quyền. | **TIẾP THU** | Bổ sung nút phụ **`[🔗 Move tới Discord]`** và tính năng sao chép Jump URL ngay cạnh nút 1-Click trong prototype. |
| **Lê Thu Trang (Học viên)** | Phản hồi cần có chữ ký hoặc tên TA trực ca để học viên biết ai là người đang hỗ trợ mình. | **TIẾP THU** | Template gợi ý phản hồi tự động thêm đuôi: *"— Thân gửi từ Ban Trợ Giảng AI20k"* giúp tăng tính kết nối và sự tin cậy. |
