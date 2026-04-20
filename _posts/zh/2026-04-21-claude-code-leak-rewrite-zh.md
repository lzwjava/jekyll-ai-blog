---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 克劳德代码泄密事件重述
translated: true
type: note
---

问题：什么是 `ultraworkers/claw-code` GitHub 仓库，是否值得使用？

回答：

## `ultraworkers/claw-code` 概述

该仓库背后有一段戏剧性的故事，解释了它是什么以及为何迅速走红。

### 起源：Claude Code 泄露事件

2026年3月31日，Anthropic 在一次 Claude Code npm 更新中意外包含了一个 `.map` 源码映射文件。几分钟内，这60万行代码被镜像、分析、移植到 Python 及其他语言，并在互联网上广泛传播。

此次泄露暴露了约512,000多行 TypeScript 代码、44个隐藏功能开关、一个名为 KAIROS 的后台常驻智能体，以及一个旨在隐藏 Anthropic 员工对开源项目贡献的隐身模式。

### `claw-code` 的真实性质

`claw-code` **并非泄露的专有代码的直接转储**。维护者谨慎地避免了存储原始的泄露代码快照，而是专注于一个功能性的、以 Python 优先的重写版本以及一个高性能的 Rust 移植版本。

该仓库最初作为一个镜像诞生，后来演变为对 Claude Code 应用程序的完整重写——先是用 Python，随后用 Rust，并在 GitHub 上获得了超过10万颗星标——使其成为 GitHub 历史上增长最快的仓库，甚至超越了之前的记录保持者。

如今，该仓库是一个**以 Rust 为主的项目**（92.9% Rust，7.1% Python），主要包含以下组件：
- `crates/api-client` — 带有供应商抽象和流式处理的 API 客户端
- `crates/runtime` — 会话状态、MCP 编排、提示词构建
- `crates/tools` — 工具清单定义和执行框架
- `crates/claw-cli` — 交互式 REPL 和项目引导流程

### 它是否“优秀”？一份诚实的评估

**优点：**
- **庞大的社区关注度** — 153k 星标和 101k fork 数量前所未有
- **净室实现方法** — 旨在通过从头重新实现架构来避免直接的版权侵权
- **Rust 移植版** — 旨在提供一个比原版 TypeScript 更快、内存安全的智能体运行时框架
- **教育价值** — 对于研究 AI 智能体框架工程、工具连接和编排模式很有帮助

**缺点 / 注意事项：**
- Python 工作区尚未成为原版系统的完整一对一替代品；它仍然比归档的源码包含更少的可执行运行时片段。
- **法律地位不确定** — claw-code 的法律状态仍未明确。截至2026年4月初，尚未有针对该净室重写版本的法律诉讼，但 Anthropic 也未发布正式的事后分析报告。
- **所有权处于变动中** — 仓库本身注明*在所有权转移期间暂时锁定*，活跃的维护工作已在 `ultraworkers/claw-code-parity` 进行。
- **生态系统中的恶意软件风险** — 一个恶意的 GitHub 仓库利用 Claude Code 泄露事件作为诱饵，分发了一个信息窃取程序（Vidar）和一个伪装成泄露源码档案的代理恶意软件（GhostSocks）。请务必核实从相关仓库下载的内容。

### 最终结论

`claw-code` 是一个**引人入胜的工程和社区现象**，对于学习 AI 智能体框架设计很有帮助。然而，它**尚未达到生产就绪状态**，无法作为 Claude Code 的完整替代品，其法律状态尚未解决，且其周围的生态系统已被恶意软件的仿冒品污染。如果您是开发者，对智能体内部机制感到好奇，Rust 移植版本值得探索——但请谨慎操作，并仅从已验证的仓库获取。

参考文献：

- [泄露的 Claude Code 源码催生了 GitHub 历史上增长最快的仓库 – Cybernews](https://cybernews.com/tech/claude-code-leak-spawns-fastest-github-repo/)
- [深入探究 Claude Code 源代码泄露事件 – Engineers Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code)
- [Claude Code 泄露的源代码在哪里？ – Medium](https://medium.com/data-science-in-your-pocket/where-is-claude-code-leaked-source-code-9a5b1d00cd2a)
- [伪造的 Claude Code 源码下载传播恶意软件 – The Register](https://www.theregister.com/2026/04/02/trojanized_claude_code_leak_github/)
- [512,000行代码，一夜之间：净室 AI 的法律危机 – Bean Kinney](https://www.beankinney.com/512000-lines-one-night-zero-permission-the-claude-code-leak-and-the-legal-crisis-of-ai-clean-rooms/)
- [Claude Code 在源码泄露数天后出现关键漏洞 – SecurityWeek](https://www.securityweek.com/critical-vulnerability-in-claude-code-emerges-days-after-source-leak/)