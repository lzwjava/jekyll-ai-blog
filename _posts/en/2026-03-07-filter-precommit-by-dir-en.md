---
audio: false
generated: true
image: false
lang: en
layout: post
title: Filter Pre-Commit Hooks by Directory
translated: false
type: note
---

**Question:** How do you specify only certain subdirectories in a pre-commit hook (e.g., for `ruff-check`)?

---

**Answer:**

There are **two keys** you use in `.pre-commit-config.yaml` to filter by path:

| Key | Purpose |
|---|---|
| `files` | **Include only** files matching this regex pattern |
| `exclude` | **Skip** files matching this regex pattern |

Both accept Python regular expressions matched against file paths relative to the repo root.

---

## Method 1 — `files:` to include only specific subdirs

Run ruff **only on** `src/` and `tests/`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff-check
        args: [ --fix ]
        files: ^(src|tests)/     # only run in src/ and tests/
      - id: ruff-format
        files: ^(src|tests)/
```

---

## Method 2 — `exclude:` to skip certain subdirs

Run ruff on everything **except** `docs/` and `migrations/`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff-check
        args: [ --fix ]
        exclude: ^(docs|migrations)/
      - id: ruff-format
        exclude: ^(docs|migrations)/
```

---

## Method 3 — Verbose regex for many paths (cleaner syntax)

When the regular expression becomes unwieldy with many paths, you can use YAML's multiline literal combined with the `(?x)` verbose regex flag:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff-check
        args: [ --fix ]
        exclude: |
          (?x)^(
            docs/.*|
            migrations/.*|
            legacy/.*|
            scripts/old/.*
          )$
```

---

## Method 4 — Global exclude (applies to ALL hooks)

You can also set a top-level `exclude` at the root of the config file to apply to every hook, without repeating it per hook:

```yaml
exclude: |
  (?x)^(
    docs/.*|
    migrations/.*|
    .*cache.*/.*|
    .*venv.*/.*
  )$

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff-check
        args: [ --fix ]
      - id: ruff-format
```

---

## Important: `force-exclude` for Ruff

The `ruff-pre-commit` hooks use `--force-exclude` by default, which ensures that Ruff respects exclusion patterns even when files are explicitly passed on the command line by pre-commit. This means Ruff's own `exclude` in `pyproject.toml` will also be honoured. However, if you encounter cases where `exclude` in `pyproject.toml` is being ignored, the safest solution is to also add the `exclude` pattern directly in `.pre-commit-config.yaml` for the ruff hook.

---

## Combined Real-World Example

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff-check
        args: [ --fix ]
        files: ^src/           # only lint the src/ directory
        exclude: ^src/legacy/  # but skip the legacy subfolder inside it
      - id: ruff-format
        files: ^src/
        exclude: ^src/legacy/
```

---

**References:**

- [pre-commit official docs – filtering](https://pre-commit.com/#filtering-files-with-types)
- [astral-sh/ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- [DeepWiki – ruff-pre-commit hooks](https://deepwiki.com/astral-sh/ruff-pre-commit/3-pre-commit-hooks)
- [Stefanie Molin – Pre-Commit Setup Guide](https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/)
