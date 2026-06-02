---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实现 100x 工程师多代理系统
translated: true
type: note
---

问题：我们如何在技术细节上实现这个 100x engineer multi-agent system？

回答：回答：

---

## 🏗️ 完整系统架构

```
You (Human)
    ↓  [one sentence / one task]
Orchestrator
    ↓  [breaks into atomic units]
Task Queue
    ↓  [distributes]
Agent Pool ←→ Tool Layer ←→ Codebase
    ↓  [stuck?]
Notification Layer
    ↓  [IM ping to you]
You unblock → Agent continues
    ↓
Auto merge + deploy
```

---

## 🧱 Layer 1 — The Orchestrator

这是**大脑**——唯一直接与您对话的层。

**它做什么：**

- 接收您的单行指令
- 将其分解为原子化的、独立的 tasks
- 每个 task 必须：自包含、有明确的成功标准、不依赖其他进行中的 task
- 将 tasks 分配给 agent pool
- 监控死循环并升级

**如何构建它：**

```python
# Orchestrator prompt pattern
system = """
You are a task decomposition engine.
Given a feature request, break it into atomic tasks.
Each task must:
- Be completable in one agent session
- Have a clear DONE condition
- List all files likely to be touched
- List all tools required
- Have zero dependency on incomplete tasks

Output format: JSON array of tasks
"""
```

**关键原则：** 一个 planning agent 解释 ticket，然后下游 agents 处理实现——这种 pipeline 结构解锁了单模型方法无法实现的并行性。

---

## 🧱 Layer 2 — The Agent (No Role Division)

每个 agent 都是**相同的**——没有 dev agent，没有 test agent。只有配备所有 tools 的 agent。

**一个 agent 拥有什么：**

```
- Full codebase access (read/write)
- Terminal access (run commands)
- Git access (branch, commit, PR)
- Test runner access
- Browser automation (Puppeteer/Playwright)
- IM/notification access (to escalate)
```

**Agent loop：**

```
1. Receive task + context
2. Read relevant files
3. Write technical plan
4. Implement
5. Run tests
6. Fix failures
7. Verify end-to-end
8. Commit + open PR
9. If stuck > N attempts → notify human
```

**为什么一个 agent 拥有所有 tools：** 为 agents 提供 browser automation tools 会显著提升性能——agent 可以识别并修复仅从代码无法明显的 bug，以真实人类用户的方式测试功能。

---

## 🧱 Layer 3 — Task Queue & Parallelism

这里是 100x 真正发生的地方——**纯并行执行**。

**实现：**

```python
# Simple task queue
task_queue = [
  { id: "t1", title: "Add login endpoint", status: "pending" },
  { id: "t2", title: "Write auth middleware", status: "pending" },
  { id: "t3", title: "Add user profile page", status: "pending" },
  # ... N tasks
]

# Spawn N agents in parallel
for task in task_queue:
    spawn_agent(task)  # each runs independently
```

**关键洞见：** 对于大多数工作流，3 到 7 个 agents 效果最佳——低于 3 个时单个 agent 就足够，超过 7 个时协调复杂性会超过收益，除非使用分层结构。

**每个 agent 都有自己的：**

- Git branch
- Sandbox environment
- Context window (fresh, no pollution from other agents)

---

## 🧱 Layer 4 — Dead Loop Detection

这是最具人类价值的关键层——**系统中您存在的唯一原因**。

**死循环的样子：**

```
Agent tries solution A → fails
Agent tries solution B → fails
Agent tries solution C → variation of A → fails
Agent tries solution D → variation of B → fails
... forever
```

**如何检测它：**

```python
def detect_loop(agent_history):
    # Check if last N attempts are semantically similar
    recent_approaches = agent_history[-5:]
    similarity_score = embed_and_compare(recent_approaches)

    if similarity_score > 0.85:  # too similar = looping
        escalate_to_human(agent_id, summary)
```

**升级的样子：**

```
[IM Notification]
🚨 Agent t3 is stuck

Task: Add OAuth login
Tried: 4 approaches
Last error: "redirect_uri mismatch"
Attempts look similar — possible loop

Reply with hint or unblock:
> The redirect URI needs to match exactly what's in Google Console
```

诸如非确定性和 agents 陷入重复模式等持久挑战依然存在——关键是构建外部升级机制，以便人类仅在 agents 真正无法自我纠正时介入。

