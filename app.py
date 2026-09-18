"""
app.py — TA Copilot Interactive Web Dashboard (Streamlit)
Theo đúng mục 2, 3.3, 3.4 & 3.6 trong base_architecture.md:
Tái sử dụng Agent Loop từ chat.py, hiển thị Tool Traces, Metrics và 1-Click Actions.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import streamlit as st

from env_loader import load_env
from versioning import build_artifact_version
from providers import make_provider
from tools import TOOL_FUNCTIONS, execute_tool_call, load_tool_declarations
from chat import run_model_tool_loop

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="TA Copilot — Discord K4 Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nạp cấu hình môi trường
load_env()
ROOT = Path(__file__).resolve().parent

# Khởi tạo Versioning
ver_info = build_artifact_version("v1")
system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
system_prompt = system_prompt_path.read_text(encoding="utf-8") if system_prompt_path.exists() else ""
tools_decl = load_tool_declarations()


# Khởi tạo Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_traces" not in st.session_state:
    st.session_state.tool_traces = []

if "pending_reply" not in st.session_state:
    st.session_state.pending_reply = None


# ==============================================================================
# SIDEBAR: CẤU HÌNH & METRICS
# ==============================================================================
with st.sidebar:
    st.title("🤖 TA Copilot K4")
    st.caption("VinUni AI20k Hackathon · Track B2")
    st.caption(f"Team: **K4-3A-DamNhauNgayMuaRoi**")
    st.divider()

    st.markdown("### 🏷️ Phiên bản Artifact")
    st.code(ver_info.artifact_version, language="text")

    st.divider()
    st.markdown("### ⚙️ Cấu hình LLM Provider")
    provider_choice = st.selectbox(
        "Nhà cung cấp (Provider):",
        options=["mock", "openai", "openrouter", "anthropic", "gemini"],
        index=0,
        help="Chọn 'mock' để thử nghiệm offline hoặc chọn 'openai' để kết nối API"
    )

    model_override = st.text_input(
        "Model ID:",
        value="gpt-4o-mini" if provider_choice in ("openai", "openrouter") else "mock-v1"
    )

    max_rounds = st.slider("Max Reasoning Rounds:", min_value=1, max_value=8, value=5)
    temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.1, step=0.05)

    st.divider()
    st.markdown("### 📊 Chỉ số Giám sát (Metrics)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tồn đọng >4h", "6 câu", delta="-2", delta_color="inverse")
    with col2:
        st.metric("Tỉ lệ duyệt 1-Click", "94.2%", delta="+5.1%")

    st.divider()
    st.markdown("### ⚡ Thao tác nhanh (Quick Triggers)")
    if st.button("🔍 Quét câu hỏi tồn (>4h)"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Hãy quét danh sách câu hỏi đang bị tồn đọng quá 4 giờ chưa được giải đáp trên Discord."
        })
        st.rerun()

    if st.button("📖 Tra cứu quy chế vắng mặt"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tra cứu quy định về số buổi vắng tối đa và điều kiện nộp đơn xin phép của sinh viên."
        })
        st.rerun()

    if st.button("🧹 Xóa lịch sử chat"):
        st.session_state.messages = []
        st.session_state.tool_traces = []
        st.session_state.pending_reply = None
        st.rerun()


# ==============================================================================
# MAIN AREA: KHUNG CHAT & ĐIỀU PHỐI
# ==============================================================================
st.markdown("## 📋 Bản tin Câu hỏi Tồn & Trợ lý Điều phối Trợ Giảng")
st.markdown(
    "Hệ thống giám sát tin nhắn Discord K4, tự động tra cứu cơ sở tri thức (KB) và đề xuất câu trả lời chuẩn hoá có trích dẫn nguồn."
)

# Hiển thị lịch sử hội thoại
for i, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)

            # Hiển thị tool trace tương ứng nếu có
            if i < len(st.session_state.tool_traces) and st.session_state.tool_traces[i]:
                trace_data = st.session_state.tool_traces[i]
                with st.expander(f"🛠️ Tool Execution Trace ({len(trace_data)} rounds)", expanded=False):
                    for round_info in trace_data:
                        r_idx = round_info.get("round")
                        st.markdown(f"**Vòng lập luận #{r_idx}:**")
                        for call in round_info.get("calls", []):
                            c_name = call.get("name")
                            c_args = call.get("args")
                            c_res = call.get("result")
                            st.code(f"Tool: {c_name}\nArgs: {json.dumps(c_args, ensure_ascii=False)}", language="yaml")
                            st.json(c_res)


# Ô nhập câu hỏi mới
user_input = st.chat_input("Nhập chỉ thị điều phối cho TA Copilot (ví dụ: 'Quét câu hỏi tồn', 'Soạn câu trả lời cho MSG_012')...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()


# Xử lý phản hồi nếu tin nhắn cuối cùng là từ user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("TA Copilot đang lập luận và thực thi công cụ..."):
            provider = make_provider(provider_choice)
            chat_context = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            result = run_model_tool_loop(
                messages=chat_context,
                tools=tools_decl,
                provider=provider,
                system_prompt=system_prompt,
                max_rounds=max_rounds,
                model=model_override,
                temperature=temperature
            )

            assistant_text = result.get("final_text", "")
            trace_events = result.get("rounds", [])

            st.markdown(assistant_text)

            # Lưu vào session
            st.session_state.messages.append({"role": "assistant", "content": assistant_text})
            st.session_state.tool_traces.append(trace_events)

            # Kiểm tra xem có dự thảo câu trả lời để kích hoạt 1-Click Action không
            for r in trace_events:
                for c in r.get("calls", []):
                    if c.get("name") == "draft_grounded_reply":
                        st.session_state.pending_reply = c.get("args")

    st.rerun()


# ==============================================================================
# 1-CLICK ACTION PANEL (NẾU CÓ BẢN NHÁP CẦN DUYỆT)
# ==============================================================================
if st.session_state.pending_reply:
    st.divider()
    st.info("⚡ **Hành động 1-Click có sẵn**: Mô hình đã soạn sẵn phản hồi cần Trợ giảng duyệt!")
    p_args = st.session_state.pending_reply

    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1.5, 3])
    with col_btn1:
        if st.button("🚀 Duyệt gửi Discord (1-Click)", type="primary"):
            res = execute_tool_call("post_discord_reply", {
                "channel_id": "k4-support-qna",
                "content": p_args.get("draft_text", ""),
                "reply_to_message_id": p_args.get("question_id", "MSG_UNKNOWN"),
                "confirmed": True
            })
            st.success(f"✔ Đã gửi thành công tới Discord channel #{res.get('channel_id')}!")
            st.session_state.pending_reply = None
            time.sleep(1)
            st.rerun()

    with col_btn2:
        if st.button("❌ Huỷ / Chỉnh sửa"):
            st.session_state.pending_reply = None
            st.rerun()


# ==============================================================================
# EXPORT TRANSCRIPT
# ==============================================================================
st.divider()
col_d1, col_d2 = st.columns([2, 6])
with col_d1:
    transcript_export = json.dumps({
        "artifact_version": ver_info.artifact_version,
        "history": st.session_state.messages,
        "tool_traces": st.session_state.tool_traces
    }, ensure_ascii=False, indent=2)

    st.download_button(
        label="📥 Tải xuống Transcript JSON",
        data=transcript_export,
        file_name=f"transcript_{ver_info.artifact_version}_{int(time.time())}.json",
        mime="application/json"
    )
