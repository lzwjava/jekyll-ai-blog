---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 液体语法检查测试与钩子
translated: true
type: note
---

已完成。以下是摘要：

**新增内容：**

1. `tests/workflow/test_liquid_syntax.py` — 扫描 `_posts/` 和 `notes/` 目录，查找 `{% raw %}{% %}{% endraw %}` 标签外部的裸 `{% raw %}{% %}{% endraw %}`。报告每个违规的文件路径、行号和内容。

2. `.pre-commit-config.yaml` — 新增 `liquid-syntax-check` 钩子，每次提交时运行该测试（`always_run: true`）。

**工作原理：**

- 查找所有 `{% raw %}{% %}{% endraw %}` 模式（会导致致命 `Liquid::SyntaxError` 的空 Liquid 标签）
- 检查每个出现位置是否位于以下之一内部：
  - 文件级别的 `{% raw %}...{% endraw %}` 包裹
  - 内联的 `{% raw %}{% %}{% endraw %}` 转义
- 报告违规并提供清晰的修复说明

**已修复：** `notes/2026-06-14-liquid-tag-build-fix-en.md` 中有 3 个裸 `{% raw %}{% %}{% endraw %}` — 已通过内联 raw/endraw 转义。

**注意：** bandit 存在一个与此更改无关的预先存在的误报（`scripts/recommendation/api_utils.py` 上的 B608）。您可能希望将 B608 添加到跳过列表中。
