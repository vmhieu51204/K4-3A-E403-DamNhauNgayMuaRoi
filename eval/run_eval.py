#!/usr/bin/env python3
"""
TA Copilot — Evaluation Test Runner (Orchestrator)
"""
from __future__ import annotations

import argparse
import time
import json
import os
from pathlib import Path

# Core Architecture Imports
from env_loader import load_env
from providers import make_provider

# Eval Module Imports
from eval.data_loader import find_k4_messages, load_csv_lookup, load_all_cases
from eval.prompts import PROMPT_V0, PROMPT_V1
from eval.classify_engine import classify_by_heuristics, normalize_action
from eval.evaluator import evaluate_case
from eval.reporter import export_markdown_report

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def call_llm(message_text: str, context_text: str = "", run_version: int = 2) -> dict:
    """Gửi câu hỏi qua Provider Layer."""
    system_prompt = PROMPT_V1 if run_version == 2 else PROMPT_V0
    if run_version == 2:
        user_content = f"<student_message>\n{message_text}\n</student_message>"
    else:
        user_content = f"Tin nhắn cần phân loại: \"{message_text}\""

    if context_text:
        user_content += f"\nNgữ cảnh liên quan:\n{context_text}"

    # Use the Provider architecture
    provider = make_provider("openai")
    
    # We construct a messages list as expected by complete()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    
    raw_text = provider.complete(messages)
    
    # Cleanup json blocks
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()
            
    return json.loads(raw_text)

