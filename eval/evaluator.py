"""
eval/evaluator.py — Bộ đánh giá và chấm điểm
"""
from typing import Any
from eval.classify_engine import normalize_action

def evaluate_case(pred: dict[str, Any], exp: dict[str, Any]) -> dict[str, Any]:
    """
    So sánh dự đoán của AI với nhãn kỳ vọng trên 4 trục độc lập.
    """
    norm_pred_action = normalize_action(pred.get("action"))
    norm_exp_action = normalize_action(exp.get("expected_action"))

    intent_match  = (pred.get("is_support_request") == exp.get("is_support_request"))
    topic_match   = (pred.get("topic") == exp.get("topic"))
    backlog_match = (pred.get("expected_in_backlog") == exp.get("expected_in_backlog"))
    action_match  = (norm_pred_action == norm_exp_action)

    passed = (intent_match and topic_match and backlog_match and action_match)

    error_details = []
    if not topic_match:
        error_details.append(f"Topic: {pred.get('topic')} != {exp.get('topic')}")
    if not backlog_match:
        error_details.append(f"Backlog: {pred.get('expected_in_backlog')} != {exp.get('expected_in_backlog')}")
    if not action_match:
        error_details.append(f"Action: {norm_pred_action} != {norm_exp_action}")

    return {
        "passed": passed,
        "intent_match": intent_match,
        "topic_match": topic_match,
        "backlog_match": backlog_match,
        "action_match": action_match,
        "norm_pred_action": norm_pred_action,
        "norm_exp_action": norm_exp_action,
        "error_note": "; ".join(error_details) if error_details else f"Khớp hoàn toàn ({pred.get('topic')} / {norm_pred_action})"
    }
