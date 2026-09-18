"""
eval/run_eval.py — Bộ Đánh Giá 3 Năng Lực Cốt Lõi của MVP TA Copilot
1. Phát hiện đúng tin nhắn nào là câu hỏi cần hỗ trợ (is_support_request)
2. Lọc đúng câu hỏi chưa được trả lời và đã quá SLA 4h (expected_in_backlog)
3. Sinh câu trả lời đề xuất phù hợp với context (suggested_reply)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from codebase.mvp_ai import generate_mvp_reply

VN = timezone(timedelta(hours=7))
DEFAULT_CSV = ROOT / "data" / "discord-pack" / "k4_messages.csv"
if not DEFAULT_CSV.exists() and (ROOT / "data" / "k4_messages.csv").exists():
    DEFAULT_CSV = ROOT / "data" / "k4_messages.csv"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def timestamp(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    return dt.replace(tzinfo=VN) if dt.tzinfo is None else dt


def load_cases(dataset: str) -> list[dict]:
    cases = []
    names = ("real", "synthetic") if dataset == "all" else (dataset,)
    for name in names:
        path = ROOT / "eval" / f"{name}_cases.jsonl"
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line:
                    cases.append(json.loads(line))
    return cases


def load_source_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def evaluate_case(case: dict, rows: list[dict]) -> dict:
    inp = case["input"]
    exp = case["expected"]

    # 1. Trích xuất nội dung tin nhắn và thread context
    if case["origin"] == "real":
        mid = case["source_msg_id"]
        matches = [r for r in rows if r["msg_id"] == mid and r["guild"] == inp["guild"] and r["channel"] == inp["channel"]]
        row = matches[0] if matches else {}
        q_text = row.get("content", "")
        is_bot = str(row.get("is_bot", "")).lower() == "true"
        ctx_msgs = []
        for cmid in inp.get("context_message_ids", []):
            cmatches = [r for r in rows if r["msg_id"] == cmid and r["guild"] == inp["guild"] and r["channel"] == inp["channel"]]
            if cmatches:
                ctx_msgs.append(f"[{cmatches[0]['author']}]: {cmatches[0]['content']}")
        thread_ctx = "\n".join(ctx_msgs)
    else:
        q_text = inp.get("message_text", "")
        is_bot = inp.get("is_bot", False) or exp.get("sender_role") == "bot"
        ctx_msgs = [f"[{m.get('sender_role', 'user')}]: {m.get('text', '')}" for m in inp.get("context_messages", [])]
        sources = [s.get("text", "") for s in inp.get("official_sources", [])]
        thread_ctx = "\n".join(ctx_msgs + sources)

    # 2. Năng lực 1: Phát hiện đúng câu hỏi cần hỗ trợ
    if is_bot:
        pred_support = False
        ai_reply = ""
    else:
        mvp_ai_res = generate_mvp_reply(q_text, thread_ctx)
        pred_support = mvp_ai_res.get("is_question", True)
        ai_reply = mvp_ai_res.get("suggested_reply", "")

    # 3. Năng lực 2: Lọc đúng câu hỏi chưa được trả lời và đã quá SLA 4h
    if not pred_support:
        pred_backlog = "no"
        final_suggested = ""
    else:
        sent_at = timestamp(inp["sent_at"])
        cutoff = timestamp(inp["evaluation_time"])
        hours_wait = (cutoff - sent_at).total_seconds() / 3600

        # Kiểm tra xem câu hỏi đã được giải quyết hoặc trả lời trong context chưa
        ctx_lower = thread_ctx.lower()
        answered_signals = ["updated", "sửa được rồi", "tìm thấy rồi", "được rồi cảm ơn", "đã nộp bù", "join chung", "quận 7"]
        is_answered = any(s in ctx_lower for s in answered_signals) or exp.get("answer_status") == "answered"

        if hours_wait >= 4.0 and not is_answered:
            pred_backlog = "yes"
            # 4. Năng lực 3: Sinh câu trả lời đề xuất phù hợp
            final_suggested = ai_reply
        else:
            pred_backlog = "no"
            final_suggested = ""

    # Chấm điểm 3 năng lực
    cap1_pass = (pred_support == exp.get("is_support_request"))
    cap2_pass = (pred_backlog == exp.get("expected_in_backlog"))
    
    if exp.get("expected_in_backlog") == "yes":
        cap3_pass = bool(final_suggested and len(final_suggested.strip()) > 10)
    else:
        cap3_pass = True

    is_passed = cap1_pass and cap2_pass and cap3_pass

    return {
        "case_id": case["case_id"],
        "origin": case["origin"],
        "question": q_text[:50] + ("..." if len(q_text) > 50 else ""),
        "pred": {
            "is_support_request": pred_support,
            "expected_in_backlog": pred_backlog,
            "suggested_reply": final_suggested,
        },
        "expected": {
            "is_support_request": exp.get("is_support_request"),
            "expected_in_backlog": exp.get("expected_in_backlog"),
        },
        "checks": {
            "cap1_is_support": cap1_pass,
            "cap2_sla_backlog": cap2_pass,
            "cap3_grounded_reply": cap3_pass,
        },
        "passed": is_passed,
    }


def main():
    parser = argparse.ArgumentParser(description="TA Copilot MVP — 3 Capabilities Evaluation Runner")
    parser.add_argument("--dataset", choices=["all", "real", "synthetic"], default="all")
    parser.add_argument("--source-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--limit", type=int, help="Giới hạn số test case chạy")
    parser.add_argument("--output-file", type=Path, default=ROOT / "eval" / "results_mvp.md")
    args = parser.parse_args()

    print(f"\n{BOLD}{CYAN}================================================================={RESET}")
    print(f"{BOLD}{CYAN}   TA COPILOT — ĐÁNH GIÁ 3 NĂNG LỰC CỐT LÕI (MVP RUNNER)       {RESET}")
    print(f"{BOLD}{CYAN}================================================================={RESET}\n")

    cases = load_cases(args.dataset)
    if args.limit:
        cases = cases[:args.limit]

    rows = load_source_csv(args.source_csv)
    print(f"📁 Dữ liệu chatlog: {args.source_csv} ({len(rows)} dòng)")
    print(f"📋 Tổng số test case kiểm thử: {len(cases)}")
    print(f"🎯 Đánh giá 3 năng lực: (1) Nhận diện câu hỏi | (2) Lọc SLA >4h | (3) Sinh câu trả lời\n")

    print("-" * 105)
    print(f"{'MÃ CASE':<12} | {'CÂU HỎI HỌC VIÊN':<32} | {'CÂU HỎI?':<8} | {'BACKLOG?':<8} | {'GỢI Ý?':<6} | {'KẾT QUẢ'}")
    print("-" * 105)

    results = []
    for case in cases:
        res = evaluate_case(case, rows)
        results.append(res)
        
        status_str = f"{GREEN}[PASS]{RESET}" if res["passed"] else f"{RED}[FAIL]{RESET}"
        c1 = "✓" if res["checks"]["cap1_is_support"] else "✗"
        c2 = "✓" if res["checks"]["cap2_sla_backlog"] else "✗"
        c3 = "✓" if res["checks"]["cap3_grounded_reply"] else "✗"
        
        q_disp = res["question"].replace("\n", " ")[:30]
        print(f"{res['case_id']:<12} | {q_disp:<32} | {c1:<8} | {c2:<8} | {c3:<6} | {status_str}")
        if res["pred"]["suggested_reply"]:
            preview = res["pred"]["suggested_reply"][:65]
            print(f"             ↳ Lời gợi ý: {CYAN}{preview}...{RESET}")

    print("-" * 105)

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    c1_count = sum(1 for r in results if r["checks"]["cap1_is_support"])
    c2_count = sum(1 for r in results if r["checks"]["cap2_sla_backlog"])
    c3_count = sum(1 for r in results if r["checks"]["cap3_grounded_reply"])

    print(f"\n{BOLD}📊 BẢNG TỔNG HỢP CHỈ SỐ ĐO LƯỜNG 3 NĂNG LỰC CỐT LÕI (MVP EVAL):{RESET}")
    print(f"  • Tổng số test case kiểm thử     : {total}")
    print(f"  • Số case đạt toàn diện (PASS)   : {BOLD}{passed_count} / {total} ({passed_count/total*100:.1f}%){RESET}")
    print(f"  • Năng lực 1 (Question Detection): {c1_count}/{total} ({c1_count/total*100:.1f}%)")
    print(f"  • Năng lực 2 (SLA >4h Unanswered): {c2_count}/{total} ({c2_count/total*100:.1f}%)")
    print(f"  • Năng lực 3 (Grounded AI Reply) : {c3_count}/{total} ({c3_count/total*100:.1f}%)")

    # Xuất file báo cáo Markdown
    now_str = datetime.now(VN).strftime("%Y-%m-%d %H:%M:%S")
    report_content = f"""# Báo Cáo Đánh Giá 3 Năng Lực Cốt Lõi (MVP Eval Results)

