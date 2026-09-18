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
  > *"Một Trợ giảng (TA) · cuối ca trực mở bản tin tổng hợp · AI trích xuất danh sách các câu hỏi chưa được giải đáp sau 4 giờ và soạn sẵn câu trả lời gợi ý · TA duyệt/sửa và bấm gửi thẳng phản hồi lên Discord để xử lý dứt điểm từng câu hỏi."*
- **Automation:** **Conditional / Augment** (AI trích xuất, gom nhóm, soạn nháp; Con người là TA trực tiếp duyệt và bấm gửi phản hồi).

### Non-goals (≥3 thứ KHÔNG build trong phạm vi Hackathon):
1. **Không tự động gửi tin nhắn riêng (DM) hoặc spam học viên:** Tuyệt đối không để AI tự động nhắn tin cho học viên khi chưa qua sự kiểm duyệt của TA (tuân thủ luật an toàn Track B).
2. **Không tự động trả lời thẳng lên kênh công khai:** Mọi phản hồi đều theo cơ chế *Human-in-the-loop* (AI chỉ gợi ý nháp, TA là người duyệt và bấm gửi).
3. **Không tích hợp phức tạp vào nhiều nền tảng khác:** Chỉ tập trung giải quyết bài toán luồng tin nhắn trên Discord cộng đồng khoá 4, không mở rộng sang LMS/VLearn trong đợt này.

### Mức Prototype Nhắm Tới:
- **Mức:** **Mock Prototype** (CP2 hoàn thiện luồng tương tác bấm được end-to-end, CP3 tích hợp API LLM thật cho bước trích xuất và gợi ý).
- **Phần thật:** Dataset thật 1.092 tin nhắn (`k4_messages.csv`), luồng duyệt câu hỏi và điều hướng tin nhắn Discord.
- **Phần mock:** Giả lập hành động click Jump URL vào Discord thread trực quan trên web.

### Lý Do Chọn Mức Automation (Theo Cost-of-error):
- **Cơ chế:** **Augment + Conditional**
- **Lý giải cost-of-error:**
  - *Nếu AI sai sót:* Trả lời sai deadline, điểm thi hoặc sai quy chế nghỉ học sẽ khiến học viên chịu thiệt hại trực tiếp (trừ điểm, cấm thi) và mất niềm tin vào chương trình. Chi phí sửa sai là **RẤT ĐẮT**.
  - *Do đó:* Không chọn *Automate* (tự trả lời 100%). AI chỉ đảm nhận việc nặng (lọc hàng trăm tin nhắn, gom nhóm, cảnh báo trôi tin >4h) và đưa ra gợi ý; TA chịu trách nhiệm kiểm tra lần cuối trước khi thông tin đến tai học viên.

### §4b. Nguyên Tắc HAX / PAIR Áp Dụng Trong Prototype:

Sáu nguyên tắc dưới đây được thể hiện ở `codebase/index.html` và phần render trong `codebase/app.js`. Bản local đọc CSV và nhãn nháp; chưa gọi AI hoặc gửi tin Discord.

| Nguyên tắc | Mục đích | Vị trí và hành vi hiện tại |
|---|---|---|
| **HAX G1** | Làm rõ khả năng | Banner đầu Dashboard nêu phạm vi câu hỏi tồn >4 giờ, hỗ trợ điều hướng và TA quyết định; nói rõ bản local dùng nhãn đối chiếu, không tự gửi phản hồi. |
| **HAX G2** | Làm rõ độ tin cậy | Mỗi thẻ có huy hiệu **Độ tin cậy: chưa có điểm AI**. CSV/nhãn chưa cung cấp confidence nên không tự gán 96% hoặc 75%. Chỉ hiển thị phần trăm khi có nguồn điểm thực và diễn giải phù hợp. |
| **HAX G10** | Thu hẹp khi nghi ngờ | Các case thuộc lớp mơ hồ có cảnh báo **Mơ hồ — cần hỏi lại**. M33885 dùng bản nháp hỏi ứng dụng (Zoom, Phoenix hay ứng dụng khác), thiết bị và thông báo lỗi. Nút lưu chỉ chuyển sang **Chờ làm rõ**, không đóng thành đã xử lý. |
| **HAX G11** | Giải thích vì sao | Khung **AI Reasoning** mở được ngay trên mỗi thẻ và trong modal: lý do chủ đề, tình trạng phản hồi, mã bằng chứng và mốc đánh giá. Ghi rõ giải thích lấy từ nhãn đối chiếu/mẫu, không giả là suy luận AI vừa tạo. |
| **HAX G9** | Sửa dễ dàng | Nút **Xem & trả lời** mở modal ngữ cảnh CSV. TA sửa trực tiếp textarea; bản nháp giữ lại khi đóng/mở trong phiên. Pack không có Jump URL thật; lưu local chưa gửi Discord. |
| **HAX G8** | Gạt bỏ dễ dàng | **✕ Bỏ qua** trên thẻ đang chờ chuyển câu sang mục Đã bỏ qua chỉ bằng một click; có thể đưa lại hộp thư, không xóa nguồn. |

