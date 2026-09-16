# AI SPEC — Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp Cho TA · Nhóm [K4-3A-DamNhauNgayMuaRoi] · Zone [Zone 2]
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới (B2)

---

## §1. User & Job

### Job Executor & Workflow
- **Job Executor:** Trợ giảng (TA) / Moderator trực ca hỗ trợ học viên trên cộng đồng Discord khoá học (khoá ~1.000 học viên).
- **Workflow hiện tại của TA:**
  1. Vào ca trực cuối ngày hoặc giữa các buổi học.
  2. Mở Discord, cuộn tay (scroll) qua hàng chục kênh thảo luận (`channel_01` đến `channel_12`, kênh công khai, kênh lab, kênh thảo luận chung).
  3. Đọc lướt hàng trăm tin nhắn lẫn lộn giữa chào hỏi, đùa vui, thông báo bot, câu hỏi đã có người giải đáp và câu hỏi chưa ai trả lời.
  4. Đọc bản tin ngày do bot tự sinh hiện tại để nắm tình hình, nhưng bản tin này chỉ là văn xuôi tóm tắt chung chung, không có link bấm thẳng tới tin nhắn gốc.
  5. Phát hiện câu hỏi tồn bằng mắt thường, bấm reply trả lời hoặc tag người liên quan.

### Core JTBD (Không có tên sản phẩm / không có chữ AI)
> *"Khi vào ca trực hỗ trợ cuối ngày, tôi muốn nhanh chóng nhận diện chính xác các câu hỏi của học viên chưa được giải đáp sau nhiều giờ kèm đường dẫn trực tiếp, để tôi có thể phản hồi kịp thời đúng người đúng vấn đề mà không phải tốn thời gian lội đọc thủ công hàng trăm tin nhắn rác."*

### Problem Statement (KHÔNG chữ AI)
> *"Trợ giảng và Moderator mất 45–60 phút mỗi ca trực để rà soát thủ công hàng trăm tin nhắn trên các kênh Discord nhằm tìm kiếm câu hỏi còn tồn đọng; trong khi đó, hơn 20% câu hỏi của học viên về logistics, điểm danh và bài lab bị trôi tin nhắn, khiến học viên phải hỏi lại nhiều lần sau 4–24 giờ hoặc nhận phản hồi trễ dẫn đến lo lắng và vi phạm quy chế nộp bài."*

### Evidence (Chuẩn B — Data Mining & Khảo sát)
**1. Số liệu mining từ Dataset thực tế (`data/discord-pack/k4_messages.csv` — 1.092 tin nhắn onboarding Khoá 4):**
- **Quy mô mẫu:** 1.092 tin nhắn (779 tin từ 202 học viên thật, 313 tin từ bot).
- **Số câu hỏi của học viên:** 274 câu hỏi (chiếm 35.2% tổng số tin nhắn của người).
- **Tỷ lệ câu hỏi chưa có ai reply trực tiếp:** 57 / 274 câu hỏi (**20.8%**).
- **Phân bổ chủ đề câu hỏi tồn:**
  - *Điểm danh / Workshop:* 52 câu (19.0%)
  - *Deadline / Nộp bài / Lab:* 31 câu (11.3%)
  - *Team / Ghép đội / Nền tảng Phoenix:* 57 câu (20.8%)
  - *Ticket / Lỗi kỹ thuật / Tài khoản:* 41 câu (15.0%)

**2. Bằng chứng lỗi từ Bản tin bot hiện tại (`data/discord-pack/k4_daily_reports.md`):**
- *Lỗi chèn chuỗi tham chiếu hỏng (String interpolation error):* Chuỗi `"nguồn tham chiếu"` bị chèn đè vào giữa từ tiếng Việt liên tục: `"nguồn tham chiếuhi chạy bước 3"`, `"health checnguồn tham chiếu"`, `"dự nguồn tham chiếuiến"`, `"nguồn tham chiếuhó nguồn tham chiếuhăn"`.
- *Lỗi cắt cụt văn bản (Truncation error):* Bản tin ngày 13/09 bị cắt cụt giữa chừng: *"Một số câu hỏi chưa được giải đá"*.
- *Lỗ hổng hành động (Actionability gap):* Bot chỉ ghi nhận *"Đã có phản hồi, chưa xác nhận đã xử lý"* hoặc *"Phản hồi tự động chưa phải hướng dẫn chính thức"*, nhưng **hoàn toàn không cung cấp link nhảy trực tiếp (Jump URL)** hay định danh kênh/tin nhắn để TA bấm vào hỗ trợ ngay.

