---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于难题的并行 AI 工作流
translated: true
type: note
---


**问题：** 对于像重新实现 AlphaGo 或改进 Transformers 这样的困难技术问题，使用 OpenClaw 结合多个会话、临时仓库目录和不同模型来并行尝试不同解决方案方法是一种好的方法吗？

**回答：**

是的——你的直觉基本上是正确的，这实际上是 2025–2026 年一个成熟且不断演进的工作流程。让我详细分解说明。

---

## 核心概念：为什么并行多会话代理有效

基本洞见很简单：LLM 的非确定性是一个特性，而不是 bug——运行 N 个并行代理会给你 N 个有效（且有意义的不同）的解决方案供选择。

对于像重新实现 AlphaGo 或实验新 Transformer 架构这样的困难研究问题，你希望**同时探索多种方法**，而不让一个会话的上下文污染另一个。这正是多会话 + 临时仓库模式所实现的。

---

## 工具：Claude Code 与 OpenClaw

你提到了“OpenClaw”——值得澄清这两个工具，因为它们扮演不同角色：


| | **Claude Code** | **OpenClaw** |
|---|---|---|
| 用途 | 基于终端的代理式编码 | 持久化个人 AI 代理/网关 |
| 会话 | 多个并行终端会话 | 具有持久内存的子代理 |
| 最适合 | 代码执行、仓库操作 | 编排、长时间运行的工作流程 |
| 模型切换 | `claude --model opus` 或 `--model sonnet` | 每个代理的模型配置 |

OpenClaw 是一个开源利器，为模型提供“双手”，而 Claude Code 是一个专注于软件开发的基于终端的工具，帮助开发者编写、调试和重构代码。这两个工具也可以结合使用——OpenClaw 可以触发 Claude Code 任务并协调工作流程。

对于纯硬核技术研究/编码任务，**Claude Code** 通常是主要工具，而 OpenClaw 适用于编排和跨会话的持久内存。

---

## 关键模式：Git Worktrees + 多个会话

你描述的生产模式是 **git worktrees** + 并行 Claude Code 会话：

Git worktrees 通过让你并行运行多个 Claude Code 会话来解决上下文切换问题，每个会话都有自己的隔离上下文——不再丢失势头。

具体针对像 AlphaGo 重新实现这样的硬核 ML 研究项目：

```bash
# 为每种方法创建隔离的 worktree 分支
git worktree add ../alphago-mcts-approach    -b approach/mcts-classic
git worktree add ../alphago-policy-net       -b approach/separate-nets
git worktree add ../alphago-transformer-mod  -b approach/transformer-variant

# 在每个中启动 Claude Code 会话
cd ../alphago-mcts-approach    && claude
cd ../alphago-policy-net       && claude --model sonnet
cd ../alphago-transformer-mod  && claude --model opus
```

Claude Code 正式支持 worktrees——子代理可以使用 worktree 隔离并行工作而不会冲突。每个子代理都有自己的 worktree，当子代理完成且无更改时会自动清理。

---

## 每个会话使用不同模型

这是明确支持且推荐的：

每个子代理可以有自己的模型、上下文窗口、内存、工具和思考级别。你可以将 Claude Opus 4 分配给编码代理，将 Claude Sonnet 4 分配给研究代理——仅在真正值得的地方支付高级费用。

对于硬核 ML 研究，一个好的拆分可能是：
- **Opus** → 架构设计、复杂推理、新颖算法设计
- **Sonnet** → 实现、重构、编写测试、更简单的子任务
- **通过 `--base-url` 的其他模型** → 你甚至可以路由到 Gemini 或 GPT-4 进行比较

使用 `--base-url` 通过自定义 API 端点路由请求，使任何 OpenAI 兼容模型都能驱动 Claude Code——解锁完整的代理循环（持久会话、工具使用、多轮交互）与任何模型后端。

---

## 协调多个会话

Agent Teams 使多个 Claude 实例能够并行处理不同子任务，同时通过 git 系统协调。一个会话充当团队领导，分解任务并综合队友的发现。