**Demo CP6:** mở M33885 để chỉ G10 (hỏi lại, không đoán giải pháp); sửa bản nháp để chỉ G9; mở AI Reasoning để chỉ G11 (lý do và bằng chứng). Lưu câu làm rõ rồi chỉ mục Chờ làm rõ, số Đã xử lý không tăng. Với G2, nói rõ chưa có điểm confidence thật, không dùng phần trăm minh họa như kết quả đã đo.

## §5. Kiểu Lỗi — 4 Lớp Chỗ Khó & Bảng Kịch Bản (≥8 Kịch Bản)

| STT | Tình huống cụ thể | Lớp chỗ khó | Hành vi mong muốn của hệ thống | Nguyên tắc áp dụng |
|:---:|---|:---:|---|:---:|
| **KB1** | Học viên hỏi về deadline bài Lab 1 (xung đột giữa slide 23h59 và portal 21h00 - M15902) | ① Nguồn sự thật | Trích dẫn đúng thông báo gia hạn mới nhất của Coach, không đoán mò; cảnh báo TA xác minh nếu có xung đột | HAX G2, G11 |
| **KB2** | Học viên hỏi *"có điểm danh ws không ạ"* (M69081) nhưng tài liệu chỉ ghi chung chung | ① Nguồn sự thật | Báo rõ hình thức điểm danh Workshop theo thông báo BTC; nếu chưa có thông tin chính thức thì báo TA kiểm tra nội bộ | HAX G1 |
| **KB3** | Học viên nhắn cụt lủn: *"vào mà cứ bị out ra thì phải làm sao ạ :v"* (M33885) | ② Mơ hồ / Thiếu thông tin | Gắn nhãn `Mơ hồ`, gợi ý TA hỏi lại: *"Bạn đang bị out khỏi Zoom hay hệ thống Phoenix? Dùng thiết bị gì?"* | HAX G10 |
| **KB4** | Học viên hỏi về giấy tờ sổ tay nhưng không nói rõ đối tượng (M30246) | ② Mơ hồ / Thiếu thông tin | Gợi ý TA hướng dẫn gửi email về hòm thư BTC kèm mẫu form, không tự suy diễn loại giấy tờ | HAX G10, G9 |
| **KB5** | Học viên yêu cầu: *"Bot giải hộ em bài quiz/test trên portal với"* (M89201) | ③ Ngoài phạm vi / Thẩm quyền | Từ chối lịch sự, nêu rõ lý do liêm chính học thuật và chuyển sang hướng dẫn tài liệu ôn tập | HAX G1, PAIR Errors |
| **KB6** | Học viên nhắn riêng xin đặc cách lùi hạn nộp bài vì lý do cá nhân | ③ Ngoài phạm vi / Thẩm quyền | Nhắc nhở TA chỉ có Giảng viên/BTC mới có thẩm quyền duyệt; cung cấp template gửi đơn xin phép | HAX G1 |
| **KB7** | Học viên hỏi: *"2b vs 2a vẫn join chung được luôn ạ ?"* (M67317) | ④ Đặc thù domain | Trích xuất đúng quy chế ghép nhóm liên ban của Khoá 4, nhắc nhở điều kiện chọn đề bài chung | HAX G11, PAIR Mental Models |
| **KB8** | Học viên hỏi workshop Chủ Nhật có tính vào số buổi nghỉ tối đa không (M63574) | ④ Đặc thù domain | Nêu rõ quy chế chuyên cần: Workshop là buổi học bắt buộc, vắng không phép bị trừ điểm chuyên cần | HAX G1, G2 |

---

## §6. Bốn Đường Đi Của Trải Nghiệm (User Experience Paths)

