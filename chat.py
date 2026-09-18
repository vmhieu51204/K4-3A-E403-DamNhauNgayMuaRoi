"""
chat.py — Agent Tool Loop & CLI Interactive Interface
Theo đúng mục 3.3 & 3.4 trong base_architecture.md:
Chạy vòng lặp lập luận đa lượt (Multi-round reasoning):
  User message -> LLM -> Tool Calls -> Execution -> Feed back -> Loop/Finish
Hỗ trợ 3 điều kiện dừng:
  1. Model trả lời trực tiếp (không gọi tool nữa) -> Done
  2. Tool trả về 'awaiting_user: True' -> Dừng sớm, hỏi user (HAX G10)
  3. Hết max_rounds -> Dừng an toàn
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from env_loader import load_env
from providers import Provider, make_provider
from tools import execute_tool_call, load_tool_declarations
from versioning import build_artifact_version

# Nạp cấu hình môi trường
load_env()


def tool_results_message(events: list[dict[str, Any]]) -> dict[str, str]:
    """Đóng gói kết quả thực thi các tools thành message gửi lại cho LLM."""
    return {
        "role": "user",
        "content": (
            f"TOOL_RESULTS_JSON:\n{json.dumps(events, ensure_ascii=False, indent=2)}\n\n"
            "Hãy sử dụng kết quả công cụ ở trên để đưa ra câu trả lời hoặc quyết định bước tiếp theo cho Trợ giảng."
        )
    }


def run_model_tool_loop(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    provider: Provider,
    *,
    system_prompt: str,
    max_rounds: int = 5,
    model: str | None = None,
    temperature: float = 0.1
) -> dict[str, Any]:
    """
    Hàm lõi chạy Agent Tool Loop (dùng chung cho CLI, Web UI và Eval Runner).
    """
    full_messages = [{"role": "system", "content": system_prompt}] + list(messages)
    rounds_record = []
    assistant_final_text = ""
    status = "answered"

    for round_idx in range(1, max_rounds + 1):
        # 1. Gọi LLM
        response = provider.complete(
            messages=full_messages,
            tools=tools,
            model=model,
            temperature=temperature
        )

        # 2. Kiểm tra nếu mô hình không gọi tool nào -> Hoàn tất
        if not response.tool_calls:
            assistant_final_text = response.text or ""
            rounds_record.append({
                "round": round_idx,
                "tool_calls": [],
                "tool_results": [],
                "response_text": assistant_final_text
            })
            break

        # 3. Thực thi danh sách tool calls
        calls_record = []
        results_record = []
        pause_for_user = False
        pause_data = None

        for tc in response.tool_calls:
            calls_record.append({"name": tc.name, "args": tc.args, "id": tc.id})
            result = execute_tool_call(tc.name, tc.args)
            results_record.append({"tool": tc.name, "args": tc.args, "result": result})

            # Detect cờ tạm dừng hỏi người dùng (HAX G10)
            if isinstance(result, dict) and result.get("awaiting_user"):
                pause_for_user = True
                pause_data = result

        rounds_record.append({
            "round": round_idx,
            "tool_calls": calls_record,
            "tool_results": results_record,
            "response_text": response.text
        })

        # 4. Nếu có tool yêu cầu dừng để hỏi lại người dùng -> Dừng loop
        if pause_for_user:
            status = "waiting_for_user"
            clarification_q = pause_data.get("clarification_question", "Cần thêm thông tin làm rõ.")
            assistant_final_text = f"⚠️ [CẦN LÀM RÕ — HAX G10]: {clarification_q}"
            break

        # 5. Đóng gói kết quả tools đưa lại vào context và tiếp tục vòng lặp
        assistant_turn_msg = {"role": "assistant", "content": response.text or ""}
        if response.raw and "choices" in response.raw:
            raw_msg = response.raw["choices"][0].get("message", {})
            if "tool_calls" in raw_msg:
                assistant_turn_msg["tool_calls"] = raw_msg["tool_calls"]

        full_messages.append(assistant_turn_msg)
        full_messages.append(tool_results_message(results_record))

    else:
        # Nếu đã quay hết max_rounds mà chưa dừng
        status = "max_tool_rounds"
        assistant_final_text = "⚠️ Đã đạt giới hạn số vòng suy luận tối đa (max_rounds)."

    return {
        "status": status,
        "assistant_text": assistant_final_text,
        "final_text": assistant_final_text,
        "rounds": rounds_record,
        "total_rounds": len(rounds_record),
        "messages_history": full_messages
    }


def save_transcript(turn_data: dict[str, Any], version_str: str) -> Path:
    """Lưu nhật ký tương tác ra file JSON trong thư mục transcripts/."""
    transcript_dir = Path(__file__).resolve().parent / "transcripts"
    transcript_dir.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%S")
    file_path = transcript_dir / f"transcript_{version_str}_{ts}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(turn_data, f, ensure_ascii=False, indent=2)
    return file_path


def main():
    """Giao diện dòng lệnh (CLI Interactive Chat) cho Trợ giảng."""
    print("\n" + "=" * 70)
    print("🤖 TA COPILOT AGENT — GIAO DIỆN DÒNG LỆNH (CLI INTERACTIVE CHAT)")
    print("=" * 70)

    # Nạp artifacts
    root = Path(__file__).resolve().parent
    prompt_file = root / "artifacts" / "system_prompt.md"
    tools_file = root / "artifacts" / "tools.yaml"

    ver = build_artifact_version("v1", prompt_file, tools_file)
    print(f"📦 Artifact Version: \033[96m{ver.artifact_version}\033[0m")

    system_prompt = prompt_file.read_text(encoding="utf-8")
    tools = load_tool_declarations(tools_file)
    provider = make_provider("openai")

    print(f"🛠️  Đã nạp thành công: {len(tools)} công cụ nghiệp vụ.")
    print("👉 Nhập yêu cầu của bạn (Ví dụ: 'Quét câu hỏi tồn', 'Có học viên hỏi về lab 1...')")
    print("👉 Gõ 'exit' hoặc 'quit' để thoát.\n" + "-" * 70)

    chat_history: list[dict[str, Any]] = []

    while True:
        try:
            user_input = input("\n👤 TA > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("👋 Tạm biệt Trợ giảng!")
                break

            chat_history.append({"role": "user", "content": user_input})

            print("\n⏳ Agent đang suy luận và điều phối công cụ...")
            result = run_model_tool_loop(
                messages=chat_history,
                tools=tools,
                provider=provider,
                system_prompt=system_prompt
            )

            # In chi tiết các bước gọi tool
            for r in result["rounds"]:
                if r["tool_calls"]:
                    print(f"\n⚙️  [Round {r['round']}] Gọi các công cụ:")
                    for tc in r["tool_calls"]:
                        print(f"   • \033[93m{tc['name']}\033[0m(args={tc['args']})")
                for tr in r["tool_results"]:
                    res_summary = str(tr['result'])[:100] + ("..." if len(str(tr['result'])) > 100 else "")
                    print(f"   ↳ Kết quả {tr['tool']}: \033[92m{res_summary}\033[0m")

            print(f"\n🤖 TA Copilot > \033[1m{result['assistant_text']}\033[0m")

            # Cập nhật context
            chat_history.append({"role": "assistant", "content": result["assistant_text"]})

            # Lưu transcript
            log_file = save_transcript({
                "artifact_version": ver.artifact_version,
                "input": user_input,
                "result": result
            }, ver.version)

        except KeyboardInterrupt:
            print("\n👋 Dừng phiên làm việc.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")


if __name__ == "__main__":
    main()
