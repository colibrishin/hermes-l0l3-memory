---
name: l0-l3-memory
description: Use when asked to remember, save memory, or recall context. Manages long-term user (global) and project memory as L0-L3 tiered files, loaded global -> project.
---

# L0-L3 Tiered Memory Protocol

Memory lives in two scopes, loaded **global -> project**. Both use the same 4-tier layout.

| Scope | Directory | Holds |
|---|---|---|
| Global | `${HERMES_HOME:-~/.hermes}/l0-l3-memory/` (per Hermes profile) | Who the user is, cross-project preferences, environment facts, conventions that apply everywhere |
| Project | nearest `.memory/` at or above the working directory (below `$HOME`) | Repo-specific architecture, conventions, decisions, playbooks |

Project memory is more specific: on conflict it overrides global memory. Never copy a global rule into a project store; only record the project-specific exception.

## Tiers (same in each scope)

1. **L0 (`L0-index.md` / Always in Context)**: max 30 lines, one-line pointers to L1/L2. Injected at session start. Never dump full notes here.
2. **L1 (`L1-active.md` / Active Rules & Decisions)**: core constraints, conventions, active decisions. Injected at session start alongside L0.
3. **L2 (`L2-topics/<topic>.md` / On-Demand)**: detailed notes and playbooks. Read only the file L0 points to for the current task.
4. **L3 (`L3-archive/` / Cold History)**: outdated plans, resolved incidents. Never load unless explicitly searching history.

## Workflow
- **Recall (at task start)**: use the preloaded global + project L0/L1 -> read only the relevant `L2-topics/*.md` from the scope L0 points to.
- **Save (at task end or when asked to remember)**:
  1. Pick the scope: would this still be true in a different project? -> global. Only true for this repo -> project. If unsure, ask.
  2. Write details to `<scope>/L2-topics/<topic>.md`, promote durable rules to `<scope>/L1-active.md`, add/update a 1-line pointer in `<scope>/L0-index.md`.
  3. Create the project `.memory/` at the repository root (not a subdirectory) the first time project memory is saved.
- Injection happens at session start; edits take effect from the next session.