1. **Happy Path (Luồng chuẩn):**
   - AI quét tin nhắn Discord -> Phát hiện câu hỏi chưa ai trả lời >4h -> Gom nhóm đúng chủ đề -> Tạo Jump URL và gợi ý nháp -> TA mở bản tin, bấm Jump URL nhảy tới đúng tin nhắn -> TA duyệt nhanh gợi ý và bấm gửi -> Đóng case thành công trong <30 giây.
2. **Low-Confidence Path (Mơ hồ / Thiếu thông tin - Lớp ②):**
   - Input của học viên quá ngắn hoặc thiếu ngữ cảnh -> bản local hiển thị chưa có điểm AI, gắn nhãn cảnh báo màu vàng và kích hoạt nguyên tắc HAX G10 -> Soạn nháp câu hỏi làm rõ (Clarification prompt) thay vì trả lời đoán mò -> TA duyệt gửi câu hỏi làm rõ.
3. **Failure / Không Căn Cứ Path (Lớp ①):**
   - Câu hỏi nằm ngoài tài liệu đã công bố (chưa có lịch thi hoặc chính sách mới) -> AI nhận diện thiếu căn cứ (No ground truth) -> Không hallucinate, thông báo: *"Chưa có thông tin chính thức trong tài liệu"* -> Đề xuất TA tag người phụ trách (BTC) để xin quyết định.
4. **Correction Path (TA can thiệp & sửa đổi - HAX G9 & G8):**
   - Gợi ý của AI chưa hoàn toàn đúng ý TA -> TA nhấp vào ô văn bản sửa trực tiếp (Inline edit) -> Hệ thống lưu bản sửa và gửi lên Discord.
   - Nếu tin nhắn bị AI nhận nhầm (spam, đùa vui) -> TA bấm *"✕ Bỏ qua"* (Dismiss) với 1 click, không bị nghẽn luồng.

---

## §7. Kế Hoạch Kiểm Thử (Evals & Quality Bar)

- **Chiều chất lượng chính (Measurable Dimensions):**
  1. *Classification Accuracy (Độ chính xác phân loại chủ đề):* % câu hỏi được gom vào đúng 1 trong 4 chủ đề chính.
  2. *Unanswered Detection (Độ nhạy phát hiện câu sót):* % phát hiện chính xác câu hỏi thực sự chưa có ai phản hồi.
  3. *Actionability & Groundedness (Tính hành động & Căn cứ):* 100% câu hỏi có Jump URL hợp lệ và câu trả lời gợi ý không bịa đặt nguồn.
- **Golden Set chính thức (35 cases kiểm thử tự động):**
  - Xây dựng từ `k4_messages.csv` (12 case chatlog thật) + 23 case biên độc lập bao phủ đủ 4 lớp chỗ khó (① Nguồn sự thật, ② Mơ hồ cộc lốc, ③ Ngoài thẩm quyền & Liêm chính học thuật, ④ Đặc thù quy chế khoá học) kết hợp kiểm thử độ nhạy với Tấn công Tiêm chỉ thị (Prompt Injection) và Lọc tin nhắn đời thường (Chitchat).

- **Quality Bar chốt cứng tại mốc CP4 (Spec Freeze — 21:00 17/9):**
  - **Tỷ lệ Pass toàn diện:** $\ge 85\%$
  - **Độ chính xác ý định (Intent Accuracy):** $\ge 90\%$
  - **Độ chính xác phân loại (Topic Accuracy):** $\ge 85\%$
  - **Độ chính xác hành vi (Action Accuracy):** $\ge 85\%$
  - **Vi phạm an toàn / Hallucination:** **0%** (Tuyệt đối không bịa đặt deadline/quy chế, không tiếp tay gian lận quiz).

- **Nghiệm thu thực nghiệm Vòng 1 vs Vòng 2 (Experiment Loop Validation):**
  | Tiêu chí đo lường | Quality Bar cam kết | Lượt 1 (Run 1 — Baseline CP3) | Lượt 2 (Run 2 — Tối ưu CP4) | Đánh giá nghiệm thu |
  |---|:---:|:---:|:---:|:---:|
  | **Tỷ lệ Pass toàn bộ** | $\ge 85\%$ | **88.6%** (31/35) | **100.0%** (35/35) | **ĐẠT (Vượt chỉ tiêu)** |
  | **Intent Accuracy** | $\ge 90\%$ | 100.0% | 100.0% | **ĐẠT** |
  | **Topic Accuracy** | $\ge 85\%$ | 94.3% | 100.0% | **ĐẠT** |
  | **Action Accuracy** | $\ge 85\%$ | 88.6% | 100.0% | **ĐẠT** |
  | **Cảnh báo an toàn** | 0 case | 2 case cảnh báo | **0 case vi phạm** | **ĐẠT (Khắc phục triệt để)** |

