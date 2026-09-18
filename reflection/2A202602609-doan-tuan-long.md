# Báo Cáo Thu Hoạch Cá Nhân (Individual Reflection) — Mini Hackathon AI

- **Họ và tên:** Đoàn Tuấn Long
- **Mã học viên:** 2A202602609
- **Nhóm:** K4-3A-E403-DamNhauNgayMuaRoi
- **Lớp:** 3A · **Phòng thi:** E403 · **Cụm:** Zone 2
- **Track dự thi:** Track B · Trợ lý Discord (Đề B2: Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp Cho TA)
- **Vai trò chính:** Kiểm thử hệ thống, tạo slide báo cáo và video demo

---

## 1. Phần việc và đóng góp cụ thể trong dự án

Với vai trò phụ trách kiểm thử hệ thống và chuẩn bị phần thuyết trình, tôi tập trung vào việc xác nhận sản phẩm chạy đúng luồng trợ giảng thật, rồi đóng gói thành slide và video demo để Ban Giám khảo hiểu lát cắt trong thời gian ngắn.

### Kiểm thử hệ thống và chạy các chức năng

- Chạy và đối chiếu kết quả eval **Run 1 (88.6%, 31/35)** với **Run 2 (100%, 35/35)** trên bộ 35 case (12 chatlog thật + 23 case tổng hợp). Ghi nhận 4 case FAIL ở vòng 1 — đặc biệt `REAL-M33885` — để nhóm chỉnh guardrail trước khi chốt demo.
- Kiểm tra luồng nghiệp vụ trên prototype theo đúng kịch bản ca trực: quét câu hỏi tồn >4h, lọc theo chủ đề, xem ngữ cảnh, sửa bản nháp, duyệt gửi 1 chạm, hỏi lại khi mơ hồ, bỏ qua tin không thuộc phạm vi hỗ trợ.
- Đi từng thao tác như người dùng thật: mở dashboard, bấm Jump tới tin gốc (ví dụ `M69081` trên `channel_02`), đối chiếu nội dung CSV với thẻ câu hỏi, xác nhận câu mơ hồ không bị đánh dấu **Đã xử lý** khi mới chỉ hỏi lại.
- Rà các điểm dễ hiểu nhầm trên UI: phản hồi chỉ lưu local chưa gửi Discord; Jump URL trên pack ẩn danh không phải link Discord thật; bản nháp phải đủ ngắn để TA sửa được trong vài giây.
- Kiểm tra hai case demo bắt buộc trước khi quay video: case chuẩn `M69081` (“có điểm danh ws không ạ”) và case chỗ khó `M33885` (“vào mà cứ bị out ra…”), bảo đảm hành vi khớp spec (trả lời có nguồn vs. clarify theo HAX G10).

### Chuẩn bị slide báo cáo và video demo

- Xây slide demo 6 trang (`demo-slides.pdf`) bám đúng khung thời gian thuyết trình: User & Job (45s) → Vì sao chọn UV1 (45s) → Giải pháp & kịch bản demo (2 phút) → Kết quả đo Run 1 → Run 2 (45s) → Validation người dùng thật (45s) → Nếu có thêm 1 tuần (30s).
- Đưa số liệu kiểm chứng được lên slide: 1.092 tin, 274 câu hỏi, 20.8% bị trôi, 4.5 giờ công TA/ngày; bảng loại UV2 (an toàn DM) và UV3 (cost-of-error); quality bar CP4 và 4 guardrails v1.
- Viết kịch bản demo hai nhánh: case chuẩn ~50s (Jump URL + duyệt nháp + đóng case) và case chỗ khó ~70s (cờ mơ hồ, không đoán “xoá cache”, hỏi Zoom hay Phoenix).
- Quay và dựng video demo theo đúng thứ tự thao tác đã kiểm thử, cắt phần dư để Ban Giám khảo thấy được nỗi đau, hành động 1 chạm và chỗ AI biết dừng lại.

---

## 2. Trải nghiệm cộng tác cùng AI (AI Co-working & Prompting)

Tôi dùng trợ lý AI chủ yếu để soạn kịch bản demo, bố cục slide và rà checklist kiểm thử. AI giúp tăng tốc, nhưng phần nào được đưa lên sân khấu thì tôi phải chạy tay và đối chiếu với dữ liệu thật.

### Điểm AI hỗ trợ tốt nhất

- **Bố cục slide theo đồng hồ:** AI giúp chia 6 trang đúng khung 45 giây / 2 phút, tránh nhồi quá nhiều chữ vào một slide.
- **Checklist kiểm thử:** AI gợi ý các bước đi xuyên suốt luồng TA (lọc → Jump → sửa nháp → gửi / hỏi lại / bỏ qua). Tôi dùng danh sách đó để tự chạy lại trên prototype chứ không tin mô tả suông.
- **Rút gọn lời thoại demo:** AI hỗ trợ viết câu dẫn ngắn cho từng màn hình, giúp video không bị đọc spec nguyên văn.

### Hạn chế của AI và sự can thiệp của tôi

- **AI hay viết slide “đẹp nhưng không chốt được”:** Bản nháp đầu đầy tính năng và slogan, thiếu số liệu `msg_id` và thời gian chờ. Tôi bắt buộc mỗi slide phải có bằng chứng: `M69081` trôi 24h, Run 1 FAIL 4 case, Run 2 = 35/35.
- **Kịch bản demo dễ bị lý tưởng hóa:** AI muốn show nhiều nút liên tiếp. Tôi cắt còn 2 case vì thời lượng thuyết trình có hạn; case thứ hai phải là chỗ khó, không phải case dễ để “AI trông thông minh”.
- **Không thể thay thế việc bấm tay:** Prompt mô tả UI trơn tru, nhưng khi chạy thật mới thấy nháp dài, trạng thái **Chờ làm rõ** dễ nhầm với **Đã xử lý**. Những lỗi này chỉ phát hiện được khi tự đi hết luồng trước khi quay video.

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

- Tôi đã trực tiếp chạy kiểm thử các chức năng trên prototype, đối chiếu kết quả Run 1 với Run 2, và chịu trách nhiệm kịch bản hai case demo (`M69081`, `M33885`) trước khi đưa lên slide và video.
- Tôi nắm được vì sao nhóm không automate câu trả lời logistics, vì sao Jump URL và duyệt 1 chạm mới là lát cắt, và vì sao case mơ hồ phải hỏi lại thay vì đoán giải pháp.
- Tôi có thể trình bày tuần tự 6 slide, chỉ đúng chỗ bấm trên giao diện, và giải thích trung thực giới hạn hiện tại: eval trên bộ 35 case đã đối chiếu, thao tác gửi chưa phải Discord production, video là luồng đã kiểm thử chứ không phải quay che lỗi.
- Tôi cam kết chịu trách nhiệm phần kiểm thử, slide và video demo; nếu Ban Giám khảo hỏi “chạy thật thì ra gì?”, tôi trả lời bằng đúng những gì đã tự bấm và đã đo, không phóng đại tính năng chưa có.
