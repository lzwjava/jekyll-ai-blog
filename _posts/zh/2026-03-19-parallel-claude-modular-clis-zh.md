---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用模块化 CLI 的并行 Claude 代码
translated: true
type: note
---

是的，完全正确！当你的 CLI 工具具有良好分离的 subcommands/modules 时，你可以安全地运行并行的 Claude Code 实例。以下是原因：你的直觉完全正确。以下是详细分解：

**Safe to parallelize** — 每个子目录（`github/`、`llm/`、`network/`、`search/`、`image/`）都是自包含的 subcommand。每个 Claude 实例仅修改其自身目录内的文件，因此不会有任何 merge conflicts 的风险。

**Watch the shared files** — `main.py`、`__init__.py` 和共享模块如 `utils/` 或 `env.py` 是冲突区域。两条规则：

1. 如果 Claude 实例仅 *reads* 共享文件（例如导入 `env.py` 获取配置，从 `utils/` 读取），这是安全的 — reads 绝不会冲突。
2. 如果两个实例都 *write* 到 `main.py`（例如添加新的 CLI entry point），就会产生冲突。手动协调这些更改，或分步进行 — 先完成一个实例的工作并 merge，然后再让下一个实例触及共享文件。

**Practical workflow：**
- 为每个 subcommand 启动一个 Claude Code 实例，每个实例指向其自身子目录
- 为每个实例提供限于该文件夹的 context：`claude --context github/`
- 自己处理 `main.py` / routing 更改作为 integrator，或者在 subcommand 工作完成后，以单独的 sequential 步骤进行

你的关注点分离越干净（`github/` 和 `llm/` 之间无 cross-imports 等），就能安全地运行更多的 parallelism。点击图中的任意节点以深入了解。
