# Reflection Cá Nhân - Hackathon AI20K Khoá 4

**Họ và tên:** Nguyễn Đình Phúc
**Mã học viên:** 2A202602953
**Lớp:** 3A
**Nhóm:** K4-3A-E403-DamNhauNgayMuaRoi
**Vai trò:** LLM API, prompt (Thiết kế hệ thống LLM API, tool calling, prompt engineering. Kiểm thử và tối ưu hệ thống)

## 1. Mục tiêu cá nhân & Kết quả đạt được
**Mục tiêu:** Xây dựng một kiến trúc LLM Backend ổn định, chuẩn xác và tách rời (decoupled) hoàn toàn với UI, đảm bảo AI có khả năng xử lý các tình huống phức tạp của TA Copilot với tỷ lệ chính xác cao.
**Kết quả:** 
- Triển khai thành công kiến trúc 5 lớp (Layered Architecture) với các module tách biệt: `providers`, `tools`, `eval`, `chat`, và API Server (`api.py`).
- Tối ưu hóa System Prompt và tích hợp Guardrails (bằng file YAML) để xử lý các case rủi ro, đẩy tỷ lệ vượt qua bài test (Pass rate) từ 88.6% (Run 1) lên tuyệt đối 100% (Run 2) ở Checkpoint 4.

## 2. Thách thức kỹ thuật & Cách giải quyết
**Thách thức:** Hệ thống nguyên khối ban đầu (`run_eval.py` dài 866 dòng) khiến việc bảo trì, mở rộng và tích hợp giao diện Frontend gần như bất khả thi. Hơn nữa, việc hardcode các luật an toàn (Guardrails) trực tiếp vào code Python khiến việc tinh chỉnh trở nên cứng nhắc.
**Cách giải quyết:** 
- Tiến hành mổ xẻ và refactor toàn bộ mã nguồn. Tách `DOMAIN_ONTOLOGY` và `GUARDRAIL_REGISTRY` ra thành các file cấu hình `.yaml`. 
- Đóng gói toàn bộ logic hội thoại vào lớp `TACopilotAgent` và bọc ngoài bằng FastAPI để Frontend có thể dễ dàng gọi qua REST API. Đặc biệt, thiết kế cơ chế fallback Heuristic Mock Engine khi Live API gặp sự cố (như lỗi token, quá tải), đảm bảo hệ thống luôn hoạt động ổn định.

## 3. Bài học kinh nghiệm sâu sắc nhất từ Case Thất Bại của nhóm
**Case thất bại điển hình:** `REAL-M33885` (Lớp chỗ khó ② — Tin nhắn cộc lốc, mơ hồ)
**Dữ liệu thực tế:** Học viên gửi tin nhắn: *"vào mà cứ bị out ra thì phải làm sao ạ :v"*.
**Hiện tượng lỗi ở Lượt 1 (Run 1):** Mặc dù AI nhận diện đúng chủ đề kỹ thuật (technical), nhưng lại tự tin chọn hành động `action: answer` và vội vã đưa ra lời khuyên phỏng đoán: *"Bạn thử xóa cache trình duyệt hoặc thử lại bằng tab ẩn danh"*.
**Kết quả kiểm thử:** FAIL do vi phạm tiêu chuẩn hành vi kỳ vọng (`expected_action: clarify`).
**Phân tích nguyên nhân:** Đứng từ góc độ thiết kế Prompt và LLM, đây là lỗi do bản tính cố gắng làm hài lòng người dùng (eagerness to help) của mô hình. Khi thiếu dữ liệu trầm trọng (không rõ out khỏi Zoom hay Phoenix), AI thà "đoán mò" còn hơn là hỏi lại. Điều này vô cùng nguy hiểm trong thực tế vì sẽ khiến học viên làm theo lời khuyên sai.
**Cách giải quyết:** Tôi đã thiết kế lại Prompt v1 và bổ sung Guardrail 1 áp dụng nguyên tắc HAX G10 (Thu hẹp phạm vi khi nghi ngờ): Bắt buộc AI nếu gặp tin nhắn dưới 15 từ, thiếu ngữ cảnh thì phải chọn hành động `clarify` để hỏi lại thay vì tự phỏng đoán. Nhờ đó, ở Run 2 case này đã PASS 100%.
**Bài học:** Ở góc độ kỹ sư AI, một hệ thống tốt không phải là cố gắng trả lời mọi câu hỏi, mà là hệ thống biết "ngại", biết giới hạn của mình (HAX G10) và biết đẩy quyền quyết định về phía con người (Human-in-the-loop) khi dữ liệu quá mờ nhạt.

## 4. Tự đánh giá & Cam kết trách nhiệm (Vibe-Coding Check)
Tôi tự chịu trách nhiệm về toàn bộ kiến trúc lõi (Backend, Agent Loop, Evaluator) của dự án.
- Tôi hiểu rõ luồng đi của dữ liệu từ khi người dùng nhập câu hỏi vào API, cách `TACopilotAgent` lấy ngữ cảnh (history), nạp tool từ `tools.yaml`, và cách `Provider` xử lý việc gọi API.
- Tôi nắm rõ từng dòng code trong quá trình tái cấu trúc file `run_eval.py` thành hệ thống đánh giá tự động nhiều module.
- Tôi hoàn toàn có khả năng giải thích cách Heuristic Mock Engine tự động kích hoạt khi API Key bị vô hiệu hóa, cũng như cách Parse Guardrails từ YAML để đưa ra quyết định mà không cần đến code tĩnh (hardcode).
