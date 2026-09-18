# Hướng Dẫn Deploy (Chi phí 0đ) cho TA Copilot

Tài liệu này hướng dẫn cách đưa dự án lên môi trường live (Internet) nhanh chóng, hoàn toàn miễn phí, rất phù hợp cho việc làm Demo vòng Pitching (CP5/CP6).

## 1. Deploy Frontend (Miễn phí 100%)

Vì giao diện hiện tại trong thư mục `codebase/` là dạng **Static Site** (chỉ có HTML/CSS/JS thuần, sử dụng Tailwind qua CDN), việc deploy cực kỳ đơn giản. Đội FE có thể chọn 1 trong 3 nền tảng miễn phí sau:

### Lựa chọn 1: Vercel (Khuyên dùng - Nhanh nhất)
- Đăng nhập [Vercel](https://vercel.com/) bằng tài khoản GitHub.
- Bấm **Add New -> Project**.
- Import repo `K4-3A-E403-DamNhauNgayMuaRoi`.
- Ở phần **Root Directory**, nhấn Edit và chọn thư mục `codebase`.
- Bấm **Deploy**. Sau 30 giây sẽ có link public (VD: `https://ta-copilot.vercel.app`).

### Lựa chọn 2: Netlify (Kéo & Thả)
- Vào [Netlify Drop](https://app.netlify.com/drop).
- Kéo thả trực tiếp thư mục `codebase/` từ máy tính vào vòng tròn trên web.
- Netlify sẽ sinh ra một đường link live ngay lập tức. (Có thể login để đổi tên link cho đẹp).

### Lựa chọn 3: GitHub Pages
- Vào Setting của Repo GitHub -> **Pages**.
- Chọn nhánh `main`, thư mục `/root`. 
- *(Lưu ý: Nếu dùng GitHub pages thì đường link mặc định sẽ chỏ vào `README.md`, người chấm sẽ phải gõ thêm đuôi `/codebase/index.html` vào URL).*

---

## 2. Deploy Backend API (Miễn phí)
Nếu đội FE cần gọi API thật thay vì dùng Mock Data, Backend (FastAPI) có thể được host miễn phí tại:

### Render.com (Web Service)
- Đăng nhập [Render](https://render.com/).
- Tạo **New Web Service**, kết nối với Repo GitHub.
- Cấu hình:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn api:app --host 0.0.0.0 --port 10000`
- Điền các API Key (OPENAI_API_KEY...) vào phần **Environment Variables**.
- *Nhược điểm:* Bản Free sẽ bị "ngủ" (spin down) nếu 15 phút không ai gọi, khi gọi lại sẽ mất 30-50s để khởi động. Nên "đánh thức" server trước giờ thuyết trình 5 phút!

## 3. Khuyến nghị cho Demo Hackathon
Vì thời gian demo chỉ có 5 phút và Wi-Fi hội trường thường rất chập chờn:
👉 **Chiến thuật an toàn nhất:** Dùng Vercel hoặc Netlify để host cái Giao diện lên lấy link xịn xò. Nhưng khi quay video hoặc Pitching, CỨ DÙNG MOCK DATA (file `mock_questions.js`) tích hợp sẵn trên giao diện. Nó vừa nhanh, vừa không sợ sập Server Backend, vừa biểu diễn được trọn vẹn luồng UX và các tính năng AI gợi ý mà anh em mình đã cấu hình cứng!
