"""
tools/_shared.py — Các tiện ích dùng chung và lớp phòng thủ an toàn (Safety Guardrails)
Theo đúng mục 3.7 trong base_architecture.md:
Layer 2 Implementation Guards (Ngăn chặn prompt injection, kiểm tra confirmed write action).
"""

import json
import re
from pathlib import Path

# Các mẫu phát hiện tiêm chỉ thị độc hại (Prompt Injection & Trojan payloads)
INJECTION_PATTERNS = [
    re.compile(r"\[SYSTEM\s+DIRECTIVE", re.IGNORECASE),
    re.compile(r"Administrative\s+Test\s+Mode", re.IGNORECASE),
    re.compile(r"IMPORTANT\s+INSTRUCTION\s+FOR\s+AI", re.IGNORECASE),
    re.compile(r"TERMINATE\s+ALL\s+PREVIOUS", re.IGNORECASE),
]

SENSITIVE_DATA_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"password\s*=\s*", re.IGNORECASE),
]


def check_forged_payload(text: str) -> bool:
    """Kiểm tra xem nội dung văn bản có chứa chỉ thị prompt injection hay không."""
    if not text:
        return False
    return any(p.search(text) for p in INJECTION_PATTERNS)


def check_sensitive_data(text: str) -> bool:
    """Kiểm tra xem văn bản có làm rò rỉ API key hoặc mật khẩu nhạy cảm không."""
    if not text:
        return False
    return any(p.search(text) for p in SENSITIVE_DATA_PATTERNS)


def get_data_dir() -> Path:
    """Trả về thư mục chứa dữ liệu domain (data/)."""
    root = Path(__file__).resolve().parent.parent
    return root / "data"


def load_official_rules() -> dict:
    """Nạp cơ sở dữ liệu quy chế khoá học chính thức."""
    rules_file = get_data_dir() / "official_rules.json"
    if rules_file.exists():
        with open(rules_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
