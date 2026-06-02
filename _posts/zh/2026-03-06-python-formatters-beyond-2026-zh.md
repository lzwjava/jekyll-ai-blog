---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越 Black 的 Python 格式化工具 2026
translated: true
type: note
---

**问题：** 除了 Black 之外，还有哪些 Python 格式化工具？

**回答：**

以下是除了 **Black** 之外最受欢迎且积极维护的 Python 代码格式化工具（截至 2025–2026 年）：

- **ruff format**
  极快（用 Rust 编写），在 2024–2026 年非常流行，默认 90–95% 与 Black 兼容，正在成为许多项目的新事实标准。

- **isort**
  仅排序 import 语句（不是完整的格式化工具），但仍与 Black 或其他工具一起广泛使用。

- **autopep8**
  自动将代码格式化为符合（大部分）PEP 8。保守、可配置，但比 Black/ruff 慢且意见较弱。

- **yapf**
  Google 的格式化工具。高度可配置——可以使其行为非常接近 Black、PEP 8 或完全自定义风格。

- **blue**
  几乎与 Black 相同，但行长度为 79 个字符（而非 88），以匹配旧项目 / flake8 默认值。

- **blacken-docs**
  使用 Black 格式化文档（Markdown、RST 等）中的代码块。

- **docformatter**
  格式化 docstring（主要是 PEP 257 / Google / NumPy 风格）。

- **pyink**
  Meta 对 Black 的 fork，带有一些额外的默认值/调整（在 Meta 内部使用）。

- **darker**
  仅格式化更改的行（在 pre-commit + CI 中有用，可避免大范围重新格式化提交）。

**快速比较（2025–2026 年受欢迎程度与理念）：**

| Formatter      | Speed       | Opinionated? | Black-compatible? | 当前主要用例                           | 是否活跃维护 |
|----------------|-------------|--------------|---------------------|------------------------------------------|--------------|
| ruff format    | ★★★★★       | 是           | ~95%                | 在新项目中取代 Black                     | 非常活跃     |
| Black          | ★★★★        | 非常         | —                   | 仍是常见基准                             | 活跃         |
| yapf           | ★★          | 否           | 可配置              | 希望完全控制风格的团队                   | 活跃         |
| autopep8       | ★★          | 否           | 否                  | 传统 / 保守项目                          | 活跃         |
| blue           | ★★★★        | 非常         | 几乎                | 坚持 79 字符行长的项目                   | 低活跃度     |

**2026 年最常见选择：**

1. **ruff format**（通常简称 **ruff**）——增长最快
2. **Black** —— 仍被广泛使用
3. **Black + isort**（或 **ruff format + ruff check --select I**）
4. **yapf** —— 主要在有自定义风格指南的公司中使用

**2026 年底线：**
如果您要启动新项目 → **ruff format** 目前是大多数团队的最强默认选择。

**参考资料：**

- [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff)
- [https://black.readthedocs.io/](https://black.readthedocs.io/)
- [https://github.com/google/yapf](https://github.com/google/yapf)
- [https://pypi.org/project/autopep8/](https://pypi.org/project/autopep8/)