**3. Danh sách 5 ví dụ nguyên văn từ học viên (Kèm `msg_id`):**
1. **`M69081`** (Học viên `D2313`, kênh `channel_02`, 12/09 12:04):
   > *"có điểm danh ws không ạ"*
   *(Hậu quả: Không ai trả lời. Đến 24 giờ sau, học viên này phải hỏi lại y hệt tại `M21623` ngày 13/09 11:22: "mình điểm danh ws ko ạ" mà vẫn không có reply trực tiếp).*
2. **`M30246`** (Học viên `D1253`, kênh `channel_02`, 12/09 19:51):
   > *"Tại e thấy trong sổ tay phải có xác nhận của giám đốc, nên là k biết e có phải chờ mail phản hồi k ạ???"*
   *(Hậu quả: Chờ 3.5 tiếng không ai phản hồi, phải hỏi lại lần 2 tại `M48859` lúc 23:15: "A ơi, Tại e thấy trong sổ tay phải có xác nhận của giám đốc, nên là k biết e có phải chờ mail phản hồi k ạ???").*
3. **`M99769`** (Học viên `D1224`, kênh `channel_02`, 12/09 18:57):
   > *"[@D7688] cho mình hỏi một team mấy bạn?"*
   *(Học viên tag bạn hỏi về quy chế team size nhưng bị trôi tin nhắn, không có phản hồi chính thức).*
4. **`M67317`** (Học viên `D3389`, kênh `channel_02`, 12/09 21:54):
   > *"2b vs 2a vẫn join chung được luôn ạ ?"*
   *(Câu hỏi thắc mắc ghép nhóm giữa hai level khác nhau trong đợt onboarding, không có reply).*
5. **`M33885`** (Học viên `D3923`, kênh `channel_02`, 13/09 11:23):
   > *"vào mà cứ bị out ra thì phải làm sao ạ :v"*
   *(Gặp sự cố kỹ thuật trong giờ workshop, câu hỏi bị trôi giữa luồng chat thảo luận).*

---

## §2. Impact & Quyết Định Chọn

### Bảng Impact So Sánh 3 Ứng Viên Giải Pháp

| Ứng viên giải pháp | Đối tượng & Số người gặp | Tần suất | Mỗi lần tốn gì (Chi phí / Hậu quả) | Tính khả thi trong Hackathon | Đánh giá / Quyết định |
|---|---|---|---|---|---|
| **Ứng viên 1 (Chọn):** Bản tin câu hỏi tồn (>4h) phân cụm chủ đề + Link điều hướng trực tiếp cho TA | ~15-20 TA/Mod + ~1.000 học viên khoá 4 | Hàng ngày (2-3 ca trực/ngày) | TA tốn 45-60 phút/ca lọc tay; 20.8% câu hỏi bị sót khiến học viên lo lắng, vi phạm deadline | **Rất cao:** Đã có data pack Discord thật + baseline bản tin cũ để so sánh và cải tiến vượt bậc | **CHỌN** (Bằng chứng rõ ràng từ dataset, tác động trực tiếp đến vận hành khoá học) |
| **Ứng viên 2:** AI Agent tự động phát hiện học viên bị "stuck" và chủ động DM (nhắn tin riêng) hỏi thăm | ~100-200 học viên gặp lỗi kỹ thuật/lab | Thỉnh thoảng (khi làm bài lab) | Nguy cơ gây phiền toái (spam DM học viên); vi phạm quy tắc an toàn (không tự ý gửi tin nhắn riêng khi chưa có người duyệt) | **Thấp - Trung bình:** Khó xác định ranh giới "chủ động" vs "làm phiền"; rủi ro quyền riêng tư cao | **LOẠI** (Vi phạm điều kiện an toàn & đạo đức của Track B: *không tự động gửi tin cho học viên khi chưa có người duyệt*) |
| **Ứng viên 3:** Nâng cấp Bot Q&A trả lời tự động câu hỏi logistics theo thời gian thực (Đề B1) | ~1.000 học viên | Liên tục cả ngày | Bot trả lời sai deadline hoặc suy đoán thông tin chưa chính thức sẽ gây hậu quả nặng (học viên trễ bài, mất điểm) | **Trung bình:** Cần kết nối hệ thống dữ liệu thông báo động cập nhật liên tục | **LOẠI** (Cost-of-error rất đắt: AI hallucination về deadline/điểm số gây bức xúc ngay lập tức) |

