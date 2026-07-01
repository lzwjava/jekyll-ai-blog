---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按目录过滤预提交钩子
translated: true
type: note
---

**问题：** 如何在 pre-commit hook 中指定仅某些子目录（例如，用于 `ruff-check`）？

---

**答案：**

在 `.pre-commit-config.yaml` 中，有 **两个键** 用于按路径过滤：

| 键 | 用途 |
| --- | --- |
| `files` | **仅包含**匹配此 regex 模式的 files |
| `exclude` | **跳过**匹配此 regex 模式的 files |

两者均接受针对相对于 repo 根目录的文件路径的 Python regular expressions。

---

## 方法 1 — 使用 `files:` 仅包含特定子目录

仅在 `src/` 和 `tests/` 上运行 ruff：

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

## 方法 2 — 使用 `exclude:` 跳过某些子目录

在除 `docs/` 和 `migrations/` 外的所有内容上运行 ruff：

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

## 方法 3 — 用于多个路径的详细 regex（更简洁的语法）

当 regular expression 对于多个路径变得繁琐时，您可以使用 YAML 的多行字面量结合 `(?x)` verbose regex flag：

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

## 方法 4 — 全局 exclude（适用于所有 hooks）

您还可以在配置文件根部设置顶级的 `exclude`，使其适用于每个 hook，而无需在每个 hook 中重复：

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

## 重要：Ruff 的 `force-exclude`

`ruff-pre-commit` hooks 默认使用 `--force-exclude`，这确保了即使 pre-commit 在命令行上显式传递文件，Ruff 也会尊重排除模式。这意味着 Ruff 在 `pyproject.toml` 中的自己的 `exclude` 也会被尊重。但是，如果您遇到 `pyproject.toml` 中的 `exclude` 被忽略的情况，最安全的解决方案是在 ruff hook 的 `.pre-commit-config.yaml` 中直接添加 `exclude` 模式。

---

## 组合真实世界示例

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

**参考资料：**

- [pre-commit official docs – filtering](https://pre-commit.com/#filtering-files-with-types)
- [astral-sh/ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- [DeepWiki – ruff-pre-commit hooks](https://deepwiki.com/astral-sh/ruff-pre-commit/3-pre-commit-hooks)
- [Stefanie Molin – Pre-Commit Setup Guide](https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/)
