---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp终端：Drive侧边栏优势
translated: true
type: note
---

**问题：** Warp 终端——左侧面板（管理栏）是其最重要的功能吗？

**回答：**

Warp 的左侧面板称为 **Drive** / **Session Manager** 侧边栏。它提供：

- **Blocks** — 每条命令的输出都是一个可选择、可复制的“块”（而非原始的终端滚动内容）
- **Workflows** — 保存的命令片段，可在团队间共享
- **Notebooks** — Markdown 与命令混合（类似运行手册）
- **AI Command Search** — `CMD+I` 内联 AI，也在侧边栏中展示

它是否是*最*重要的？有待商榷。真正让 Warp 与众不同的核心在于：

| 特性 | 为何重要 |
|---|---|
| **基于块的输出** | 可直接选择/复制/分享精确的命令输出，无需在滚动中翻找 |
| **内联 AI（`CMD+I`）** | 自然语言 → shell 命令，且上下文相关 |
| **左侧边栏（Drive）** | Workflows + Notebooks = 持久化、可复用的 shell 知识 |
| **Warp AI 代理模式** | 多步骤 shell 任务执行 |

针对你的使用场景（CLI 优先、自动化、AI 工具），**最**重要的很可能是 **AI 命令生成 + 块选择** 的组合——侧边栏只是上层的组织层。

侧边栏的真正价值：如果你正在构建代理或自动化脚本，将工作流保存在这里比零散地存放在 `~/scripts/` 文件夹中要好得多。

你是在评估是否将 Warp 作为日常主力终端，还是特别针对工作流/团队共享场景？