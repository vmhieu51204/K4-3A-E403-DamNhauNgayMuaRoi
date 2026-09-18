"""
tools/__init__.py — Tool Registry & Loader
Theo đúng mục 3.2 trong base_architecture.md:
Đảm bảo 3-Layer Sync:
  1. Declaration: artifacts/tools.yaml
  2. Implementation: tools/<name>/tool.py
  3. Registry: TOOL_FUNCTIONS mapping name -> function
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable
import yaml

# Import các implementations thực tế của 6 tools
from tools.fetch_backlog.tool import fetch_backlog_questions
from tools.search_kb.tool import search_course_kb
from tools.request_clarification.tool import request_clarification
from tools.draft_reply.tool import draft_grounded_reply
from tools.escalate_authority.tool import escalate_authority
from tools.post_discord_reply.tool import post_discord_reply


# Registry mapping name -> function
TOOL_FUNCTIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "fetch_backlog_questions": fetch_backlog_questions,
    "search_course_kb": search_course_kb,
    "request_clarification": request_clarification,
    "draft_grounded_reply": draft_grounded_reply,
    "escalate_authority": escalate_authority,
    "post_discord_reply": post_discord_reply,
}


def load_tool_declarations(path: Path | None = None) -> list[dict[str, Any]]:
    """Nạp danh sách khai báo tools từ file YAML."""
    if path is None:
        root = Path(__file__).resolve().parent.parent
        path = root / "artifacts" / "tools.yaml"
    
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file khai báo tools tại: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("tools", [])


def execute_tool_call(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Thực thi một tool call dựa vào tên và danh sách tham số."""
    if name not in TOOL_FUNCTIONS:
        return {
            "status": "error",
            "error_type": "unknown_tool",
            "message": f"Công cụ '{name}' không tồn tại trong registry."
        }
    
    func = TOOL_FUNCTIONS[name]
    try:
        # Nếu có raw arguments json chưa parse
        if "_raw_arguments" in args:
            return {
                "status": "error",
                "error_type": "invalid_arguments_json",
                "message": f"Không thể giải mã tham số JSON cho công cụ {name}: {args['_raw_arguments']}"
            }
        return func(**args)
    except TypeError as e:
        return {
            "status": "error",
            "error_type": "wrong_arguments",
            "message": f"Sai tham số khi gọi '{name}': {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "execution_failed",
            "message": f"Lỗi thực thi trong '{name}': {str(e)}"
        }


__all__ = [
    "TOOL_FUNCTIONS",
    "load_tool_declarations",
    "execute_tool_call",
    "fetch_backlog_questions",
    "search_course_kb",
    "request_clarification",
    "draft_grounded_reply",
    "escalate_authority",
    "post_discord_reply",
]
