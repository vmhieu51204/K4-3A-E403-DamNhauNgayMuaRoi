# Báo Cáo Thu Hoạch Cá Nhân (Individual Reflection) — Mini Hackathon AI

- **Họ và tên:** Dương Minh Hiếu
- **Mã học viên:** 2A202602488
- **Nhóm:** K4-3A-E403-DamNhauNgayMuaRoi
- **Lớp:** 3A · **Phòng thi:** E403 · **Cụm:** Zone 2
- **Track dự thi:** Track B · Trợ lý Discord (Đề B2: Bản Tin Câu Hỏi Tồn & Điều Hướng Trực Tiếp Cho TA)
- **Vai trò chính:** Thiết kế eval và UI — tạo bộ test case theo các trường hợp, triển khai giao diện prototype.

## 1. Phần việc và đóng góp cụ thể trong dự án

Với vai trò phụ trách thiết kế eval và triển khai UI, tôi tập trung vào hai mục tiêu: kiểm tra hệ thống có đưa ra hành động phù hợp cho từng tình huống hay không và giúp trợ giảng thao tác được trên những kết quả đó.

### Thiết kế bộ eval và chia test case theo tình huống

- Tham gia xây dựng bộ case thật và case tổng hợp, phân chia theo bốn lớp chỗ khó: nguồn thông tin cần xác minh; câu hỏi mơ hồ hoặc thiếu ngữ cảnh; yêu cầu ngoài phạm vi hoặc thẩm quyền; tình huống đặc thù của khóa học.
- Với case thật, đối chiếu mã tin nhắn, nội dung gốc, kênh, thời gian gửi và các tin liên quan trong CSV. Chú ý mốc đánh giá để không dùng phản hồi xuất hiện sau thời điểm đó làm bằng chứng.
- Xác định hành vi kỳ vọng cho từng trường hợp: hỏi lại khi thiếu thông tin, xác minh nguồn khi chưa có căn cứ, chuyển người có thẩm quyền khi cần quyết định, loại khỏi backlog khi đã có phản hồi hoặc không phải câu hỏi hỗ trợ.
- Bổ sung góc nhìn kiểm thử đối với các trường hợp dễ gây nhầm: tin bot, tin chào hỏi hoặc tán gẫu, phản hồi nằm trong nhánh liên quan thay vì reply trực tiếp, câu đã có phản hồi nhưng chưa được giải đáp đầy đủ.
- Tham gia hoàn thiện cách chạy eval và đọc kết quả theo từng case để phân biệt sai chủ đề, sai trạng thái phản hồi và sai hành động. Không coi việc thiếu dữ liệu hoặc bỏ qua một case là kiểm thử đạt.

### Thiết kế và triển khai UI cho trợ giảng

- Triển khai giao diện bằng HTML, CSS và JavaScript dựa trên prototype HTML của nhóm: nền tối, thanh điều hướng phía trên, bốn ô thống kê và danh sách thẻ câu hỏi.
- Kết nối giao diện với dữ liệu trong `data/discord-pack` qua máy chủ Python local. Hiển thị nội dung câu hỏi, mã tác giả, kênh và ngữ cảnh từ CSV thay cho dữ liệu minh họa viết tay.
- Hoàn thiện các thao tác tìm kiếm, lọc chủ đề, sắp xếp, xem ngữ cảnh, chỉnh sửa bản nháp, lưu phản hồi và bỏ qua câu hỏi. Phân biệt câu đã có phản hồi trong nguồn với câu TA vừa xử lý trong phiên.
- Đưa ô soạn trả lời ngay trên từng thẻ; đồng bộ bản nháp với modal ngữ cảnh để TA có thể kiểm tra và sửa câu chữ thuận tiện.
- Cài cắm các điểm HAX: banner làm rõ khả năng (G1), thông báo giới hạn độ tin cậy (G2), yêu cầu hỏi lại khi mơ hồ (G10), giải thích lý do và bằng chứng (G11), sửa bản nháp dễ dàng (G9), bỏ qua và khôi phục câu hỏi (G8).
- Với case cần làm rõ, thao tác lưu đưa câu hỏi sang **Chờ làm rõ**, không tăng số **Đã xử lý**. Giao diện cũng ghi rõ phản hồi chỉ lưu trong phiên local, chưa gửi lên Discord.