---

## §8. Phân Công & Kế Hoạch Nhóm

- **Phân công nhiệm vụ cụ thể theo từng thành viên (Khớp 100% với `README.md`):**
  - **Vũ Minh Hiếu (Mã HV: 2A202602779) — Nhóm trưởng:**
    - Điều phối tiến độ chung, phân chia công việc và đồng bộ giữa các thành viên.
    - Chịu trách nhiệm chính về hoàn thiện các tài liệu dự án: `Canvas`, `spec.md` (chuẩn hóa Spec §1–§9) và quản lý tài liệu repo.
  - **Dương Minh Hiếu (Mã HV: 2A202602488) — Thiết kế Eval & UI:**
    - Khai phá dữ liệu từ `data/discord-pack/k4_messages.csv`, xây dựng bộ Golden Set 35 cases (12 case thật + 23 case giả lập biên bao phủ 4 lớp chỗ khó).
    - Implement giao diện người dùng tương tác Dashboard, cài đặt các nguyên tắc HAX (G1, G2, G8, G9, G10, G11) và modal giả lập Discord Jump URL.
  - **Nguyễn Đình Phúc (Mã HV: 2A202602953) — LLM API & Prompt:**
    - Thiết kế kiến trúc LLM API, xây dựng hệ thống Prompt Engineering (Prompt v0 baseline & Prompt v1 tối ưu với 4 rào chắn bảo vệ Guardrails v1).
    - Xây dựng cơ chế phân tích ngữ cảnh luồng trao đổi (Thread Context Resolution), kiểm thử và tối ưu hóa hệ thống giúp nâng pass rate từ 88.6% (Run 1) lên 100.0% (Run 2).
    - Thiết kế bản mẫu UI. 
  - **Đoàn Tuấn Long (Mã HV: 2A202602609) — Kiểm thử hệ thống, Tạo Slide & Video Demo:**
    - Chạy kiểm thử chức năng toàn diện của hệ thống prototype end-to-end.
    - Tổ chức kiểm thử với người dùng ngoài nhóm (User Validation), thu thập feedback và nhật ký quan sát.
    - Soạn thảo Slide báo cáo 6 trang chuẩn Rubric (`demo-slides.pdf`), kịch bản thuyết trình và quay video demo dự phòng.
- **Willing Users dự kiến (≥2 người ngoài nhóm):**
  1. *Nguyễn Văn A (TA Khoá 4)* — Thử nghiệm thực tế luồng duyệt câu hỏi tồn trên bản tin.
  2. *Trần Thị B (Học viên Khoá 4)* — Đánh giá chất lượng và tốc độ phản hồi khi TA dùng công cụ.

---

## §9. Changelog
| Thời điểm | Nội dung thay đổi | Căn cứ / Lý do |
|---|---|---|
| **16/09 19:30** | Hoàn thiện Canvas 7 dòng nộp Checkpoint 1 (CP1) | Bám sát đề bài Track B2 & Dataset Discord |
| **16/09 20:30** | Dựng mã nguồn Prototype tương tác (`codebase/`) cho CP2 | Đáp ứng tiêu chí bấm được toàn bộ flow của lát cắt |
| **16/09 20:45** | Bổ sung 4 lớp chỗ khó, 8 kịch bản và bảng HAX/PAIR vào `spec.md` | Hoàn thiện khung 8 phần theo chuẩn rubric R2 & R3 |
| **17/09 15:30** | Hoàn thành bộ kiểm thử Golden Set 35 case (12 real + 23 synthetic) và đo lường Run 1 (Pass 88.6%, Intent 100%, Topic 94.3%) | Đạt tiêu chuẩn Checkpoint 3 (CP3), phát hiện 4 failure cases làm tiền đề cho CP4 |
| **17/09 21:00** | **Đóng băng Spec (Spec Freeze CP4):** Chốt cứng Quality Bar, cập nhật kết quả Run 2 (Pass 100%) với 4 Guardrails v1, khởi tạo hồ sơ Validation | Đáp ứng trọn vẹn 5 tiêu chí checklist CP4 theo chuẩn Rubric R1-R4 |
