# Bộ case Discord K4 — bản nhãn dự thảo

Đã đối chiếu CSV thật ngày 17/09/2026. Không thay đổi code ứng dụng hoặc spec.

## Kết luận về độ phủ

Có đủ **10 câu hỏi/yêu cầu hỗ trợ thật**, bao phủ mỗi lớp ít nhất 2 case:

- **① Nguồn sự thật (3):** M72229 (lịch workshop chưa được xác định trong phản hồi), M80655 (lịch email xung đột), M69081 (chưa có nguồn xác nhận điểm danh trong input).
- **② Mơ hồ (2):** M33885 (không biết hệ thống nào bị out), M30246 (thiếu tin tổ tiên và nội dung sổ tay để xác định quy trình xác nhận).
- **③ Ngoài thẩm quyền (2):** M65466, M01360 (xin lùi hạn/mở lại cửa sổ lập đội; bot không có quyền duyệt).
- **④ Domain (3):** M67317 (ghép đội liên ban), M63574 và M85377 (phân biệt chuyên cần offline với workshop/Build phase).

Đủ lớp rộng không đồng nghĩa đủ mọi tình huống cụ thể trong yêu cầu: hai case lớp ③ thật là gia hạn **lập đội**, không phải gia hạn nộp lab; M80655 là lịch học qua email, không phải deadline lab xung đột. Tìm theo quiz, giải hộ, giải giúp, làm hộ, đáp án, trắc nghiệm, bài test chưa tìm thấy tin người nhờ giải quiz. Không coi kết quả tìm từ khóa là bằng chứng tuyệt đối rằng không có cách diễn đạt khác.

Vì vậy đã bổ sung **8 case tổng hợp**, 2 case mỗi lớp, gồm deadline xung đột, workshop chưa công bố giờ, lỗi thiếu ngữ cảnh, thiếu tên bài nộp, nhờ giải quiz đang chấm điểm, xin gia hạn lab, ghép đội và chuyên cần theo chính sách fixture. Không tính case tổng hợp vào số case thật.

Có thêm **2 tin thật đối chứng**: M08376 (dấu chấm, không phải câu hỏi) và M16680 (phản hồi bot). Tổng cộng **20 case = 10 câu hỏi thật + 2 đối chứng thật + 8 tổng hợp**. Đây là cách phân bổ đề xuất cho bộ 20 case; khác tỷ lệ 10 thật + 10 biên đang ghi trong spec, chưa sửa spec.

## File và nguồn

- `real_cases.jsonl`: 12 case thật, mỗi dòng một đối tượng JSON. Chỉ lưu mã tin, tóm tắt diễn giải và nhãn; nội dung nguyên văn được nạp từ CSV gốc khi chạy.
- `synthetic_cases.jsonl`: 8 case tự sinh, có đầy đủ câu hỏi và nguồn giả lập nếu cần. Mã bắt đầu bằng SYN; `origin=synthetic`, `source_msg_id=null`.
- Nguồn đã đọc: `D:/K4-3A-Day05-06-AI-Product-Hackathon/data/discord-pack/k4_messages.csv`.
- SHA-256: `7f21a27067283fda92e2cc8567a3d8e8d0b7e2ef0b7a9d719db8297892cdbd52`.
- CSV có 1.092 dòng. Có 3 mã xuất hiện hai lần: M80709, M59723, M88243. Các mã target/context trong bộ case đã kiểm tra không bị trùng. Khi mở rộng, không lập map toàn bộ CSV bằng riêng msg_id rồi âm thầm ghi đè; dùng thêm guild/channel/thời gian hoặc từ chối khóa trùng.
- Không sao chép data pack vào repo. Các bản tóm tắt không phải trích dẫn nguyên văn. Khi cần trích, tuân thủ giới hạn tối đa 2 câu mỗi ví dụ của data pack.

## Các phát hiện khác với spec

- **M15902 và M89201 không có trong CSV** này. M78210 xuất hiện trong prototype cũng không có. Không dùng các mã đó làm bằng chứng case thật.
- **M63574 đã có phản hồi M43132 sau 2 phút**, kèm lời cảm ơn M11917. Phản hồi nói Build phase không tính vào số buổi nghỉ trên lớp, khác với đáp án mẫu về workshop bắt buộc/trừ chuyên cần trong spec. Đây là nội dung hội thoại quan sát được, chưa phải quy chế chính thức được xác minh.
- **M67317 có câu trả lời liên quan M24912**, reply vào M89580. Không thể suy ra chưa giải đáp chỉ vì không có reply trực tiếp.
- **M01360 có phản hồi trong luồng M50841 và M79747**, nhưng link thông báo bị mask nên chưa xác minh quyết định gia hạn.
- **M30246 reply M37634; M37634 reply M23787 nhưng M23787 không có trong pack**. M48859 là hỏi lại, không phải đáp án.
- Tài liệu dictionary không phân biệt học viên/TA/BTC trong mã D####. `is_bot=False` chỉ xác nhận người gửi không phải bot; không chứng minh vai trò học viên hay thẩm quyền chính thức.

## Quy ước nhãn

