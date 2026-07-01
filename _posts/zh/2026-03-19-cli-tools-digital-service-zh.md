---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 每个数字服务的 CLI 工具
translated: true
type: note
---

Question: 针对 DBS Bank、SCB Bank、OpenRouter、Pinduoduo、Temu、Amazon、RedNote 等服务的 CLI 工具的可能性和想法有哪些？

Answer:

这是一个迷人的愿景——本质上是 **"everything as a CLI"**，更重要的是 **"everything as an agent-controllable interface"**。让我来分解一下。

---

## 核心理念：CLI 优先的一切

真正的价值不仅仅是为人类提供 CLI——而是**让每个服务都可编程且可被 agent 访问**。Claude Code（或任何 AI agent）就可以协调所有这些服务。

---

## 类别分解

### 🏦 银行 CLI（DBS、SCB 等）

```bash
dbs balance --account savings
dbs transfer --to "John" --amount 500 --currency SGD
dbs history --last 30days --export csv
scb fx-rate --from THB --to USD
scb pay --bill electricity --amount auto
```

**当前可能实现的内容：**

- DBS 和 SCB 都有开发者 API（PayLah、RAPID API）
- Open Banking 法规（新加坡 MAS、泰国 BoT）正在推动这一点
- Claude Code 可以自动支付账单、异常警报、重新平衡储蓄

**挑战：** 认证（2FA、MFA）、合规性、安全沙箱

---

### 🛒 电商 CLI（Amazon、Temu、Pinduoduo）

```bash
amazon search "mechanical keyboard" --max-price 100 --prime-only
amazon buy --asin B08N5KWB9H --quantity 1
temu cart --add [item-id] --coupon auto-best
pinduoduo group-buy --join cheapest --category electronics
```

**当前可能实现的内容：**

- Amazon 有 Product Advertising API
- Temu/Pinduoduo 目前还没有官方公共 API
- 可以通过浏览器自动化（Playwright + Claude）构建

**Agent 用例：** Claude 监控价格、在达到阈值时购买、跟踪交付

---

### 🤖 AI/开发 CLI（OpenRouter）

```bash
openrouter models --list --filter cost<0.01
openrouter run --model deepseek/v3 --prompt "summarize this"
openrouter benchmark --models gpt4o,claude,gemini --task coding
openrouter spend --this-month --breakdown-by-model
```

**当前可能实现的内容：**

- OpenRouter 已经有 REST API——CLI 包装器非常容易构建
- 这是**最容易立即实现**的类别
- Claude Code 可以根据任务类型自动选择最便宜的 model

---

### 📱 社交/内容 CLI（RedNote / 小红书）

```bash
rednote search "Tokyo travel" --top 10
rednote post --image ./photo.jpg --caption "..." --tags travel,japan
rednote analytics --my-posts --last 7days
rednote trending --category food --region shanghai
```

**挑战：** 没有官方 API，需要逆向工程或非官方访问

---

## 更宏大的愿景：Agent 协调层

真正的力量体现在 Claude Code 连接**所有这些**服务时：

```
“Claude，我的 DBS 账户余额超过 5000 SGD。
在 Amazon 或 Temu 上给我买最便宜的 iPhone 16，
在 RedNote 上发布开箱计划，
并使用 OpenRouter 上最便宜的 AI model 来写 caption。”
```

Claude Code 将：

1. `dbs balance` → 确认资金 ✅
2. `amazon search` + `temu search` → 比较价格
3. `amazon buy` → 购买
4. `openrouter run deepseek` → 生成 caption（最便宜的 model）
5. `rednote post` → 调度发布

---

## 为什么这很重要

## 实现这一愿景所需条件

| Today | Future Vision |
| --- | --- |
| Click through 5 apps | One Claude prompt |
| Manual price comparison | Auto-agent monitors 24/7 |
| Copy-paste between services | Seamless pipeline |
| Human triggers everything | Event-driven automation |

---

## 实现这一愿景所需条件

1. **官方 API**——银行和社交平台需要开放
2. **认证标准**——OAuth、passkeys 用于 agent 安全的登录
3. **MCP servers**——Claude Code 的 Model Context Protocol 可以包装任何 API
4. **Agent 权限模型**——“允许 Claude 每月花费高达 200 美元”

---

## MCP 视角（已在发生）

Claude Code 的 **MCP (Model Context Protocol)** 正是为此提供的基础设施。任何人可以为以下构建 MCP server：

- DBS → `dbs-mcp-server`
- Amazon → `amazon-mcp-server`
- OpenRouter → `openrouter-mcp-server`

Claude Code 将原生协调它们所有——**这个未来比大多数人想象的更近。**
