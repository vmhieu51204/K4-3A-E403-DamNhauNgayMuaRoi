"""
eval/data_loader.py — Nạp dữ liệu đánh giá (Data Loader)
Trích xuất từ eval/run_eval.py gốc (Phần 1 & 2).
Chức năng:
  - Dò tìm file k4_messages.csv
  - Nạp bảng tra cứu nhanh CSV
  - Nạp toàn bộ test case từ JSONL
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any


def find_k4_messages() -> Path | None:
    """
    Tự động dò tìm file dữ liệu chatlog gốc 'k4_messages.csv'.
    Ưu tiên: biến môi trường → bên trong repo → thư mục chia sẻ cấp cha.
    """
    env_csv = os.environ.get("K4_MESSAGES_CSV")
    if env_csv and Path(env_csv).exists():
        return Path(env_csv)

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    candidates = [
        repo_root / "data" / "k4_messages.csv",
        repo_root / "k4_messages.csv",
        script_dir / "k4_messages.csv",
        script_dir / "data" / "k4_messages.csv",
        Path("data/k4_messages.csv"),
        Path("k4_messages.csv"),
        Path("eval/k4_messages.csv"),
        repo_root.parent / "data" / "discord-pack" / "k4_messages.csv",
        repo_root.parent / "data" / "k4_messages.csv",
        repo_root.parent / "K4-3A-Day05-06-AI-Product-Hackathon" / "data" / "discord-pack" / "k4_messages.csv",
        Path("../data/discord-pack/k4_messages.csv"),
        Path("../K4-3A-Day05-06-AI-Product-Hackathon/data/discord-pack/k4_messages.csv"),
    ]

    for p in candidates:
        if p.exists():
            return p
    return None


def load_csv_lookup(csv_path: Path | str | None) -> dict[str, dict[str, str]]:
    """Nạp bảng tra cứu nhanh toàn bộ tin nhắn từ k4_messages.csv theo msg_id."""
    lookup: dict[str, dict[str, str]] = {}
    if not csv_path or not os.path.exists(csv_path):
        return lookup

    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg_id = row.get("msg_id", "").strip()
                if msg_id:
                    lookup[msg_id] = dict(row)
    except (PermissionError, OSError):
        pass
    return lookup


def load_all_cases(csv_lookup: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Nạp toàn bộ test case từ 2 file JSONL:
      1. eval/real_cases.jsonl    : 12 case thật từ Discord
      2. eval/synthetic_cases.jsonl : 23 case tổng hợp biên
    """
    eval_dir = Path(__file__).resolve().parent
    real_file = eval_dir / "real_cases.jsonl"
    synth_file = eval_dir / "synthetic_cases.jsonl"

    cases: list[dict[str, Any]] = []

    # 1. Nạp Real Cases
    if real_file.exists():
        with open(real_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                msg_id = item.get("source_msg_id")

                if msg_id in csv_lookup:
                    row = csv_lookup[msg_id]
                    item["message_text"] = row.get("content", "")
                    if str(row.get("is_bot", "")).strip().lower() in ["true", "1"]:
                        item["is_bot"] = True
                else:
                    item["message_text"] = item.get("scenario_summary", "")

                ctx_ids = item.get("input", {}).get("context_message_ids", [])
                ctx_texts = []
                for cid in ctx_ids:
                    if cid in csv_lookup:
                        ctx_texts.append(
                            f"{cid} ({csv_lookup[cid].get('author', 'user')}): "
                            f"{csv_lookup[cid].get('content', '')}"
                        )
                item["context_text"] = "\n".join(ctx_texts)
                cases.append(item)

    # 2. Nạp Synthetic Cases
    if synth_file.exists():
        with open(synth_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                item["message_text"] = item.get("input", {}).get("message_text", "")

                ctx_msgs = item.get("input", {}).get("context_messages", [])
                ctx_msg_texts = [
                    f"[{m.get('msg_id', 'CTX')}]: {m.get('text', '')}" for m in ctx_msgs
                ]

                sources = item.get("input", {}).get("official_sources", [])
                src_texts = [
                    f"[{s.get('source_id')}]: {s.get('text')}" for s in sources
                ]

                item["context_text"] = "\n".join(ctx_msg_texts + src_texts)
                cases.append(item)

    return cases
