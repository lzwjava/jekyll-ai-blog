---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可审查代理IDE ORG-II
translated: true
type: note
---

**问题：** GitHub 仓库 `yorgai/ORG2` 是什么？

**答案：**

ORG-II 是一个开源的、类 Cursor 的 agent IDE，其核心理念截然不同：**可审查性与对原始编码速度的控制**。

与 Cursor/Claude Code 的主要区别：

**架构**

- 使用 **Rust + Tauri** 构建——本地优先，磁盘占用 <100MB
- TypeScript (54%) + Rust (39%) 拆分：前端用 TS，agent 运行时用 Rust
- 使用你现有的 API 密钥（无需新订阅）

**其探索的核心洞察**——Cursor/Claude Code 将 agent 视为“外包助手”：对输出有用，但对审计是黑箱。ORG-II 将 agent 视为结构化组织中的**持久、可观察的同事**：

- **Agent 轨迹直播 + 回放**——每个 agent 会话都可以回放。你可以精确审查 agent 每一步做了什么。“AI 责备”（类似 `git blame`，但针对 agent 行为）
- **跨会话记忆 + 跨 agent 知识共享**——agent 跨会话积累上下文，而非每个对话无状态
- **长时间运行 + 定时会话**——agent 可以整夜运行、自动重启、对 CPU/RAM 可用性做出反应
- **GUI、CLI、终端、Git、浏览器、LSP、数据库工具**全部集成
- **浏览器使用 + 计算机使用**通过原生 sidecar（macOS 上的 `agent-browser`、`peekaboo`）

**状态：** v1.0.1.21，2026年6月20日发布。737 颗星，AGPL-3.0 许可证。

**为什么它对你有意义：** 这与你想构建的东西在哲学上一致——它是 agent 架构优先，而不是编辑器上的 LLM 封装。“组织级对齐”框架（将 agent 视为具有责任感的同事，而非黑箱助手）是 Claude Code/Cursor 所缺乏的上层。可回放的执行轨迹对于调试 agent 故障特别有趣，这在规模上是一个真正的痛点。

如果你正在构建 CLI agent（如 `ww`、`zz`）并关心 agent 实际行为的可审计性，值得关注。

参考：

- [yorgai/ORG2 在 GitHub 上](https://github.com/yorgai/ORG2)
