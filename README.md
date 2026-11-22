# hermes-l0l3-memory

Lightweight L0-L3 tiered memory provider and skill for Hermes Agent.

## Scopes (global -> project)

| Scope | Directory | Loaded |
|---|---|---|
| Global | `<HERMES_HOME>/l0-l3-memory/` (per profile) | every session |
| Project | nearest `.memory/` at or above the session cwd, below `$HOME` | when one exists |

Each scope holds `L0-index.md` (≤30 lines), `L1-active.md` (≤120 lines), `L2-topics/`, `L3-archive/`.
Only L0 and L1 are injected, global first; project entries win on conflict. Each scope is capped at 3000 chars.

## Quick Install
- **Windows (PowerShell):** `.\install.ps1`
- **macOS / Linux (Bash):** `bash install.sh`

Then set `memory.provider: l0-l3-memory` in `config.yaml`.
