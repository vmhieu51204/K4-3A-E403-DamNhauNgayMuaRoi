"""
tools/search_kb/tool.py — Tool tra cứu quy chế, lịch học và deadline chính thức
"""

from typing import Any
from tools._shared import load_official_rules


def search_course_kb(query: str, category: str | None = None) -> dict[str, Any]:
    """
    Tìm kiếm thông tin chính thức từ cơ sở dữ liệu quy chế khoá học.
    """
    rules = load_official_rules()
    query_lower = query.lower()

    # Dữ liệu quy chế mặc định K4 nếu chưa nạp file
    kb_records = [
        {
            "id": "KB-ATTENDANCE-01",
            "category": "attendance",
            "title": "Quy chế điểm danh lớp học và Workshop",
            "content": "Lớp học offline: vắng tối đa 4 buổi; Workshop online: tự nguyện tham gia không tính vào giới hạn vắng offline. Đi muộn > 15 phút tính 0.5 buổi vắng.",
            "citation": "Sổ tay học viên K4 §2.1"
        },
        {
            "id": "KB-LAB-01",
            "category": "lab_deadline",
            "title": "Hạn nộp và quy định chấm bài Lab 1",
            "content": "Hạn nộp Lab 1 chính thức là 23:59 ngày 17/09/2026 trên Portal. Nộp muộn sau giờ này trừ 10% mỗi giờ, quá 24h không nhận bài.",
            "citation": "Thông báo môn học #lab-announcements"
        },
        {
            "id": "KB-TEAM-01",
            "category": "team_rule",
            "title": "Quy chế lập đội bài tập lớn",
            "content": "Mỗi đội bắt buộc từ 4 đến 5 thành viên. Học viên cùng khoá được phép ghép đội liên ban (Ban A và Ban B) nếu cùng level.",
            "citation": "Quy chế Hackathon K4 §4.3"
        },
        {
            "id": "KB-POLICY-01",
            "category": "general_policy",
            "title": "Thẩm quyền gia hạn và thi cử",
            "content": "Trợ giảng và Bot KHÔNG có thẩm quyền gia hạn nộp bài riêng hoặc miễn thi. Mọi đơn xin gia hạn đặc biệt phải gửi email cho Ban Tổ Chức.",
            "citation": "Quy định liêm chính học thuật AI20k"
        }
    ]

    matched = []
    for r in kb_records:
        if category and r["category"] != category:
            continue
        # So khớp từ khoá đơn giản
        score = 0
        for word in query_lower.split():
            if len(word) > 2 and (word in r["title"].lower() or word in r["content"].lower()):
                score += 1
        if score > 0 or not query_lower:
            matched.append(r)

    if not matched:
        matched = kb_records[:2]

    return {
        "status": "success",
        "query": query,
        "results_count": len(matched),
        "results": matched
    }
