---
audio: false
generated: true
image: false
lang: en
layout: post
title: Personal Productivity CLI Toolkit Repository
translated: false
type: note
---

## Comprehensive Summary of `ww` Repository

### What It Is

`ww` is a Python CLI toolkit (`pip install ww`) with 90+ commands organized into ~35 groups. It's a personal productivity Swiss Army knife — one binary that replaces dozens of scripts, aliases, and one-off tools. Built by you, for you.

### Architecture

- **Entry point**: `ww/main.py` (1,573 lines) — flat `if/elif` dispatcher, lazy imports per command
- **Pattern**: each module exposes `main()`, imported on-demand inside the elif branch
- **State**: SQLite DB (`ww.db`) logs every command invocation with timestamp, group, subcmd, exit code
- **LLM layer**: `openrouter_client.py` wraps OpenRouter API (non-streaming + streaming), used by git-ai-commit, note processing, search, image gen, whisper refinement, degree categorization, etc.
- **Env**: `.env` file loaded from 3 locations, keys: `OPENROUTER_API_KEY`, `MODEL`, `VISION_MODEL`, `BASE_PATH`

### Command Groups (wired into main.py)

| Category | Groups |
|----------|--------|
| **Git/GitHub** | git, github, action, actions |
| **Content** | note, screenshot, image, gif, pdf, md, marp, gen-image |
| **LLM/AI** | llm, openrouter, copilot, hf, env, whisper |
| **System** | macos, linux, proc, host, alarm, display, ghostty |
| **Network** | network, clash, cloudflare |
| **Search** | search (bing, ddg, startpage, tavily, web, code, filename) |
| **DevOps** | sync, projects, zed, amd-dev-cloud, completion |
| **Data** | read (RAG), weather, degree, db |
| **Utilities** | utils, encoding |

### Unwired Modules (~20+)

These exist as code but aren't accessible via `ww` CLI:

`ww/agent/` (code_agent, fix_agent, refactor_agent, optimize_agent, merge_agent, table_agent, toc_agent, git_grammar_agent), `ww/ml/`, `ww/torch_llm/`, `ww/mmlu/`, `ww/trading/`, `ww/social/`, `ww/crawler/`, `ww/bot/`, `ww/selenium/`, `ww/ansible/`, `ww/arduino/`, `ww/canvas/`, `ww/graph/`, `ww/kalman/`, `ww/langchain_test/`, `ww/linear/`, `ww/ocr/`, `ww/pico/`, `ww/pl/`, `ww/plot/`, `ww/postgres/`, `ww/scheme/`, `ww/supabase/`, `ww/tooluse/`, `ww/video/`, `ww/vscode/`, `ww/wandbrun/`, `ww/youtube/`, `ww/auto_ss_config/`, `ww/cloud/`, `ww/encoding/`, `ww/content/`, `ww/pyperclip_client/`

### Pre-commit Hooks (6 repos)

1. **pre-commit-hooks** — trailing whitespace, EOF fixer, YAML/TOML check, merge conflict, debug statements, AST check, large files (500KB)
2. **ruff** — lint + format
3. **pyright** — type checking (basic mode, with 12 additional deps)
4. **bandit** — security scan (22 rules skipped)
5. **detect-secrets** — secret detection with baseline
6. **local pytest** — `uv run python -m pytest tests/ -x -q --tb=short`

### CI Workflows (3)

1. **Lint & Security** (`lint.yml`) — ruff check, ruff format, pyright, bandit, pip-audit. Runs on push/PR to `ww/**`, `pyproject.toml`, `.pre-commit-config.yaml`
2. **Unit Test** (`unit_test.yml`) — `unittest discover` + coverage (fail-under 60%). Runs on push/PR to `ww/**`, `tests/**`
3. **Integration Test** (`integration_test.yml`) — `unittest discover integration_tests`. Runs on push/PR to `ww/**`, `integration_tests/**`

### Tests

- ~50 test files in `tests/` using unittest style
- conftest.py defers `test_audio_pipeline` (mocks sys.modules)
- Coverage threshold: 60%
- No test suite for most unwired modules

### Build & Tooling

- **Build**: Hatchling
- **Package manager**: uv
- **Python**: >=3.11
- **Linting**: Ruff (intentional exclusions: E731, E722, F841)
- **Type checking**: Pyright basic mode, excludes ml/macos/trading/wandbrun/tests/arduino/ansible/pico
- **Security**: Bandit skips 22 rules, detect-secrets with baseline
- **No test framework**: pytest for running, unittest for writing

### Key Observations

1. **main.py is the bottleneck** — 1,573 lines of elif chains. Adding a command requires editing 3 places: the module, the dispatcher, and the help text. This is fragile but simple.

2. **Agent modules are built but hidden** — `ww/agent/` has 8+ agents (code, fix, refactor, optimize, merge, table, toc, git-grammar) that could be high-value if wired up.

3. **CI inconsistency** — pre-commit runs pytest, CI runs unittest discover. Both work but produce different output formats and may discover tests differently.

4. **Integration tests are empty** — workflow exists, triggers, runs a placeholder. Either populate or remove.

5. **Heavy LLM integration** — OpenRouter client supports streaming + non-streaming, used across git, notes, search, audio, image gen. Model selection via env var.

6. **Cross-platform focus** — macOS and Linux paths separated, conditional pyobjc deps, platform-specific commands (ghostty, display, alarm are macOS-only).

7. **No dependency management automation** — all versions pinned manually, no Dependabot/Renovate.

8. **No release/publish workflow** — no PyPI publishing, no GitHub releases, no changelog generation.

### What's Missing

| Gap | Impact |
|-----|--------|
| No `ww doctor` (self-diagnostic) | Debugging broken env is manual |
| No `ww git blame-ai` | Differentiator for AI-first CLI |
| No `ww db export` (CSV/JSON) | Can't analyze usage patterns easily |
| No `ww openrouter budget` | Spend tracking without alerts |
| Agent modules unwired | Built code sitting idle |
| No Dependabot | Deps go stale |
| No release workflow | Manual publishing |
| CI doesn't run detect-secrets | Bypassable via `--no-verify` |
| CI doesn't cache uv deps | Slow CI runs |
| No bash/fish completions | Only zsh supported |
| No CONTRIBUTING.md | Onboarding friction |
| No type stubs or mypy strict | Type safety is basic only |
| 20+ unwired modules | Code rot risk |
