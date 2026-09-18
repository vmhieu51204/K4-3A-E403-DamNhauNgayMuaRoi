# Báo Cáo Thu Hoạch Cá Nhân (Individual Reflection) — Mini Hackathon AI

- **Họ và tên:** Vũ Minh Hiếu
- **Mã học viên:** 2A202602779
- **Nhóm:** K4-3A-E403-DamNhauNgayMuaRoi
- **Lớp:** 3A · **Phòng thi:** E403 · **Cụm:** Zone 2
- **Track dự thi:** Track B · Trợ lý Discord (Đề B2: Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp Cho TA)
- **Vai trò chính:** Nhóm trưởng (Team Lead) & Quản lý Tài liệu Dự án (Spec Lead)

---

## 1. Phần việc và đóng góp cụ thể trong dự án

Với vai trò là Nhóm trưởng kiêm người phụ trách tài liệu và điều phối, tôi đã trực tiếp đảm nhiệm các phần việc trọng tâm sau:

1. **Điều phối tiến độ và đồng bộ nhóm qua các Checkpoint (CP1 → CP6):**
   - Lên kế hoạch phân chia công việc cho từng thành viên (gán tên cụ thể cho Phúc, Long, Dương Minh Hiếu theo đúng thế mạnh về Prompt/API, Kiểm thử/Slide, và Data/UI).
   - Kiểm soát chặt chẽ các mốc nộp bài (CP1: 19:30 16/9, CP2: 21:00 16/9, CP3: 16:00 17/9, CP4: 21:00 17/9 và chuẩn bị cho CP5: 13:00 18/9).

2. **Khai phá dữ liệu gốc (Data Mining) & Xác lập Bằng chứng Nỗi đau (Rubric R1):**
   - Trực tiếp phân tích tập dữ liệu thực tế `data/discord-pack/k4_messages.csv` gồm 1.092 tin nhắn onboarding Khoá 4.
   - Thống kê định lượng: chỉ ra **274 câu hỏi** từ học viên, trong đó có tới **57 câu hỏi (20.8%) bị trôi và hoàn toàn không có ai phản hồi trực tiếp**.
   - Trích xuất các lỗi điển hình từ bản tin bot hiện tại (`k4_daily_reports.md`) như lỗi chèn đè chuỗi tham chiếu và lỗi cắt cụt văn bản, từ đó làm căn cứ bảo vệ tính cấp thiết của đề tài.

3. **Chịu trách nhiệm chính xây dựng và chuẩn hoá tài liệu:**
   - **Canvas (`canvas.md`):** Xây dựng Canvas 7 dòng nộp tại CP1, định vị rõ Job Executor (Trợ giảng trực ca) và Problem Statement không chứa từ "AI".
   - **AI Spec (`spec.md`):** Trực tiếp viết và chuẩn hóa toàn bộ 9 mục (§1 → §9) theo đúng khung `03-ai-spec-template.md`, bao gồm: Bảng impact 3 ứng viên, phân tích cost-of-error cho cơ chế Augment, hệ thống 4 lớp chỗ khó, 8 kịch bản lỗi HAX/PAIR, và chốt cứng Quality Bar trước hạn chốt spec (21:00 17/9).

---

## 2. Trải nghiệm cộng tác cùng AI (AI Co-working & Prompting)

Trong suốt 48 giờ hackathon, tôi thường xuyên sử dụng các công cụ trợ lý AI (như Claude, ChatGPT, Cursor/Antigravity) như một người bạn đồng hành (pair-programmer/product advisor):

- **Điểm AI hỗ trợ tốt nhất:**
  - **Tăng tốc cấu trúc hóa tài liệu:** AI giúp nhanh chóng chuyển đổi các ghi chú thô của nhóm thành bảng biểu markdown chuẩn chỉnh, hỗ trợ đối chiếu nhanh giữa các tiêu chí Rubric và nội dung trong spec.
  - **Gợi ý kịch bản biên (Edge-case brainstorming):** Khi xây dựng §5 (Kiểu lỗi và Kịch bản rủi ro), AI hỗ trợ gợi ý các tình huống tấn công tiêm chỉ thị gián tiếp (Indirect Prompt Injection) và các câu hỏi học thuật vi phạm liêm chính.

