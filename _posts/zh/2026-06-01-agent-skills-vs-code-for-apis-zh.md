---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理技能与API代码对比
translated: true
type: note
---

**问题：** 与其为 AMD Dev Cloud / DigitalOcean API 调用编写固定的包装代码（如 `snapshots.py`），我们是否应该直接给智能体（Hermes/Claude Code）API 令牌，让它动态决定如何操作？通用原则是：智能体用于灵活/探索性任务，代码用于固定/复杂任务？

**回答：**

是的，完全正确。这是现代 AI 工程中的核心判断之一。让我明确一下框架：

## 原则：技能 vs. 无技能

```
固定 + 复杂  →  编写代码（技能）
灵活 + 简单  →  给智能体令牌（无需技能）
```

你的 `snapshots.py` 是**过度工程化一个智能体可以轻松处理的任务**的完美例子。DigitalOcean API 文档完善，Claude Code / Hermes 非常熟悉它，快照操作本质上是探索性的（“显示正在运行的内容”、“创建一个”、“删除旧的”）。

## 智能体优先的做法

与其用 `snapshots.py`，不如：

```bash
export DIGITALOCEAN_TOKEN=xxx

claude "列出我所有的 droplet 及其快照。删除 amd-dev droplet 上超过 7 天的任何快照。"
```

或者通过兼容 OpenAI 的端点使用 Hermes：

```python
system = """
您有权访问 DigitalOcean API v2。
基础 URL：https://api.digitalocean.com/v2
认证头：Authorization: Bearer {token}

使用 HTTP 工具调用来完成任务。要精确，删除前请确认。
"""
```

智能体读取它训练时学到的 DO API 文档，构造正确的 `GET /v2/droplets`、`GET /v2/droplets/{id}/snapshots`、`DELETE /v2/snapshots/{id}` 调用——无需包装器。

## 何时编写代码（真正的阈值）

| 情况 | 智能体还是代码？ |
|---|---|
| “列出快照，删除旧的” | 智能体 |
| “SSH 隧道 + 端口转发到 droplet” | 智能体（可能） |
| “启动 droplet，等待 cloud-init，运行基准测试，创建快照，销毁”——可靠地在 CI 中运行 | **代码** |
| 带有退避的复杂重试逻辑 + 状态机 | **代码** |
| 每天运行 100 次的多步骤工作流 | **代码** |
| 一次性探索 / 运维任务 | 智能体 |

阈值是：**这里的 bug 会让你损失金钱或数据吗？** 在错误的 droplet 上删除快照 = 糟糕。对此，你需要幂等的、经过审查的代码，并带有 `--dry-run` 选项。对于“我有哪些快照？”——直接问智能体就行。

## 更深层的洞察：智能体缩小了技能差距

`snapshots.py` 真正编码的是**你过去学习 DO API 的努力**——分页、认证头、错误处理。智能体已经拥有这些知识。因此，除非符合以下情况，否则包装器是负 ROI：

1. 你需要**确定性行为**（相同的动作，相同的结果，每次一致）
2. 你需要**可组合性**（这个脚本被另一个脚本调用）
3. 该 API 是**晦涩/未记录的**（智能体不太了解）
4. 你需要**速度**（智能体往返会增加延迟）

具体到 AMD Dev Cloud —— DigitalOcean API 非常知名，Claude Code 原生支持它，所以 `ww/amd_dev_cloud/` 中几乎所有内容都可以删除，转而使用 `claude "在我的 droplet 上执行 X"`。

## 实际应该保留为代码的内容

从你的 `ww` 仓库中，值得保留为脚本的内容有：

- **GPU 基准测试框架**——复杂，需要精确的可重复性
- **训练任务提交**——状态机、重试逻辑、成本控制
- **SSH 隧道设置**——繁琐，你每天运行 10 次，肌肉记忆
- **数据集流水线**——确定性转换、版本控制

所有只是“调用此 API 并显示结果”的内容 → 删除，让智能体来做。

## 实际设置

```bash
# ~/.zshrc 或 ww 配置
export DIGITALOCEAN_TOKEN=$(cat ~/.secrets/do_token)

# 一个别名搞定一切
alias amd='claude --system "你通过 DigitalOcean API 管理我的 AMD Dev Cloud droplet。令牌在环境变量 DIGITALOCEAN_TOKEN 中。破坏性操作前务必确认。"'

# 用法
amd "我有哪些快照？"
amd "立即为 droplet amd-mi300x 创建快照"
amd "我的 droplet 是 192.168.1.x，当前状态是什么？"
```

这确实比 `snapshots.py` 更强大，因为智能体可以串行操作、处理错误并自适应——你的固定包装器如果不写更多代码是无法做到的。

**核心观点：** 正确的问题不是“我应该编写这个脚本吗？”，而是“这个任务值得固化为代码，还是应该保持在智能体空间中的流动状态？”大多数运维任务属于智能体空间。只有当它们通过重复性和可靠性要求赢得资格时，才将它们升级为代码。