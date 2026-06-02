---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw编程智能体生成指南
translated: true
type: note
---

Question: OpenClaw中的“生成编码代理”如何工作？

Answer:

## OpenClaw中生成编码代理的工作原理

OpenClaw是一个开源的个人AI代理框架。其最强大的功能之一是能够**生成子代理**——即在后台运行的代理会话，它们独立处理特定任务（例如大型代码重构），而不会阻塞您的主要代理对话。

---

### 什么是“生成编码代理”？

子代理是从现有代理运行中生成的**后台代理运行**。它们在各自的独立会话中运行（`agent:<agentId>:subagent:<uuid>`），并在完成后将结果通知给请求者的聊天频道。每个子代理运行都作为后台任务进行追踪。

这正是“立即生成编码代理，约2小时”这条消息的含义——OpenClaw即将启动一个长时间运行的编码任务（例如重写您的JSSDK + CI4控制器）作为后台代理，让您的主要会话在此期间保持空闲。

---

### 如何生成编码代理

#### 方法1：斜杠命令（手动）

```
/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]
```

spawn命令是非阻塞的；它会立即返回一个运行ID。完成后，子代理会向请求者的聊天频道发送一条摘要/结果消息。

#### 方法2：通过 `sessions_spawn` 工具（由代理触发）

主代理在其推理过程中可以内部调用 `sessions_spawn`，参数包括：

- `task`（必需）——子代理应执行的任务
- `model?` ——覆盖此子代理使用的模型
- `thinking?` ——覆盖思考级别
- `runTimeoutSeconds?` ——如果设置，则在N秒后中止
- `thread?` ——将会话绑定到聊天线程以便后续跟进
- `mode?` —— `run`（一次性）或 `session`（持久性，需要 `thread: true`）

---

### 编码代理后端（ACP代理）

OpenClaw通过后台进程将编码任务委托给Codex、Claude Code或Pi代理。适用于以下情况：(1)构建/创建新功能或应用，(2)审查PR，(3)重构大型代码库，(4)需要文件探索的迭代编码。

每个后端有不同的调用要求：

- **Codex / Pi / OpenCode** → 需要 `pty:true`（交互式终端）
- **Claude Code (`claude` CLI)** → 使用 `--print --permission-mode bypassPermissions`（无需PTY）

bash调用示例：

```bash
# 使用Codex快速一次性执行（自动批准，需要PTY）
bash pty:true workdir:~/project command:"codex exec --full-auto '为CI4重写JSSDK'"

# 长时间后台重构
bash pty:true workdir:~/project background:true command:"codex --yolo '重构所有CI4控制器'"

# Claude Code（无需PTY）
claude --print --permission-mode bypassPermissions '重写JSSDK模块'
```

---

### 嵌套与并发规则

默认情况下，子代理**不能**生成自己的子代理（`maxSpawnDepth: 1`）。您可以通过设置 `maxSpawnDepth: 2` 来启用一级嵌套，允许编排模式：主代理 → 编排子代理 → 工作子子代理。

每个代理会话最多可以同时有 `maxChildrenPerAgent`（默认值：5）个活跃的子代理。这可以防止单个编排代理过度扩散。

---

### 监控与控制子代理

使用 `/subagents` 来检查或控制当前会话的子代理运行：

| 命令 | 用途 |
|---|---|
| `/subagents list` | 查看所有活跃子代理 |
| `/subagents log <id>` | 查看进度/输出 |
| `/subagents info <id>` | 状态、时间戳、会话ID |
| `/subagents kill <id>` | 停止特定代理 |
| `/subagents steer <id> <msg>` | 发送任务中途指导 |

---

### 重要安全规则

切勿在 `~/Projects/openclaw/` 目录中检出分支——那是LIVE OpenClaw实例。当您在后台生成编码代理时，**请让用户保持在循环中**。开始时发送1条简短消息（说明正在运行什么以及位置）。如果代理失败或挂起，请重新生成它或询问用户指示——不要默默地接管。

切勿在OpenClaw状态目录（`$OPENCLAW_STATE_DIR`，默认为 `~/.openclaw`）内启动Codex——它会读取您的灵魂文档并搞混组织结构！

---

### 应用于您的CI4重构决策

当OpenClaw显示**“立即生成编码代理，约2小时”**时，这意味着：
1. 它将调用 `sessions_spawn` 或执行后台 `bash` 命令
2. Codex/Claude Code代理在您的项目目录中启动
3. 它自主编辑文件、运行测试并工作约2小时
4. 完成后，它会向您的聊天发送摘要
5. 您可以随时使用 `/subagents log` 监控进度

参考资料：

- [OpenClaw子代理官方文档](https://docs.openclaw.ai/tools/subagents)
- [LLMBase上的coding-agent-local技能](https://llmbase.ai/openclaw/coding-agent-local/)
- [GitHub上的openclaw/openclaw SKILL.md](https://github.com/openclaw/openclaw/blob/main/skills/coding-agent/SKILL.md)
- [OpenClaw完全指南 – Lenny's Newsletter](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building)
