---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repo Analysis and Improvement Suggestions
translated: false
type: note
---

Now I have a thorough picture of the codebase. Here's my analysis:

---

## Analysis of `ww` repo

**What exists:**
- 90+ command modules in a flat `main.py` dispatcher (~1573 lines)
- Pre-commit: trailing whitespace, ruff, pyright, bandit, detect-secrets, pytest
- CI: 3 workflows (lint, unit test, integration test)
- SQLite command logging (`ww/db.py`)
- Tests in `tests/` (unittest-style, run via pytest in pre-commit)
- Integration tests dir exists but is a placeholder (`test_placeholder.py`)
- ~20+ unwired modules (ml, agent, trading, social, crawler, bot, etc.)

**Current issues spotted:**
1. CI uses `unittest discover`, pre-commit uses `pytest` — inconsistent
2. CI doesn't run detect-secrets (only in pre-commit)
3. Integration test workflow triggers on `integration_tests/**` but there's only a placeholder
4. No dependency caching in CI (setup-uv but no cache)
5. Ruff version `v0.9.10` in pre-commit but `0.14.13` in `.ruff_cache` — stale

---

## Suggestions for what to add

### High impact, low effort

1. **Unify CI to use pytest** — Change unit_test.yml from `unittest discover` to `uv run pytest tests/ -x -q`. This matches pre-commit and gives consistent behavior.

2. **Add `detect-secrets` to CI** — Currently only in pre-commit. If someone bypasses pre-commit (`--no-verify`), secrets can slip through. Add a step in lint.yml.

3. **Add dependency caching to CI** — `astral-sh/setup-uv` supports caching. Add `enable-cache: true` to speed up workflows.

4. **Add Dependabot or Renovate** — Auto-update deps in `pyproject.toml` and pre-commit hook revs. Currently everything is manual.

5. **Delete the integration test placeholder** or replace it with real tests. The workflow exists, triggers, and does nothing useful — just noise.

### Medium impact

6. **Add `ww doctor`** — A self-diagnostic command that checks: Python version, .env keys present, proxy reachable, OpenRouter API responding, disk space, GPU available. You already have `_check_proxy()` and env loading — just compose them.

7. **Add `ww openrouter cost`** — Your activity command shows spend, but a quick "how much did I spend today/this week" one-liner would be useful given you consume ~1.5B tokens/year. The data is already in `get_activity()`.

8. **Add `ww db export`** — Export command history to CSV/JSON for analysis. The SQLite DB already tracks everything.

9. **Wire up `ww/agent/` modules** — You have `code_agent`, `fix_agent`, `refactor_agent`, `optimize_agent`, `merge_agent` etc. sitting unwired. These are high-value for your AI-first workflow.

10. **Add `ww llm cost`** — Per-model cost breakdown from OpenRouter, similar to `openrouter activity` but focused on cost optimization (cheapest model for task type, waste detection).

11. **Add `ww db autocomplete`** — Command suggestion based on history frequency. You already have `db top` — extend it to feed zsh completion.

### Nice to have

12. **Add ruff rules `I` (isort)** and `UP` (pyupgrade) — You're already using ruff-format, adding import sorting and pyupgrade is free.

13. **Add `coverage` to CI with `--fail-under`** — Already there at 60%, but add a coverage upload step (Codecov or Coveralls) for PR comments.

14. **Add `pre-commit autoupdate` to a monthly cron** — Keeps hook revs fresh.

15. **Add `ww openrouter budget`** — Set a monthly budget, alert when approaching. The management API has limit info already.

16. **Add `ww git blame-ai`** — LLM-powered `git blame` that explains *why* a change was made, not just *who*. Feed the commit message + diff to OpenRouter.

---

## What I'd prioritize first

Given your trajectory toward AI engineering and the fact that you're the primary user:

1. **`ww doctor`** — saves debugging time when things break
2. **`ww git blame-ai`** — differentiator, leverages your LLM infrastructure
3. **Unify CI pytest** — 5 min fix, prevents confusion
4. **Wire `ww/agent/` modules** — you already built them, just expose them
5. **Dependabot** — set and forget, keeps deps fresh

Want me to implement any of these?