## 2. Trải nghiệm cộng tác cùng AI (AI Co-working & Prompting)

Tôi sử dụng trợ lý AI để hỗ trợ viết mã, đề xuất tình huống kiểm thử và điều chỉnh UI. Qua quá trình làm việc, tôi nhận thấy chất lượng đầu ra phụ thuộc nhiều vào việc cung cấp đúng dữ liệu, mô tả rõ hành vi mong muốn và kiểm tra lại kết quả.

### Điểm AI hỗ trợ tốt nhất

- **Mở rộng góc nhìn kiểm thử:** AI giúp gợi ý các trường hợp biên để bộ eval không chỉ gồm những câu hỏi dễ. Tôi cần đối chiếu lại từng gợi ý với dữ liệu và phạm vi sản phẩm trước khi sử dụng.
- **Tăng tốc triển khai UI:** AI hỗ trợ dựng bố cục, bộ lọc, modal, ô soạn trả lời và các trạng thái giao diện. Điều này giúp tôi tập trung hơn vào luồng xử lý của TA và tính nhất quán giữa UI với bộ case.
- **Hỗ trợ kiểm tra hành vi:** AI giúp kiểm tra các luồng như không lưu câu trả lời rỗng, giữ bản nháp khi đóng rồi mở modal, cập nhật số đếm và không đánh dấu hoàn tất đối với câu hỏi còn thiếu thông tin.

### Hạn chế của AI và sự can thiệp của tôi

- **Tự diễn giải yêu cầu thiết kế quá rộng:** Khi tôi yêu cầu làm UI theo HTML có sẵn, phiên bản đầu được đổi sang nền sáng và sidebar, khác bố cục gốc. Tôi đã cung cấp ảnh tham chiếu và yêu cầu quay lại nền tối, bố cục giữa trang, ô trả lời ngay trên thẻ. Bài học là cần chỉ rõ phần được phép thay đổi và phần phải bám sát mẫu.
- **Dữ liệu minh họa không thay thế được dữ liệu thật:** Phiên bản đầu dùng các câu mẫu nên có thể mô tả sai nội dung hoặc trạng thái phản hồi của một mã tin. Tôi yêu cầu nối trực tiếp thư mục dữ liệu, kiểm tra ngữ cảnh và tách các câu đã có phản hồi khỏi nhóm đang chờ.
- **Hiển thị phải đúng với khả năng thực tế:** Huy hiệu phần trăm độ tin cậy trông thuyết phục nhưng không có ý nghĩa nếu nguồn chưa cung cấp điểm AI. Trong bản local, tôi chọn hiển thị “chưa có điểm AI”; phần giải thích cũng ghi rõ là từ nhãn đối chiếu, không giả là kết quả AI vừa tạo.
- **Có giao diện chưa đồng nghĩa có tích hợp hoàn chỉnh:** Tôi phân biệt rõ thao tác lưu local với gửi tin thật lên Discord. Pack đã ẩn danh không có Jump URL thật nên giao diện chỉ mở ngữ cảnh local, tránh làm người dùng hiểu nhầm.

