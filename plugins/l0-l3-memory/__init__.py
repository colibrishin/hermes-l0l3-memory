# Lightweight L0-L3 Memory Provider for Hermes Agent.
from __future__ import annotations
from pathlib import Path
import os

from agent.memory_provider import MemoryProvider

MAX_L0_LINES = 30
MAX_L1_LINES = 120
MAX_TOTAL_CHARS = 6000


def _read_bounded(path: Path, max_lines: int) -> str:
    if not path.is_file():
        return ""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    clipped = lines[:max_lines]
    if len(lines) > max_lines:
        clipped.append(f"... (truncated at {max_lines} lines; keep {path.name} concise)")
    return "\n".join(clipped).strip()


def build_l0_l3_memory_block(workdir: str | Path | None = None) -> str:
    root = Path(workdir or os.getcwd())
    mem_dir = root / ".memory"
    if not mem_dir.is_dir():
        return ""
    l0_text = _read_bounded(mem_dir / "L0-index.md", MAX_L0_LINES)
    l1_text = _read_bounded(mem_dir / "L1-active.md", MAX_L1_LINES)
    if not l0_text and not l1_text:
        return ""
    sections = [
        "## Project Memory (L0-L3 Tiered Store)",
        "L0 index and L1 active rules are loaded below. Read `.memory/L2-topics/<topic>.md` on demand only when relevant to the current task.",
    ]
    if l0_text:
        sections.append(f"### L0 Index (`.memory/L0-index.md`)\n{l0_text}")
    if l1_text:
        sections.append(f"### L1 Active Rules (`.memory/L1-active.md`)\n{l1_text}")
    return "\n\n".join(sections)[:MAX_TOTAL_CHARS]


class L0L3MemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "l0-l3-memory"

    def __init__(self) -> None:
        self._block = ""

    def is_available(self) -> bool:
        return True

    def initialize(self, session_id: str, **kwargs) -> None:
        workdir = kwargs.get("cwd") or kwargs.get("workdir") or os.getcwd()
        self._block = build_l0_l3_memory_block(workdir)

    def system_prompt_block(self) -> str:
        return self._block

    def get_tool_schemas(self) -> list[dict]:
        return []


def register(ctx) -> None:
    ctx.register_memory_provider(L0L3MemoryProvider())
