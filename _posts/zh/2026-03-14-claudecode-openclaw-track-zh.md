---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 OpenClaw Tools 中跟踪 Claude 代码
translated: true
type: note
---

问题：如何监控 Claude Code 在 OpenClaw 中的进度并查看它当前在做什么？

回答：

## 在 OpenClaw 中监控 Claude Code 进度

我没有 OpenClaw 确切 UI 的具体文档，所以让我给出最好的通用答案，并建议如何找出。问题：如何监控并检查 Claude Code 在 OpenClaw 中当前在做什么？

回答：

## 如何在 OpenClaw 中监控 Claude Code 进度

有几种方法，从简单到复杂：

---

### 🥇 选项 1：ClawPort（最佳可视化仪表板）

ClawPort 是 Claude Code 代理团队的免费开源可视化命令中心。它提供 org map、agent chat、kanban board、cron pipeline monitor、cost dashboard、live log streaming 和 memory browser——全部在一个仪表板中。

Install it:
```bash
npm install -g clawport
clawport setup   # auto-detects your OpenClaw workspace
clawport dev     # launches the dashboard
```

What you can see:
- 哪个代理正在运行以及它当前使用什么工具
- Kanban board：queued → in progress → done
- Live log stream
- 每个代理的 Token 使用量和成本

---

### 🥈 选项 2：claw-monitor（终端仪表板）

claw-monitor 是一个终端仪表板，提供实时会话跟踪，显示当前执行的工具和总工具调用次数、每个会话的经过时间，以及代理详细信息视图——使用箭头键选择代理，按 Enter 展开最近的工具和错误。

它实时监视 `~/.openclaw/agents/main/sessions/` 和 `sessions.json`。

---

### 🥉 选项 3：CLI 状态检查（最快）

启动会话后，可以使用 `claude-code-skill session-status myproject` 直接从命令行检查会话状态。

```bash
# Check what a session is doing
claude-code-skill session-status myproject

# Stream live output
claude-code-skill session-send myproject "status update" --stream
```

---

### 📋 监控时要关注什么

| Signal | Meaning |
|--------|---------|
| Tool calls increasing | 它正在积极工作 |
| Same tool repeating | 可能陷入循环 |
| No activity for 5+ min | 可能需要推动或遇到错误 |
| "Write" tool firing | 它正在创建/编辑文件 |
| "Bash" tool firing | 它正在运行命令 |

---

### ✅ 推荐工作流程

```
在 OpenClaw 中启动任务
    ↓
打开 ClawPort 仪表板（或 claw-monitor）
    ↓
每 10-15 分钟检查一次
    ↓
如果卡住 → 在 ClawPort 聊天中直接向代理发送消息
    ↓
完成时 → 检查输出文件
```

---

### 💡 关键洞见

OpenClaw 最好被视为“运营团队”——它日常运行事务、监控并执行重复流程——而 Claude Code 是构建的“工程团队”。对于你的 Todo app 任务，Claude Code 正在构建，你使用 ClawPort 或 claw-monitor 来实时观看。

参考资料：

- [ClawPort - AI Agent Command Center](https://www.clawport.dev/)
- [claw-monitor on GitHub](https://github.com/DanWahlin/claw-monitor)
- [openclaw-claude-code-skill on GitHub](https://github.com/Enderfga/openclaw-claude-code-skill)