---

## 🧱 Layer 5 — Notification Layer (Push, Not Pull)

您**绝不检查仪表板**。系统主动与您对话。

**渠道：**

- Telegram Bot (simplest)
- Slack Bot
- WhatsApp via Twilio
- 任何有 API 访问的 IM

**通知类型：**

| Type | When | Action Required |
|---|---|---|
| 🚨 **Stuck** | Agent looping | Reply with hint |
| ✅ **Done** | Task complete, PR open | Review or auto-merge |
| ⚠️ **Permission** | Agent needs access | Grant or decline |
| 💀 **Crash** | Agent environment died | Restart or reassign |
| 📋 **Daily Summary** | End of day | Read or ignore |

**实现：**

```python
async def notify_human(type, agent_id, context):
    message = format_message(type, agent_id, context)
    await telegram.send(HUMAN_CHAT_ID, message)

    # Wait for reply
    reply = await wait_for_reply(timeout=30min)
    return inject_reply_into_agent_context(reply)
```

---

## 🧱 Layer 6 — Full Permissions Model

Agents 绝不能被权限阻塞。**这是扼杀流程的东西**。

**Agents 需要访问什么：**

```yaml
permissions:
  - git: read/write all repos
  - filesystem: full project directory
  - terminal: run any command
  - env_vars: all secrets in vault
  - deploy: staging environment
  - database: staging DB
  - external_apis: all keys in vault
```

**安全模型：**

- **staging/dev** 上完全权限——绝不生产环境
- 生产部署需要一人确认（单个 IM 回复）
- 所有 agent 操作均记录以供审计

---

## 🧱 Layer 7 — Auto Merge & Deploy Pipeline

当 agent 完成时，它应以最小摩擦自动流入生产。

```
Agent opens PR
    ↓
Auto: run full test suite
    ↓
Auto: run integration tests
    ↓
Auto: visual diff (if UI change)
    ↓
Pass? → notify human "PR ready, merge?"
    ↓
Human replies "yes" (or auto-merge if confidence high)
    ↓
Auto deploy to staging
    ↓
Auto smoke test
    ↓
Auto deploy to production
```

这些系统可以接收自然语言的功能请求，探索 codebase，编写实现，生成 tests，在 sandboxed environment 中运行这些 tests，并在人类审查前迭代失败。

---

## 🛠️ Tech Stack Recommendation

| Layer | Tool |
|---|---|
| **Orchestrator** | Claude API (claude-sonnet-4) |
| **Agent runtime** | Claude Code SDK / OpenHands |
| **Task queue** | Redis Queue or simple SQLite |
| **Git operations** | GitHub API + CLI |
| **Notifications** | Telegram Bot API |
| **Environment** | Docker containers per agent |
| **Secrets** | HashiCorp Vault or .env managed |
| **Monitoring** | Simple SQLite log per agent run |

Anthropic 的 MCP (Model Context Protocol) 标准化了 agents 访问 tools 和外部资源的方式——不再需要每个连接的自定义集成。

---

## 📐 The Minimal MVP to Build First

不要一次性构建一切。按此顺序构建：

```
Week 1: One agent + one task + Telegram notification
Week 2: Task decomposition (orchestrator)
Week 3: Parallel agent pool (2-3 agents)
Week 4: Dead loop detection + escalation
Week 5: Auto PR + merge pipeline
Week 6: Full permissions + secrets vault
```

---

## 💡 The North Star Metric

> **每小时您的注意力完成多少 tasks？**

从 1:1 开始（您做一切）。
10x = 每小时注意力 10 个 tasks。
100x = 每小时注意力 100 个 tasks。

**通过每周使您的干预更少、更快、更精准来实现。**

References:

- [Effective harnesses for long-running agents — Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Multi-Agent AI Systems 2026 — DEV Community](https://dev.to/synsun/multi-agent-ai-systems-are-transforming-enterprise-development-the-trend-reshaping-tech-in-2026-g33)
- [How to Build Multi-Agent Systems 2026 — DEV Community](https://dev.to/eira-wexford/how-to-build-multi-agent-systems-complete-2026-guide-1io6)
- [Autonomous Coding Agents — C3 AI](https://c3.ai/blog/autonomous-coding-agents-beyond-developer-productivity/)
