"""
agent.py — TA Copilot Agent Wrapper
Theo đúng mục 2 & 3.4 trong base_architecture.md:
Đóng gói Agent thành class để tái sử dụng trong Eval Runner, API Service hoặc Web App.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from providers import Provider, make_provider
from tools import load_tool_declarations
from versioning import ArtifactVersion, build_artifact_version
from chat import run_model_tool_loop


class TACopilotAgent:
    """
    Agent đại diện cho TA Copilot, tích hợp Multi-round Reasoning và 6 Tools nghiệp vụ.
    """

    def __init__(
        self,
        provider: Provider | None = None,
        version: str = "v1",
        model: str | None = None,
        max_rounds: int = 5
    ):
        self.root = Path(__file__).resolve().parent
        self.prompt_path = self.root / "artifacts" / "system_prompt.md"
        self.tools_path = self.root / "artifacts" / "tools.yaml"

        self.version_info: ArtifactVersion = build_artifact_version(
            version, self.prompt_path, self.tools_path
        )
        self.system_prompt = self.prompt_path.read_text(encoding="utf-8")
        self.tools = load_tool_declarations(self.tools_path)

        self.provider = provider or make_provider("openai")
        self.model = model
        self.max_rounds = max_rounds

    def run(self, user_query: str, history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Thực thi một lượt tương tác của người dùng qua Agent Tool Loop."""
        messages = list(history or [])
        messages.append({"role": "user", "content": user_query})

        return run_model_tool_loop(
            messages=messages,
            tools=self.tools,
            provider=self.provider,
            system_prompt=self.system_prompt,
            max_rounds=self.max_rounds,
            model=self.model
        )
