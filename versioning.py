"""
versioning.py — Hash-Based Artifact Versioning
Theo đúng mục 3.5 trong base_architecture.md.
Mục đích: Tự động tính mã băm SHA-256 của system_prompt.md và tools.yaml để
đảm bảo mọi thử nghiệm đều được gắn định danh bất biến (immutability).
Định dạng: v{N}+p{prompt_hash_12}+t{tools_hash_12}
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactVersion:
    version: str              # Label người dùng: "v0", "v1", "v2"...
    artifact_version: str     # "v1+p3a4b5c6d7e8+t9f0a1b2c3d4"
    prompt_hash: str          # Full SHA-256 của system_prompt.md
    tools_hash: str           # Full SHA-256 của tools.yaml
    prompt_path: str
    tools_path: str


def compute_sha256(file_path: Path) -> str:
    """Tính mã băm SHA-256 cho một file."""
    if not file_path.exists():
        return "0" * 64
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_artifact_version(
    version: str = "v1",
    prompt_path: Path = None,
    tools_path: Path = None
) -> ArtifactVersion:
    """
    Tạo định danh ArtifactVersion bất biến từ file prompt và tools.
    """
    root = Path(__file__).resolve().parent
    if prompt_path is None:
        prompt_path = root / "artifacts" / "system_prompt.md"
    if tools_path is None:
        tools_path = root / "artifacts" / "tools.yaml"

    p_hash = compute_sha256(prompt_path)
    t_hash = compute_sha256(tools_path)

    short_p = p_hash[:12]
    short_t = t_hash[:12]
    artifact_ver_str = f"{version}+p{short_p}+t{short_t}"

    return ArtifactVersion(
        version=version,
        artifact_version=artifact_ver_str,
        prompt_hash=p_hash,
        tools_hash=t_hash,
        prompt_path=str(prompt_path),
        tools_path=str(tools_path)
    )