针对研究问题的真实世界模式：

1. **领导/架构师会话 (Opus)：** 将问题分解为子任务，编写共享的 `TASKS.md` 文件，设置接口
2. **实现会话 (Sonnet)：** 每个拾取一个任务，在自己的 worktree 中工作
3. **审查/合并会话：** 使用 `git diff` 比较实现，合并最佳的一个

一个有文档记录的工作流程涉及架构师代理迭代计划，然后由新的 Claude Code 实例审查并实现。另一种模式是“派出侦察兵”——给代理一个真正困难的任务，对大型代码库无意落地其代码，只是获取它修改哪些文件以及如何处理问题的想法。

---

## 需要了解的关键陷阱

**1. 长会话中的上下文漂移**

同一个代理在对话不同点被问相同问题时，可能采取不同方法。会话早期，新鲜的上下文窗口，它读取现有文件并遵循既定模式。会话晚期，上下文饱和时，它从训练数据构建而不是你的约定。→ 对于长研究任务，**优先使用新鲜会话** 而非非常长的会话。

**2. 磁盘空间**

Cursor 论坛用户报告，在一个 20 分钟会话中处理 ~2GB 代码库时，自动 worktree 创建使用了 9.82 GB。构建产物会更糟。→ 将 ML 模型检查点和大.dataset 放在 worktree 路径之外。

**3. 无共享数据库状态**

Worktrees 共享 `.git` 对象数据库，但不共享运行时状态如数据库或 GPU 内存。对于 AlphaGo 训练，每个 worktree 代理需要自己的检查点目录。

---

## ML 研究问题的实际设置

```bash
# 1. 创建共享父仓库
mkdir alphago-research && cd alphago-research && git init

# 2. 使用 Opus 会话搭建项目
claude --model claude-opus-4-6
> "为重新实现 AlphaGo Zero 设计仓库结构。
> 创建 TASKS.md 将工作分解为：MCTS 引擎、
> policy/value 网络、自对弈循环、训练循环。"

# 3. 为每个组件生成并行 worktrees
git worktree add ../alphago-mcts    -b component/mcts
git worktree add ../alphago-network -b component/network
git worktree add ../alphago-selfplay -b component/selfplay

# 4. 并行运行代理（例如使用 tmux）
tmux new-session -d -s mcts "cd ../alphago-mcts && claude"
tmux new-session -d -s net  "cd ../alphago-network && claude --model sonnet"
tmux new-session -d -s play "cd ../alphago-selfplay && claude"

# 5. 每个完成后，比较并合并最佳
git diff component/mcts main
git merge component/network
```

---

## 总结

是的，这是一个真实且强大的工作流程。完整栈看起来像：

- **Claude Code** 用于隔离 worktrees 中的单个编码会话
- **Git worktrees** 用于每个方法/组件的临时仓库目录
- **不同模型**（Opus 用于硬推理，Sonnet 用于实现）
- **OpenClaw** 可选叠加，用于持久内存、编排和跨会话的长时间协调
- **领导/架构师代理** 编写共享任务文件，让子代理协调而不冲突

该工作流程已在 incident.io 等公司经过实战检验，并现已被 Claude Code 官方文档支持。

---

**参考文献：**

- [Claude Code Parallel Worktrees Skill](https://github.com/spillwavesolutions/parallel-worktrees)
- [Mastering Git Worktrees with Claude Code](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)
- [Embracing the Parallel Coding Agent Lifestyle – Simon Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)
- [incident.io: Shipping faster with Claude Code and Git Worktrees](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)
- [Claude Code Agent Teams Workflow Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md)
- [Claude Code Common Workflows – Official Docs](https://code.claude.com/docs/en/common-workflows)
- [openclaw-claude-code-skill (multi-model routing)](https://github.com/Enderfga/openclaw-claude-code-skill)
- [Designing the Multi-Agent Development Environment](https://alexlavaee.me/blog/parallel-agent-sessions-infrastructure-gap/)
