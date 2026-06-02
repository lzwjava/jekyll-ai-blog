---
audio: false
generated: true
image: false
lang: en
layout: post
title: Additional Python Project Pre-commit CI Checks
translated: false
type: note
---

**Question:** What other pre-commit / CI checks can we add to a Python project beyond the ones already running?

**Answer:**

You're already running a solid baseline. Here's what's worth adding, grouped by value:

## High Value — Add These First

### `pytest` + `pytest-cov`

```yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest tests/ --tb=short -q
      language: system
      pass_filenames: false
      always_run: true
```

Coverage gate:

```yaml
entry: pytest --cov=ww --cov-fail-under=80 -q
```

### `bandit` — security linting

Catches hardcoded secrets, shell injections, unsafe `eval`, etc.

```yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.3
  hooks:
    - id: bandit
      args: ["-r", "ww/", "-ll"]  # -ll = medium+ severity only
```

### `detect-secrets`

Scans for API keys, tokens, passwords before they hit origin.

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.5.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

Init once: `detect-secrets scan > .secrets.baseline`

---

## Medium Value — Situational

### `mypy` — strict type checking

You have `pyright` already, but `mypy` catches different edge cases. Running both is overkill — stick with pyright unless a dep only has mypy stubs.

### `pip-audit` — dependency CVE scanning

```yaml
- repo: https://github.com/pypa/pip-audit
  rev: v2.9.0
  hooks:
    - id: pip-audit
```

Checks your `requirements.txt` / `pyproject.toml` against OSV/PyPI advisory DB.

### `vulture` — dead code detection

```yaml
- repo: https://github.com/jendrikseipp/vulture
  rev: v2.14
  hooks:
    - id: vulture
      args: ["ww/", "--min-confidence", "80"]
```

Useful for CLI tools like `ww` where commands accumulate.

### `interrogate` — docstring coverage

```yaml
- repo: https://github.com/econchick/interrogate
  rev: 1.7.0
  hooks:
    - id: interrogate
      args: ["-vv", "--fail-under", "70", "ww/"]
```

---

## Low Overhead — Worth Adding to `pre-commit`

```yaml
# Already have some of these, but these are commonly missed:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v5.0.0
  hooks:
    - id: check-added-large-files     # blocks files > 500KB
      args: ['--maxkb=500']
    - id: check-ast                   # Python syntax validity
    - id: check-json
    - id: check-symlinks
    - id: no-commit-to-branch         # protect main/master
      args: ['--branch', 'main']
    - id: check-executables-have-shebangs
    - id: mixed-line-ending
```

---

## CI-Only (Too Slow for Pre-commit)

These belong in GitHub Actions / GitLab CI, not local hooks:

| Check | Tool | Why CI-only |
|---|---|---|
| Integration tests | `pytest -m integration` | Needs network/AMD cloud |
| Mutation testing | `mutmut` | Takes minutes |
| Full coverage report | `pytest-cov` + Codecov | Needs upload token |
| Dependency license check | `pip-licenses` | Slow scan |
| Container scan | `trivy` | Docker required |

```yaml
# .github/workflows/ci.yml snippet
- name: pip-audit
  run: pip-audit --requirement requirements.txt

- name: bandit full scan
  run: bandit -r ww/ -f json -o bandit-report.json
```

---

## My Recommendation for `ww` Specifically

Given it's a CLI agent tool hitting AMD Dev Cloud / cloud APIs, I'd prioritize:

1. **`bandit`** — you're dealing with cloud credentials, SSH, API keys
2. **`detect-secrets`** — same reason; one leaked AMD key = expensive
3. **`pip-audit`** — you're consuming a lot of deps for LLM/cloud SDKs
4. **`check-added-large-files`** — prevents accidentally committing model weights or logs
5. **`pytest` with `--cov`** — even 60% coverage on CLI entrypoints saves debugging time

Skip `interrogate` and `vulture` until the project stabilizes — they create noise during fast iteration.