- **Hạn chế của AI & Sự can thiệp quyết định của con người:**
  - **AI hay bị "vibe-check" và dễ tính:** Khi nhờ AI đánh giá output ban đầu, AI thường cho rằng mọi thứ đều "hoàn hảo" hoặc sinh ra các tiêu chí chung chung, không đo lường được. Tôi đã phải can thiệp để ép tiêu chí thành các chỉ số định lượng kiểm chứng được (như tỷ lệ pass $\ge 85\%$, Intent $\ge 90\%$, Action $\ge 85\%$).
  - **Thiếu bối cảnh vận hành thực tế:** AI ban đầu đề xuất giải pháp bot tự động DM riêng cho học viên. Tôi và nhóm nhận ra ngay giải pháp này vi phạm điều kiện an toàn của Track B (không tự ý gửi tin nhắn riêng cho học viên) và cost-of-error quá cao, nên đã loại bỏ để chuyển sang mô hình Human-in-the-loop hỗ trợ TA.

---

## 3. Bài học kinh nghiệm sâu sắc nhất từ Case Thất Bại của nhóm

### Case thất bại điển hình: `REAL-M33885` (Lớp chỗ khó ② — Tin nhắn cộc lốc, mơ hồ)
- **Dữ liệu thực tế:** Học viên gửi tin nhắn: *"vào mà cứ bị out ra thì phải làm sao ạ :v"*.
- **Hiện tượng lỗi ở Lượt 1 (Run 1):** 
  - AI nhận diện đúng chủ đề kỹ thuật (`technical`), nhưng lại tự tin chọn hành động **`action: answer`** và vội vã đưa ra lời khuyên phỏng đoán: *"Bạn thử xóa cache trình duyệt hoặc thử lại bằng tab ẩn danh"*.
  - Kết quả kiểm thử: **FAIL** do vi phạm tiêu chuẩn hành vi kỳ vọng (`expected_action: clarify`).
- **Phân tích nguyên nhân:** 
  - Đây là lỗi điển hình của mô hình ngôn ngữ lớn: **thiên kiến cố gắng làm hài lòng người dùng (eagerness to help)** dẫn đến việc "đoán mò" khi thiếu dữ liệu đầu vào trầm trọng (học viên không nói rõ out khỏi Zoom, Phoenix hay Discord). Nếu áp dụng trong thực tế, lời khuyên sai này sẽ khiến học viên hoang mang và tốn thời gian vô ích.
- **Cách nhóm đã giải quyết:**
  - Chúng tôi áp dụng triệt để nguyên tắc **HAX G10 (Thu hẹp phạm vi khi nghi ngờ)** vào Prompt v1 và Guardrail 1: *Nếu tin nhắn dưới 15 từ, thiếu chủ ngữ hoặc không nêu rõ hệ thống gặp sự cố, AI bắt buộc phải chọn hành động `clarify` để soạn câu hỏi làm rõ, tuyệt đối không được tự ý phỏng đoán giải pháp*.
  - Ở Lượt 2 (Run 2), case này đã chuyển sang **PASS 100%**.
- **Bài học tư duy sản phẩm AI lớn nhất rút ra:**
  > *"Sản phẩm AI tốt không phải là sản phẩm luôn cố gắng trả lời mọi thứ, mà là sản phẩm biết rõ giới hạn của mình: biết khi nào cần dừng lại để hỏi làm rõ (HAX G10) và biết giữ con người trong vòng lặp quyết định (Human-in-the-loop) khi chi phí sai sót là đắt."*

---

## 4. Tự đánh giá & Cam kết trách nhiệm (Vibe-Coding Check)

- Tôi đã trực tiếp tham gia vào quá trình phân tích số liệu, định hình bài toán, viết Spec và theo dõi quá trình kiểm thử Run 1 & Run 2.
- Tôi nắm vững toàn bộ kiến trúc sản phẩm, lát cắt 1 câu, bảng phân loại 4 lớp chỗ khó và cách thức áp dụng các nguyên tắc HAX/PAIR trong mã nguồn prototype.
- Tôi cam kết tự tin trả lời bất kỳ câu hỏi phản biện nào từ Ban Giám khảo về quy trình sản phẩm, số liệu đo lường và vai trò cá nhân trong buổi thuyết trình CP6.