def main():
    load_env()
    
    parser = argparse.ArgumentParser(description="TA Copilot Evaluation Test Runner")
    parser.add_argument("--run", "-r", type=int, default=2, choices=[1, 2],
                        help="Lượt đánh giá (1: Baseline CP3, 2: Optimized Guardrails CP4 - Mặc định: 2)")
    args, _ = parser.parse_known_args()
    run_version = args.run

    if run_version == 1:
        print(f"\n{BOLD}{CYAN}================================================================={RESET}")
        print(f"{BOLD}{CYAN}   TA COPILOT — EVALUATION TEST RUNNER (CHECKPOINT 3 — RUN 1)   {RESET}")
        print(f"{BOLD}{CYAN}================================================================={RESET}\n")
    else:
        print(f"\n{BOLD}{CYAN}================================================================={RESET}")
        print(f"{BOLD}{CYAN}   TA COPILOT — EVALUATION TEST RUNNER (CHECKPOINT 4 — RUN 2)   {RESET}")
        print(f"{BOLD}{CYAN}================================================================={RESET}\n")

    csv_path = find_k4_messages()
    if csv_path:
        print(f"📁 Đã tìm thấy dữ liệu gốc: {csv_path.name}")
        csv_lookup = load_csv_lookup(csv_path)
    else:
        print(f"{YELLOW}⚠️  Không tìm thấy k4_messages.csv, dùng tóm tắt nội dung.{RESET}")
        csv_lookup = {}

    cases = load_all_cases(csv_lookup)
    total_cases = len(cases)
    real_count = sum(1 for c in cases if c.get("origin") == "real")
    synth_count = total_cases - real_count
    print(f"📋 Tổng số test case đã nạp: {BOLD}{total_cases}{RESET} ({real_count} Real + {synth_count} Synthetic)")
    print(f"🎯 Phiên bản kiểm thử: {BOLD}LƯỢT {run_version} ({'Baseline CP3' if run_version == 1 else 'Tối ưu Guardrails v1 CP4'}){RESET}\n")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "")
    use_live_api = bool(api_key and "sk-" in api_key)

    if use_live_api:
        print(f"🌐 Chế độ: {GREEN}{BOLD}CALL LIVE API THẬT{RESET} ({base_url})")
    else:
        print(f"⚙️  Chế độ: {YELLOW}{BOLD}PREVIEW TRACE RUNNER{RESET} (Không có API Key hoặc chạy kiểm tra)")

    print("-" * 88)
    print(f"{'MÃ CASE':<12} | {'CHỦ ĐỀ':<11} | {'BACKLOG?':<8} | {'HÀNH ĐỘNG':<9} | {'KẾT QUẢ':<8} | {'CHI TIẾT / LỖI'}")
    print("-" * 88)

    results = []
    pass_count = 0
    intent_correct_count = 0
    topic_correct_count = 0
    action_correct_count = 0
    safety_violations = 0

    for i, case in enumerate(cases, 1):
        cid = case.get("case_id")
        exp = case.get("expected", {})
        msg_snippet = case.get("message_text", "")[:45].replace("\n", " ")
        pred = None

        if use_live_api:
            try:
                pred = call_llm(case.get("message_text", ""), case.get("context_text", ""), run_version=run_version)
                time.sleep(0.3)
            except Exception:
                pred = classify_by_heuristics(case.get("message_text", ""), case.get("context_text", ""), run_version=run_version, is_bot=case.get("is_bot", False))

        if not pred:
            pred = classify_by_heuristics(case.get("message_text", ""), case.get("context_text", ""), run_version=run_version, is_bot=case.get("is_bot", False))

        eval_res = evaluate_case(pred, exp)

        if eval_res["intent_match"]:
            intent_correct_count += 1
        if eval_res["topic_match"]:
            topic_correct_count += 1
        if eval_res["action_match"]:
            action_correct_count += 1
        if eval_res["passed"]:
            pass_count += 1

        is_safety_case = (normalize_action(exp.get("expected_action", "")) == "reject") or ("jailbreak" in str(exp.get("reason", "")).lower()) or ("liêm chính" in str(exp.get("reason", "")).lower())
        if is_safety_case and not eval_res["action_match"]:
            safety_violations += 1

        status_str = f"{GREEN}[PASS]{RESET}" if eval_res["passed"] else f"{RED}[FAIL]{RESET}"
        pred_topic = pred.get("topic", "other")
        pred_backlog = pred.get("expected_in_backlog", "no")
        norm_pred_action = eval_res["norm_pred_action"]

        print(f"{cid:<12} | {pred_topic:<11} | {pred_backlog:<8} | {norm_pred_action:<9} | {status_str} | {eval_res['error_note']}")
        if "suggested_reply" in pred:
            print(f"             ↳ Lời gợi ý: {CYAN}{pred['suggested_reply']}{RESET}")

        results.append({
            "case_id": cid,
            "input": msg_snippet,
            "expected_topic": exp.get("topic"),
            "pred_topic": pred_topic,
            "expected_backlog": exp.get("expected_in_backlog"),
            "pred_backlog": pred_backlog,
            "expected_action": eval_res["norm_exp_action"],
            "pred_action": norm_pred_action,
            "passed": eval_res["passed"],
            "reason": pred.get("reason", "")
        })

    pass_rate   = (pass_count / total_cases) * 100
    intent_rate = (intent_correct_count / total_cases) * 100
    topic_rate  = (topic_correct_count / total_cases) * 100
    action_rate = (action_correct_count / total_cases) * 100

    print("-" * 88)
    print(f"\n{BOLD}📊 BẢNG TỔNG HỢP CHỈ SỐ ĐO LƯỜNG LƯỢT {run_version} (EVAL RUN {run_version} — {'CHECKPOINT 3' if run_version == 1 else 'CHECKPOINT 4'}):{RESET}")
    print(f"  • Tổng số case kiểm thử : {BOLD}{total_cases}{RESET} ({real_count} Real + {synth_count} Synthetic)")
    print(f"  • Số case đạt (PASS)    : {GREEN}{BOLD}{pass_count} / {total_cases} ({pass_rate:.1f}%){RESET}")
    print(f"  • Intent Accuracy       : {BOLD}{intent_rate:.1f}%{RESET} (Kỳ vọng: ≥90%)")
    print(f"  • Topic Accuracy        : {BOLD}{topic_rate:.1f}%{RESET} (Kỳ vọng: ≥85%)")
    print(f"  • Action Accuracy       : {BOLD}{action_rate:.1f}%{RESET} (Kỳ vọng: ≥85%)")
    print(f"  • Safety / Jailbreak    : {YELLOW if safety_violations > 0 else GREEN}{BOLD}{safety_violations} case cảnh báo{RESET} ({'Cần bổ sung guardrails ở CP4' if safety_violations > 0 else 'Hoàn toàn an toàn'})")

    stats = {
        "total": total_cases,
        "real": real_count,
        "synth": synth_count,
        "pass_count": pass_count,
        "pass_rate": pass_rate,
        "intent_rate": intent_rate,
        "topic_rate": topic_rate,
        "action_rate": action_rate,
        "safety_violations": safety_violations
    }
    
    out_dir = Path("eval")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"results_run_{run_version}.md"
    export_markdown_report(out_file, stats, results, run_version=run_version)
    print(f"\n{GREEN}✅ Đã xuất báo cáo chi tiết ra: {BOLD}{out_file}{RESET}\n")

if __name__ == "__main__":
    main()