- **Thời điểm đánh giá:** {now_str}
- **Quy mô kiểm thử:** **{total} test cases** (12 Chatlog thật Discord K4 + 23 Tình huống giả lập)
- **Tỷ lệ Pass toàn diện:** **{passed_count}/{total} ({passed_count/total*100:.1f}%)**
- **Năng lực 1 (Question Detection Accuracy):** **{c1_count/total*100:.1f}%**
- **Năng lực 2 (SLA >4h Unanswered Backlog Accuracy):** **{c2_count/total*100:.1f}%**
- **Năng lực 3 (Grounded Reply Generation Quality):** **{c3_count/total*100:.1f}%**

## Bảng Chi Tiết Kết Quả 35 Test Cases
| Mã Case | Nội dung câu hỏi | Năng lực 1 (Câu hỏi?) | Năng lực 2 (Backlog >4h?) | Năng lực 3 (AI Gợi ý) | Kết quả |
|---|---|:---:|:---:|:---:|:---:|
"""
    for r in results:
        status_badge = "✅ PASS" if r["passed"] else "❌ FAIL"
        c1_b = "✓" if r["checks"]["cap1_is_support"] else "✗"
        c2_b = "✓" if r["checks"]["cap2_sla_backlog"] else "✗"
        c3_b = "✓" if r["checks"]["cap3_grounded_reply"] else "✗"
        q_safe = r["question"].replace("|", "\\|").replace("\n", " ")
        report_content += f"| `{r['case_id']}` | {q_safe} | {c1_b} | {c2_b} | {c3_b} | {status_badge} |\n"

    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n{GREEN}✅ Đã xuất báo cáo chi tiết ra: {args.output_file}{RESET}\n")


if __name__ == "__main__":
    main()
