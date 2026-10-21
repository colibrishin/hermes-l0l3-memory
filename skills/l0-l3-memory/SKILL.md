---
name: l0-l3-memory
description: 프로젝트와 사용자의 장기 기억을 토큰 낭비 없이 L0~L3 4단계 파일 구조로 관리합니다. (기억해줘, 메모리에 저장, 이전 기억 확인, remember, save memory, recall context 요청 시 자동 실행)
---

# L0-L3 Tiered Memory Protocol

Maintain project memory inside `.memory/` across 4 strict tiers to minimize context bloat:

1. **L0 (`.memory/L0-index.md` / Always in Context)**:
   - Maximum 30 lines. One-line index mapping topics to L1/L2 files.
   - Automatically injected at session start by the `l0-l3-memory` plugin. Never dump full notes into L0.
2. **L1 (`.memory/L1-active.md` / Active Rules & Decisions)**:
   - Core architectural constraints, coding conventions, and active decisions for the current project.
   - Automatically injected at session start alongside L0.
3. **L2 (`.memory/L2-topics/<topic>.md` / On-Demand Deep Context)**:
   - Detailed module notes, debugging playbooks, and domain specifics.
   - ONLY read the specific L2 file matching the current task found in `L0-index.md`.
4. **L3 (`.memory/L3-archive/` / Cold History)**:
   - Outdated plans, resolved incident logs, and raw history. Never load unless explicitly searching past history.

## Workflow
- **Recall (작업 시작 시)**: Check preloaded L0/L1 context -> load only relevant `.memory/L2-topics/*.md` when needed.
- **Save (작업 완료/기억 요청 시)**: Write detailed findings to `.memory/L2-topics/<topic>.md`, promote permanent rules to `.memory/L1-active.md`, and add/update a 1-line pointer in `.memory/L0-index.md`.
