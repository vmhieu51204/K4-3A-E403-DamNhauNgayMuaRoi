"""
env_loader.py — Trình nạp biến môi trường (.env) thuần Python không cần thư viện ngoài.
Theo đúng đặc tả mục 3.4 & 7 trong base_architecture.md.
"""

import os
from pathlib import Path


def load_env(env_path=None, override=True):
    """
    Nạp các biến môi trường từ file .env vào os.environ.
    Hỗ trợ tìm kiếm tự động ở thư mục hiện tại và các thư mục cha.
    """
    if env_path is None:
        # Danh sách các ứng viên vị trí file .env
        candidates = [
            Path(".env"),
            Path("../.env"),
            Path("../../.env"),
            Path(__file__).resolve().parent / ".env",
            Path(__file__).resolve().parent.parent / ".env",
        ]
        for p in candidates:
            if p.exists() and p.is_file():
                env_path = p
                break

    if not env_path or not os.path.exists(env_path):
        return {}

    loaded = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            loaded[key] = val
            if override or key not in os.environ:
                os.environ[key] = val

    return loaded


# Tự động nạp khi module được import
load_env()
