# TA Copilot — UI với dữ liệu Discord local

## Chạy

Từ thư mục repo:

```powershell
python codebase/server.py
```

Mở **http://127.0.0.1:8081**. Không dùng server tĩnh cũ ở cổng 8080: UI cần API Python để đọc dữ liệu. Không cần cài thư viện Python ngoài.

## Nguồn và phạm vi

- Đọc trực tiếp `data/discord-pack/k4_messages.csv`, không nhúng nội dung riêng tư vào file JS hoặc commit thêm bản sao dữ liệu.
- Dùng nhãn nháp của `eval/real_cases.jsonl` để chọn và phân loại các case đã đối chiếu. Đây không phải pipeline AI tự động phát hiện toàn bộ câu hỏi trong CSV.
- Pack hiện có 1.092 tin: 779 tin người, 313 tin bot. Trong 12 case đối chiếu có 10 yêu cầu hỗ trợ: 7 cần xem xét, 3 đã có phản hồi. Hai case còn lại là tin bot và tin không phải câu hỏi.
- Thời gian chờ tính theo mốc đánh giá riêng của từng case, không tính từ ngày hiện tại. Nhãn chỉ phản ánh ngữ cảnh đã chọn tới mốc đó, cần TA duyệt lại.
- Nội dung câu hỏi, tác giả, kênh, thời gian và ngữ cảnh lấy nguyên từ CSV. Không suy ra vai trò TA/BTC từ mã tác giả.
- Xem bản tin bot gốc `k4_daily_reports.md` trong mục Bản tin Discord.

## Thao tác

Tìm theo nội dung, mã tin, tác giả, kênh hoặc server; lọc chủ đề; sắp xếp theo thời gian. Mở câu hỏi để xem ngữ cảnh, lý do phân loại, bằng chứng phản hồi và lưu ý của nhãn nháp. Có thể sửa mẫu trả lời, lưu phản hồi, bỏ qua và đưa lại hộp thư. Nút **Đọc lại dữ liệu** nạp CSV mới nhưng giữ thao tác trong phiên.

Mẫu trả lời được soạn sẵn theo loại hành động, không phải kết quả AI. Phản hồi chỉ lưu trong bộ nhớ trình duyệt, chưa gửi Discord. Tải lại trang sẽ đặt lại thao tác. Pack đã ẩn danh không có Jump URL thật nên UI hiển thị ngữ cảnh local.

Máy chủ chỉ nghe tại `127.0.0.1`, chỉ phục vụ các asset UI và hai API đọc dữ liệu, không mở toàn bộ thư mục repo. Giữ thư mục `data/` trong gitignore. Font Google có font hệ thống dự phòng.

## Kiểm tra

```powershell
python -m unittest discover -s codebase -p "test_*.py"
```

## HAX trong UI

Banner G1 nêu phạm vi; huy hiệu G2 báo chưa có điểm AI thật. Mỗi thẻ có mục AI Reasoning (G11) ghi rõ nguồn nhãn đối chiếu. Case mơ hồ có cờ G10 và bản nháp hỏi lại; lưu chuyển sang **Chờ làm rõ**, không tăng **Đã xử lý**. TA sửa bản nháp trong modal (G9), bỏ qua một click và khôi phục được (G8). Xem mô tả đầy đủ tại `spec.md` §4b.

Giao diện bám HTML gốc: nền tối, header ngang, bốn ô thống kê, thẻ câu hỏi có ô soạn và nút lưu ngay trên thẻ. Bản nháp đồng bộ giữa thẻ và modal ngữ cảnh.
