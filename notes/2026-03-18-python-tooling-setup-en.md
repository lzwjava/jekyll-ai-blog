---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Tooling Setup Guide
translated: false
type: note
---

**Question:** What does this Python project tooling recommendation document explain, covering the already set-up tools (ruff, pre-commit) and the recommended additions (uv, pyright/mypy, pre-commit hooks, pytest, bump-my-version)?

---

**Answer:**

This document is a **Python developer tooling guide** that describes what's already configured in a project and what additional tools should be added to improve code quality, safety, and developer experience. Here's a comprehensive breakdown of every section:

---

## ✅ Already Set Up

### 1. `ruff` — Linting + Formatting

Ruff is an extremely fast Python linter and code formatter, written in Rust. It is 10–100x faster than existing linters like Flake8 and formatters like Black, and supports over 800 built-in rules.

- It replaces many tools at once: Flake8, Black, isort, pydocstyle, pyupgrade, autoflake — all in one.
- It is configured in `pyproject.toml` with **targeted ignores**, meaning specific rules that don't apply to this project are suppressed so that only meaningful warnings appear.

Example `pyproject.toml` config:
```toml
[tool.ruff.lint]
select = ["E", "F", "UP", "B", "I"]
ignore = ["E501"]  # targeted ignores
```

### 2. `pre-commit` — Automated Checks Before Every Commit

`pre-commit` is a framework that installs Git hooks so that every time you run `git commit`, it automatically runs `ruff` (linting) and `ruff-format` (formatting). This prevents poorly formatted or lint-failing code from ever reaching the repository.

---

## 🔧 Recommended Additions

### 1. `uv` — Dependency Management (High Priority)

`uv` is a package and virtual environment manager from Astral — the same team that builds `ruff`. It is a replacement for `pip` and `venv`.

- **Replace** `pip install -e .` with `uv sync`
- It generates a `uv.lock` lockfile, ensuring reproducible installs across machines
- It is dramatically faster than pip

```bash
# Instead of:
pip install -e .

# Use:
uv sync
```

An official pre-commit hook is also provided at `astral-sh/uv-pre-commit`, which can keep your `uv.lock` file up to date even if your `pyproject.toml` changes.

---

### 2. `pyright` or `mypy` — Static Type Checking (Medium Priority)

These tools analyze your code **without running it** to catch type-related bugs (e.g., passing a `str` where an `int` is expected).

| Tool | Characteristics |
|---|---|
| **pyright** | Faster, made by Microsoft, used in VS Code's Pylance |
| **mypy** | Older, more mature, wider community adoption |

Add to `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.x.x
  hooks:
    - id: mypy
```

The document specifically highlights that **the biggest gap in this project is no type checking** — because the project makes LLM/external API calls and uses multi-module dispatch in `main.py`, which is exactly where type bugs are most dangerous and hardest to debug at runtime.

---

### 3. `pre-commit-hooks` — Extra Safety Hooks (High Priority)

These are lightweight, fast checks from the official `pre-commit-hooks` repo. Add them to `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v5.0.0
  hooks:
    - id: trailing-whitespace       # removes trailing spaces
    - id: end-of-file-fixer         # ensures files end with a newline
    - id: check-yaml                # validates YAML syntax
    - id: check-toml                # validates TOML syntax
    - id: check-merge-conflict      # detects unresolved merge conflict markers
    - id: debug-statements          # catches leftover print() or breakpoint() calls
```

These hooks catch common issues: trailing whitespace, missing newlines at end of file, invalid YAML syntax, and accidentally committed large files.

---

### 4. `pytest` + `pytest-cov` — Testing (Low Priority)

- **`pytest`**: The standard Python test runner for CLI tools
- **`pytest-cov`**: Adds coverage reporting (how much of your code is exercised by tests)

The document notes this is **Low Priority** because `CLAUDE.md` states there's no test suite — but a `tests/` directory does exist, suggesting tests may be added soon.

```bash
uv run pytest --cov=src tests/
```

---

### 5. `bump-my-version` — Release & Version Management (Low Priority)

This tool integrates with `pyproject.toml` and manages version bumps via CLI commands. For example, it can update `version = "0.1.0"` → `version = "0.2.0"` automatically with:

```bash
bump-my-version bump minor
```

It handles consistent versioning across files and can trigger Git tags and commits automatically.

---

## 📊 Priority Summary Table

| Priority | Tool | Reason |
|---|---|---|
| **High** | `pre-commit-hooks` | Catches whitespace, YAML, merge issues cheaply |
| **High** | `uv` | Faster installs, reproducible lockfile |
| **Medium** | `mypy` or `pyright` | API calls + multi-module code → types catch real bugs |
| **Low** | `pytest` | No test suite yet, but `tests/` dir exists |
| **Low** | `bump-my-version` | Useful once ready for versioned releases |

---

## 🔑 Key Takeaway

The document describes a **layered code quality strategy**:

1. **Format & Lint** (already done) → `ruff` + `pre-commit`
2. **Dependency Hygiene** → `uv` (lockfile, fast installs)
3. **Type Safety** → `mypy`/`pyright` (most critical gap)
4. **Commit Hygiene** → `pre-commit-hooks` (trivial to add, high value)
5. **Testing** → `pytest` + coverage
6. **Release Management** → `bump-my-version`

The author identifies **static type checking as the #1 missing piece** given the nature of the codebase (LLM API calls, external services, multi-module architecture).

---

**References:**

- [Ruff Official Docs](https://docs.astral.sh/ruff/)
- [Ruff GitHub](https://github.com/astral-sh/ruff)
- [uv pre-commit integration](https://docs.astral.sh/uv/guides/integration/pre-commit/)
- [How to set up pre-commit hooks for Python](https://pydevtools.com/handbook/how-to/how-to-set-up-pre-commit-hooks-for-a-python-project/)
- [Ruff Tutorial – Real Python](https://realpython.com/ruff-python/)