3. Bài học kinh nghiệm sâu sắc nhất từ Case Thất Bại của nhóm
Case thất bại điển hình: REAL-M33885 (Lớp chỗ khó ② — Tin nhắn cộc lốc, mơ hồ)
Dữ liệu thực tế: Học viên gửi tin nhắn: "vào mà cứ bị out ra thì phải làm sao ạ :v".
Hiện tượng lỗi ở Lượt 1 (Run 1):
AI nhận diện đúng chủ đề kỹ thuật (technical), nhưng lại tự tin chọn hành động action: answer và vội vã đưa ra lời khuyên phỏng đoán: "Bạn thử xóa cache trình duyệt hoặc thử lại bằng tab ẩn danh".
Kết quả kiểm thử: FAIL do vi phạm tiêu chuẩn hành vi kỳ vọng (expected_action: clarify).
Phân tích nguyên nhân:
Đây là lỗi điển hình của mô hình ngôn ngữ lớn: thiên kiến cố gắng làm hài lòng người dùng (eagerness to help) dẫn đến việc "đoán mò" khi thiếu dữ liệu đầu vào trầm trọng (học viên không nói rõ out khỏi Zoom, Phoenix hay Discord). Nếu áp dụng trong thực tế, lời khuyên sai này sẽ khiến học viên hoang mang và tốn thời gian vô ích.
Cách nhóm đã giải quyết:
Chúng tôi áp dụng triệt để nguyên tắc HAX G10 (Thu hẹp phạm vi khi nghi ngờ) vào Prompt v1 và Guardrail 1: Nếu tin nhắn dưới 15 từ, thiếu chủ ngữ hoặc không nêu rõ hệ thống gặp sự cố, AI bắt buộc phải chọn hành động clarify để soạn câu hỏi làm rõ, tuyệt đối không được tự ý phỏng đoán giải pháp.
Ở Lượt 2 (Run 2), case này đã chuyển sang PASS 100%.
Bài học tư duy sản phẩm AI lớn nhất rút ra:
"Sản phẩm AI tốt không phải là sản phẩm luôn cố gắng trả lời mọi thứ, mà là sản phẩm biết rõ giới hạn của mình: biết khi nào cần dừng lại để hỏi làm rõ (HAX G10) và biết giữ con người trong vòng lặp quyết định (Human-in-the-loop) khi chi phí sai sót là đắt."

## 4. Tự đánh giá & Cam kết trách nhiệm (Vibe-Coding Check)

Tôi đã tham gia thiết kế bộ eval theo các tình huống và triển khai UI phục vụ luồng xử lý câu hỏi tồn của trợ giảng. Đóng góp của tôi nằm ở việc kết nối yêu cầu kiểm thử với hành vi có thể quan sát và thao tác trên giao diện.

Tôi hiểu cách dữ liệu đi từ CSV và bộ nhãn đối chiếu tới danh sách câu hỏi; biết phân biệt nội dung nguồn, nhãn kỳ vọng, mẫu trả lời và kết quả AI. Tôi có thể giải thích vì sao một câu cần hỏi lại, vì sao có phản hồi trực tiếp chưa chắc đã giải quyết xong, và vì sao phải xem cả ngữ cảnh liên quan tại đúng mốc đánh giá.

Tôi có thể trình bày luồng tìm kiếm, lọc, xem ngữ cảnh, sửa bản nháp, lưu phản hồi, bỏ qua và khôi phục; đồng thời chỉ ra cách G10, G9 và G11 được thể hiện trong UI. Tôi cũng nhận rõ giới hạn hiện tại: danh sách dùng nhãn nháp của các case đã đối chiếu, chưa phải AI quét toàn bộ CSV; bản nháp là mẫu soạn sẵn; thao tác chưa gửi Discord và chưa lưu bền vững qua lần tải lại trang.

Tôi cam kết chịu trách nhiệm giải thích phần eval và UI mình phụ trách, kiểm tra mã do AI hỗ trợ tạo ra và trình bày trung thực những gì đã làm được, những gì mới là mô phỏng. Nếu tiếp tục phát triển, tôi sẽ ưu tiên bổ sung case khó, rà soát nhãn cùng thành viên khác và kiểm thử giao diện trực tiếp với người dùng trước khi mở rộng tích hợp.