### Ứng viên ĐÃ LOẠI & Lý do:
1. **Loại Ứng viên 2 (Tự động DM học viên stuck):**
   - Vi phạm trực tiếp mục *An toàn & đạo đức* của Track B: *"không tự động gửi tin cho học viên khi chưa có người duyệt"*.
   - Học viên thường thảo luận hoặc tự fix sau vài phút; bot nhảy vào DM riêng dễ gây cảm giác bị giám sát và làm loãng thông tin hỗ trợ.
2. **Loại Ứng viên 3 (Bot Q&A logistics tự động B1):**
   - Việc trả lời tự động 100% cho học viên mang lại rủi ro sai sót rất lớn (*high cost of error*). Nếu bot trích xuất nhầm deadline từ thông báo cũ, học viên mất điểm thi. 
   - Ứng viên 1 (Hỗ trợ TA - Human-in-the-loop) an toàn hơn, AI đóng vai trò lọc và đề xuất, TA là người chốt câu trả lời cuối cùng.

### Ứng viên CHỌN & Lý do (Bằng số liệu chứng minh):
- **Bằng chứng rõ ràng và kiểm chứng được:** 57 câu hỏi chưa trả lời (20.8%) trong 3 ngày onboarding.
- **Tiết kiệm thời gian định lượng:** Mỗi ngày 3 ca trực × 2 server × 45 phút rà soát = **4.5 giờ công TA mỗi ngày** được tinh gọn xuống còn 10 phút kiểm tra bản tin tập trung.
- **Tỷ lệ phản hồi (SLA) nâng cao:** Giảm thời gian chờ phản hồi của học viên từ 4–24 giờ xuống dưới 1 giờ đối với các thắc mắc cấp thiết (deadline, workshop, điểm danh).
- **Khắc phục triệt để lỗi của hệ thống hiện tại:** Thay thế bản tin văn xuôi lỗi font và thiếu tương tác bằng Dashboard/Bản tin có cấu trúc: *Phân cụm chủ đề - Trích xuất câu hỏi tóm lược - Đính kèm Jump URL trực tiếp - Gợi ý hướng xử lý*.

---

## §3. Giải Pháp Tương Tự Đã Nghiên Cứu *(Sơ bộ)*
- **GitHub Issue Triage Bot / Stale Bot:**
  - *Flow:* Quét các issue không có hoạt động trong X ngày, gắn nhãn `needs-triage` hoặc `unanswered`.
  - *Đáng học:* Cơ chế gắn nhãn phân loại tự động và tính thời gian phản hồi (SLA).
  - *Đáng né:* Tự động đóng/bình luận máy móc khiến người dùng ức chế.
  - *Mình khác gì:* AI phân tích ngữ cảnh câu hỏi (phân biệt câu hỏi thật vs câu tán gẫu) và tạo bản tin tổng hợp kèm link cho TA duyệt xử lý, không can thiệp tự động vào học viên.

---

## §4. Thiết Kế Lát Cắt *(Sơ bộ cho CP1)*
- **Lát cắt MỘT CÂU:**
  > *"Một Trợ giảng (TA) · cuối ca trực mở bản tin tổng hợp · AI trích xuất danh sách các câu hỏi chưa được giải đáp sau 4 giờ và gom nhóm theo chủ đề kèm link tin nhắn trực tiếp · TA bấm link nhảy đến Discord và trả lời dứt điểm từng câu hỏi."*
- **Automation:** **Conditional / Augment** (AI trích xuất, gom nhóm, phát hiện câu hỏi chưa ai xử lý; Con người là TA trực tiếp duyệt và trả lời học viên).
