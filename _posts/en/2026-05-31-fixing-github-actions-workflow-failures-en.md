---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing GitHub Actions Workflow Failures
translated: false
type: note
---

Here's the summary of what I found and fixed:

## GH Actions Failures — Root Causes & Fixes Applied

### 1. Lint & Security workflow (`lint.yml`) — ALL 3 jobs failing

**Fix applied** (`/Users/lzwjava/projects/ww/.github/workflows/lint.yml`):

- **ruff job**: Added `uv pip install ruff` after `uv sync` — ruff wasn't in pyproject.toml deps
- **pyright job**: Added `uv pip install pyright` — same issue
- **bandit job**: Added missing `uv sync` before `uv pip install bandit[toml]` — no venv existed

### 2. Unit Test workflow — 45 errors

**Fixes applied**:

- **`pyproject.toml`**: Added `PyJWT>=2.0.0` to dependencies (12 jwt-related test errors)
- **`tests/test_main.py`**: Updated `_run()` helper with `sys.modules` fallback for modules that can't be imported (macOS-only on Linux). Added `MagicMock` import.
- **`tests/test_main_extended.py`**: Updated `_dispatch()` with same `sys.modules` fallback pattern
- **Note tests**: Added `patch.dict(os.environ, {"NOTE_ENTER_CONFIRM": "1"})` to ensure the `input()` mock is reached (was falling through to `note_workflow.main()` which hit a ValueError)
- **Update test**: Changed `["ww", "update"]` → `["ww", "projects", "update"]` (command moved under `projects` group)
- **Ruff f-string**: Fixed `f"\n--- Creating ---"` → `"\n--- Creating ---"` in `ww/amd_dev_cloud/start_train.py`

### 3. Integration Test workflow — directory missing

**Fix applied**: Created `integration_tests/__init__.py`

### Remaining ~20 pre-existing errors (NOT from my commits)

These are all `ModuleNotFoundError` from optional deps not in `pyproject.toml`:

| Test file | Missing module |
|-----------|---------------|
| `tests/auto_ss_config/test_lightsail.py` | `yaml` (PyYAML) |
| `tests/bot/test_punch_bot.py` | `pytz` |
| `tests/cloud/test_ec2.py` | probably `yaml` |
| `tests/ml/test_w2v_utils.py` | `torch` |
| `tests/ml/test_word_vectors.py` | `torch` |
| `tests/crawler/test_weibo.py` | selenium/weibo deps |
| `tests/agent/test_agents.py` | `frontmatter` |

These tests fail at **import time** — the test module itself can't be loaded because the source module imports heavy/optional deps at the top level. The fix for each is wrapping with `try/except ImportError` + `unittest.skip()`:

```python
try:
    from ww.auto_ss_config import lightsail
except ImportError:
    lightsail = None

@unittest.skipUnless(lightsail, "Missing optional dependency: PyYAML")
class TestGetLightsailInstances(unittest.TestCase):
    ...
```

Would you like me to continue and fix those remaining test files too?
