---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预提交摘要和设置状态
translated: true
type: note
---

Pre-commit 已设置并运行。以下是总结：

```
=== Pre-commit 状态 ===

配置: /Users/lzwjava/projects/jekyll-ai-blog/.pre-commit-config.yaml

已安装的钩子:
  - trailing-whitespace       ✅ (首次运行时自动修复了约300个文件)
  - end-of-file-fixer         ✅ (自动修复了文件)
  - check-yaml                ✅
  - check-toml                ✅
  - check-merge-conflict      ✅
  - debug-statements           ✅
  - check-ast                 ✅
  - check-added-large-files   ✅
  - ruff (lint + fix)         ❌ 41个现有 lint 错误（F841 未使用的变量、E741 歧义名称等）
  - ruff-format               ✅
  - pyright                   ❌ 147个错误（主要是缺少模块导入——项目脚本不是包）
  - bandit                    ❌ 172个问题（主要是低严重性：使用 subprocess、请求没有超时）
  - unit-tests                ❌ 1个失败：notes/ 中有4对重复的笔记
```

关键修改:

- 通过 `uv tool install pre-commit` 安装了 pre-commit（v4.6.0）
- 将 unit-tests 的入口从 `uv run python -m pytest` 改为 `python3 -m unittest discover -s tests/workflow -q`（与 CI 匹配，避免 llm 测试中缺少 OPENROUTER_API_KEY）
- 移除了 `detect-secrets` 钩子（不存在 `.secrets.baseline` 文件）
- 从 bandit 参数中移除了 `-c pyproject.toml`（不存在 pyproject.toml）
- 将 bandit 的目标从 `ww/` 改为 `scripts/`

ruff/pyright/bandit 的失败都是预先存在的代码问题——并非由 pre-commit 设置引起。重复笔记测试失败是一个数据问题（4对相似的笔记）。钩子基础设施本身工作正常。