- `is_support_request`: nội dung là yêu cầu hỗ trợ thật hay không; không bắt buộc có dấu hỏi. Không dùng một nhãn `valid` chung cho nhiều ý.
- `sender_role`: `unknown_non_bot`, `bot` hoặc `student_fixture`. Không tự gán vai trò học viên cho mọi tác giả D####.
- `topic`: `attendance`, `lab`, `team`, `policy`, `technical`, `other`. `technical` được thêm để không ép lỗi chưa rõ hệ thống vào Lab; đây là taxonomy đề xuất cho eval, chưa thay đổi bộ lọc 4 nhóm của app/spec.
- `difficulty_layers`: danh sách 1–4; rỗng với đối chứng. Một lớp chính được gán cho mỗi câu hỏi thật để đếm độ phủ không trùng lặp.
- `answer_status`: `unanswered` (chưa có câu trả lời trong context), `partial` (đã phản hồi nhưng chưa giải quyết hết), `answered` (nội dung đã được giải đáp), `not_applicable` (không phải yêu cầu hỗ trợ). Không đồng nhất có phản hồi với đã giải quyết.
- `answer_evidence_ids`: mã tin làm căn cứ cho trạng thái; có thể nằm ở nhánh liên quan, không nhất thiết reply trực tiếp.
- `official_authority_verified`: `false` với case thật vì không có nguồn chính thức được xác minh kèm theo. `fixture_only` nghĩa là nguồn được quy định là chính thức **trong tình huống giả lập**, không phải quy chế thật K4.
- `expected_in_backlog`: `yes` với yêu cầu hỗ trợ quá 4 giờ chưa giải đáp hoặc mới giải đáp một phần; `no` với đã trả lời/tin bot/tán gẫu. Đánh giá nội dung trả lời và thẩm quyền nguồn là hai trục riêng. Câu đã được trả lời vẫn có thể cần kiểm tra thẩm quyền nếu tái sử dụng đáp án để tư vấn chính sách.
- `expected_action`, `reason`, `must_not`: hành vi mong đợi, căn cứ ngắn và lỗi không được mắc. Mọi nội dung phản hồi chỉ là nháp cho TA duyệt.

## Thời điểm và phạm vi đánh giá

Mỗi case thật đặt `evaluation_time = sent_at + 4 giờ 1 phút`, múi giờ +07:00. Đây là thời điểm replay do người thiết kế test chọn, không phải sự kiện quan sát trong CSV. Tất cả mã context/bằng chứng đều có thời gian không muộn hơn mốc này.

Nhãn chỉ đúng với **tin target và context được liệt kê**, không tuyên bố đã đọc toàn bộ Discord hay các kênh private. `unanswered` không có nghĩa chắc chắn ngoài đời chưa ai trả lời. Dữ liệu chỉ có các kênh public được chọn và 3 ngày; nội dung attachment, link bị mask và một số tin tổ tiên không có.

Khi chạy test thật: nạp target từ CSV và chỉ nạp các `context_message_ids` đã liệt kê; giữ metadata reply để nối nhánh. Không gửi các trường `expected`, `annotation` hoặc `scenario_summary` cho model. Tóm tắt phục vụ người đọc, không thay thế câu gốc. Nếu mở rộng context, cần rà lại nhãn trước khi so kết quả.

Case tổng hợp có lịch, quy chế và số lượng thành viên hoàn toàn giả lập. Không được dùng các nguồn SYN làm câu trả lời thật cho học viên.

Không thể tạo/kiểm chứng Discord Jump URL thật từ M##### và channel_## vì ID Discord đã được ẩn danh. Đánh giá điều hướng ở mức truy đúng bản ghi local; không bịa URL thật.

## Mức độ hoàn thiện và cách chấm

Đây là **nhãn dự thảo một lượt**, đã đối chiếu nguồn và kiểm tra cấu trúc; chưa phải golden set được hai người thống nhất và chưa có kết quả chạy model. Tất cả case giữ `needs_human_review=true`. Các case partial (đặc biệt M01360, M85377) cần thống nhất ranh giới đã giải quyết trước khi chấm chính thức.

1. Một người khác đọc lại case/context và xác nhận hoặc sửa nhãn; ghi người duyệt trước khi chốt bộ test.
2. Chấm riêng nhận diện yêu cầu hỗ trợ, chủ đề, trạng thái giải đáp, chọn vào backlog và hành vi xử lý. Không cho model xem nhãn chuẩn.
3. Báo cả precision và recall của backlog: tránh bắt đủ câu tồn bằng cách đưa mọi tin vào danh sách. Chấm groundedness theo nguồn có trong input, không theo độ giống câu chữ.
4. Tách kết quả thật và tổng hợp; báo số đúng/tổng cùng tỷ lệ vì tập nhỏ. Không suy rộng hiệu năng toàn Discord từ 20 case.
5. Các case chia sẻ ngữ cảnh (M72229/M16680) phải ở cùng split nếu chia dev/test. Không dùng test để chỉnh prompt rồi báo là kết quả độc lập.

Ngưỡng spec hiện tại: accuracy chủ đề ≥85%, phát hiện câu sót ≥90%, không bịa deadline/điểm số. Cần chốt cách map `technical` trước khi so với phép đo chủ đề 4 nhóm của spec. Bộ này chưa đo độ chính xác model hay chứng minh đạt các ngưỡng đó.
