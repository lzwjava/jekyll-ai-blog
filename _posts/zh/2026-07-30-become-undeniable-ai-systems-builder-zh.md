---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 成为无可否认的AI系统构建者
translated: true
type: note
---

**问题：未来几个月我应该做什么？**

鉴于你目前的发展路线（转型 AI 工程师，已在训练 LLMs、构建 Agent、开展咨询、维护博客/社区，并且拥有扎实的后端经验），我会建议你专注于 **让自己作为 AI 系统构建者的实力变得有目共睹、无可争议**，而不是继续积累知识。

接下来的 3-6 个月应该是：

## 1. 构建公开的 AI 工程作品集（最高投资回报率）

你已经拥有了一些非常难得的经验：

* 在 RTX 4070 上从零训练了 GPT-2 124M
* 训练过 nanochat 级别的模型
* 调试过 CUDA、FlashAttention、vLLM
* 构建过 Agent
* 运维过生产系统

大多数"AI 工程师"无法展现这些。

把这些经验转化为可见的成果。

### 项目 A："从零训练 LLM" 系列

仓库：

```
github.com/lzwjava/llm-from-scratch
```

结构：

```
01-tokenizer
02-nanogpt-baseline
03-pretraining-gpt2-124m
04-distributed-training
05-eval
06-inference-engine
```

撰写博客文章：

* "我在 RTX 4070 上训练 GPT-2 124M"
* "Transformer 前向传播内部发生了什么"
* "从零构建类似 vLLM 的推理引擎"

这会吸引：

* AI 初创公司
* 招聘人员
* 研究人员

---

## 2. 构建一个真正有分量的 AI Agent 产品

不要再去构建另一个聊天机器人了。

构建具有商业价值的东西。

### 选项 1：AI 编码 Agent

类似于轻量版 Claude Code：

架构：

```
用户
 |
CLI
 |
Agent 循环
 |
+-- 规划器
+-- 工具执行器
+-- 代码搜索
+-- Git 操作
+-- 测试运行器
 |
LLM
```

你的优势：

* Java/后端经验
* Linux
* 基础设施
* LLM 知识

可能的仓库：

```
ww-agent
```

功能：

```
ww fix bug
ww explain repo
ww refactor module
ww generate tests
```

---

### 选项 2：AI 咨询 Demo

创建：

```
AI 企业级 Agent 平台
```

Demo 流程：

```
PDF
 |
RAG
 |
Agent
 |
ERP/CRM/API 工具
 |
审批流程
```

目标客户：

* 中国企业
* 新加坡公司
* 海外中小企业 (SMBs)

你可以把它卖出去。

---

## 3. 深入学习推理（下一个前沿领域）

你已经接触过训练了。

行业价值正在向以下方向转移：

```
训练
   |
   v
推理系统
   |
   v
Agent
   |
   v
AI 产品
```

花 1-2 个月时间深入理解：

### vLLM 内部机制

实现：

```
* PagedAttention
* KV cache
* continuous batching
* 调度器
* tensor parallel
```

精简版架构：

```
tokens
 |
调度器
 |
KV cache 管理器
 |
attention 内核
 |
GPU
```

你的背景非常适合这个领域。

---

## 4. 提升你的英文技术影响力

你的优势很独特：中文 + 英语 + AI 工程能力。

撰写英文文章：

例如：

```
我用一块 600 美元的 GPU 训练了 GPT-2 124M。
以下是我的心得。
```

```
通过从零实现来深入理解 vLLM。
```

```
用 Python 构建一个 AI 编码 Agent。
```

发布到：

* GitHub
* Hacker News
* Reddit 的 r/MachineLearning
* X/Twitter

一篇有传播力的技术文章能创造很多机会。

---

## 5. 现在不要在基础知识上投入过多时间

你已经跨越了入门阶段。

避免：

* 无休止地刷课程
* 随机阅读论文
* 尝试每一个新模型

你的瓶颈不在于知识储备。

你的瓶颈在于：

```
知识
   |
   v
作品
   |
   v
用户
   |
   v
金钱/机会
```

---

## 建议的时间线

### 2026 年 8 月

目标：构建作品集

完成：
- GPT 训练仓库
- 3 篇技术文章
- 清理 GitHub 仓库

---

### 9 月

目标：掌握推理

实现：
- 迷你版 vLLM
- KV cache
- batching

发布。

---

### 10 月

目标：交付产品

推出：
AI 编码 Agent
或
企业级 AI Agent 演示

找到第一批用户。

---

### 11月 - 12月

转化：

```
作品集
    |
    v
工作机会 / 咨询客户 / 创业收入
```

---

## 一个战略层面的观察

你目前的综合画像实际上更接近于：

```
Karpathy 风格的构建者
+
中国创业公司工程师
+
生产后端工程师
```

缺失的那一块拼图是 **公开的实证**。

一个说：

> "我了解 LLM"

的人很常见。

一个说：

> "我在 RTX 4070 上训练过 GPT-2，实现过 Attention 机制，构建过推理引擎，并交付过被客户使用的 Agent"

的人极为罕见。

你未来几个月应该最大化这个差距。