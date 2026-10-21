# Lightweight L0-L3 Memory Provider for Hermes Agent.
from __future__ import annotations
from pathlib import Path
import os

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


class L0L3MemoryProvider:
    name = "l0-l3-memory"

    def recall(self, *args, **kwargs) -> str:
        workdir = kwargs.get("workdir") or kwargs.get("cwd")
        return build_l0_l3_memory_block(workdir)

    def get_context(self, *args, **kwargs) -> str:
        return self.recall(*args, **kwargs)


def register(ctx) -> None:
    provider = L0L3MemoryProvider()
    if hasattr(ctx, "register_memory_provider"):
        try:
            ctx.register_memory_provider("l0-l3-memory", provider)
        except Exception:
            pass
    if hasattr(ctx, "register_system_prompt_section"):
        try:
            ctx.register_system_prompt_section(
                "l0_l3_memory",
                lambda *a, **kw: build_l0_l3_memory_block(),
            )
        except Exception:
            pass
