---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 启用 Hermes Agent 的危险跳过权限标志
translated: true
type: note
---

**问题：** 如何在 Hermes 代理中使用 Claude Code 时启用 `--dangerously-skip-permissions` 标志？

**答案：**

根据 Hermes 启动 Claude Code 的方式（交互模式 tmux、打印模式或通过持久设置文件），有三种方法。

---

## 选项 1：通过 tmux 的交互模式（Hermes 中最常用）

Hermes 使用 tmux 编排 Claude Code 的交互模式。你可以像这样使用权限绕过标志启动：

```bash
# 步骤 1：在 tmux 中带标志启动 Claude Code
tmux send-keys -t claude-work 'claude --dangerously-skip-permissions "你的任务"' Enter

# 步骤 2：处理首次信任对话框（按 Enter 选择默认的"Yes"）
sleep 4 && tmux send-keys -t claude-work Enter

# 步骤 3：处理权限对话框（按向下箭头然后 Enter 接受）
sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter

# 步骤 4：等待并捕获输出
sleep 15 && tmux capture-pane -t claude-work -p -S -60
```

**重要提示：** 在对某个目录首次信任接受后，信任对话框将不再出现。每次使用 `--dangerously-skip-permissions` 时，只有权限对话框会重复出现。

---

## 选项 2：打印模式（最简单——无需标志）

打印模式运行一次性任务，返回结果后退出。它会跳过所有交互式对话框——没有工作区信任提示，也没有权限确认。这使其非常适合自动化。

```bash
terminal(command="claude -p '你的任务' --allowedTools 'Read,Edit,Bash' --max-turns 10", workdir="/path/to/project", timeout=120)
```

如果你只想无中断执行而不处理权限对话框，这是**最清晰、最安全的方式**。

---

## 选项 3：持久设置（推荐日常使用）

在项目的 `.claude/settings.json` 中设置 `defaultMode`，使该目录中的每个会话自动启用绕过模式：

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

`--dangerously-skip-permissions` 标志等同于 `--permission-mode bypassPermissions`。管理员可以通过在托管设置中将 `permissions.disableBypassPermissionsMode` 设置为 `"disable"` 来阻止此模式。

---

## 选项 4：Hermes IDE 向导（图形界面复选框）

如果你想要完全异步的操作，请在 Hermes 向导中启用"自动批准所有操作"。这对应于 `--dangerously-skip-permissions`，允许 Claude 读取、写入和执行而无需暂停询问。

---

## ⚠️ 安全提醒

`bypassPermissions` 无法防范提示注入或意外操作。在 Linux 和 macOS 上，当以 root 或 sudo 身份运行时，Claude Code 会拒绝在此模式下启动。

使用前的最佳实践：**始终先 `git commit` 你的工作**，这样如果 Claude 做了意外的事情，你可以 `git reset`。

**参考资料：**

- [Hermes Agent – Claude Code Skill 文档](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)
- [Claude Code – 选择权限模式](https://code.claude.com/docs/en/permission-modes)
- [如何通过 Hermes IDE 从 Telegram 控制 Claude Code](https://medium.com/@anhaia.gabriel/how-to-control-claude-code-from-telegram-using-hermes-ide-3d81c6705f8c)
- [Claude Code 自主模式指南](https://pasqualepillitteri.it/en/news/141/claude-code-dangerously-skip-permissions-guide-autonomous-mode)
