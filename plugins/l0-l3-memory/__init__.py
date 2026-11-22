# Lightweight L0-L3 Memory Provider for Hermes Agent.
#
# Two scopes, loaded global -> project:
#   global : <hermes_home>/l0-l3-memory/   (profile-scoped; applies in every session)
#   project: nearest <dir>/.memory/ walking up from the session cwd (stops below $HOME)
# Both scopes use the same layout: L0-index.md, L1-active.md, L2-topics/, L3-archive/.
# Only L0 and L1 are injected; project entries override global ones on conflict.
from __future__ import annotations
from pathlib import Path
import os

from agent.memory_provider import MemoryProvider

GLOBAL_DIRNAME = "l0-l3-memory"
PROJECT_DIRNAME = ".memory"
MAX_L0_LINES = 30
MAX_L1_LINES = 120
MAX_SCOPE_CHARS = 3000  # per scope, so a large global store cannot starve the project one


def _read_bounded(path: Path, max_lines: int) -> str:
    if not path.is_file():
        return ""
    try:
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except OSError:
        return ""
    clipped = lines[:max_lines]
    if len(lines) > max_lines:
        clipped.append(f"... (truncated at {max_lines} lines; keep {path.name} concise)")
    return "\n".join(clipped).strip()


def _resolve(path: Path) -> Path:
    try:
        return path.resolve()
    except OSError:
        return path.absolute()


def global_memory_dir(hermes_home: str | Path | None = None) -> Path:
    home = hermes_home or os.environ.get("HERMES_HOME") or (Path.home() / ".hermes")
    return Path(home) / GLOBAL_DIRNAME


def find_project_memory_dir(workdir: str | Path | None = None) -> Path | None:
    """Nearest ``.memory/`` at or above ``workdir``, never at $HOME or above (that is global territory)."""
    start = _resolve(Path(workdir or os.getcwd()))
    user_home = _resolve(Path.home())
    for d in (start, *start.parents):
        if d == user_home or d in user_home.parents:
            return None
        candidate = d / PROJECT_DIRNAME
        if candidate.is_dir():
            return candidate
    return None


def _scope_section(title: str, mem_dir: Path) -> str:
    l0_text = _read_bounded(mem_dir / "L0-index.md", MAX_L0_LINES)
    l1_text = _read_bounded(mem_dir / "L1-active.md", MAX_L1_LINES)
    if not l0_text and not l1_text:
        return ""
    parts = [f"### {title} (`{mem_dir}`)"]
    if l0_text:
        parts.append(f"#### L0 Index\n{l0_text}")
    if l1_text:
        parts.append(f"#### L1 Active Rules\n{l1_text}")
    return "\n\n".join(parts)[:MAX_SCOPE_CHARS]


def build_l0_l3_memory_block(workdir: str | Path | None = None, hermes_home: str | Path | None = None) -> str:
    global_dir = global_memory_dir(hermes_home)
    project_dir = find_project_memory_dir(workdir)
    if project_dir is not None and _resolve(project_dir) == _resolve(global_dir):
        project_dir = None

    sections = []
    if global_dir.is_dir():
        sections.append(_scope_section("Global Memory", global_dir))
    if project_dir is not None:
        sections.append(_scope_section("Project Memory", project_dir))
    sections = [s for s in sections if s]
    if not sections:
        return ""

    header = (
        "## L0-L3 Tiered Memory (global -> project)\n"
        "Global memory applies everywhere; project memory is more specific and wins on conflict. "
        "Read `<scope dir>/L2-topics/<topic>.md` on demand only when relevant to the current task."
    )
    return "\n\n".join([header, *sections])


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
        self._block = build_l0_l3_memory_block(workdir, kwargs.get("hermes_home"))

    def system_prompt_block(self) -> str:
        return self._block

    def get_tool_schemas(self) -> list[dict]:
        return []


def register(ctx) -> None:
    ctx.register_memory_provider(L0L3MemoryProvider())
