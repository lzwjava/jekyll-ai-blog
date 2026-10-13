---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数十亿Token背后的真实工作负载
translated: true
type: note
---

问题：人们如何每天/每周消耗 1B 或 5B 个 LLM token？这些数字背后的真实工作负载是什么？

答案：

关键点：**没有人能手动输入足够多的聊天消息来达到数十亿个 token。** 巨大的 token 消耗量来自**自动化、agent、产品和 pipeline**。

1B token/天听起来很惊人，但实际上是可以达到的：

- 1B token/天 ≈ 11,500 token/秒，持续运行
- 5B token/周 ≈ 平均 8,300 token/秒

单次人类对话的 token 消耗量非常小：

- 普通 ChatGPT 对话：约 5k–50k token
- 长时间编码会话：约 100k–1M token
- Agent 编码任务：可能达到数百万 token，因为它会循环执行、读取文件、运行工具、重试、推理等。[arXiv](https://arxiv.org/abs/2604.22750?utm_source=chatgpt.com)

因此，关键在于**很多机器并行工作**。

---

## 1. AI 编码 agent

示例：

一家公司有这样的规模：

- 10,000 名开发者
- 每位开发者每天使用 agent 2 小时
- 每个 agent 每小时消耗 100k token

计算：

```
10,000 名开发者
× 2 小时
× 100k token/小时

= 20 亿 token/天
```

Agent 不只是简单回答：

```
用户：
“修复这个 bug”

Agent：
- 读取代码仓库
- 读取文档
- 搜索代码
- 生成计划
- 修改文件
- 运行测试
- 发现错误
- 再次修复
- 审查 diff
```

每一轮循环都会消耗大量 token。

Agent 工作流比普通聊天消耗的 token 多得多，因为它们会反复与工具和上下文交互。[arXiv](https://arxiv.org/abs/2604.22750?utm_source=chatgpt.com)

---

## 2. 面向客户的 AI 产品

想象一家 AI 客服公司：

```
1000 万用户
× 每天 20 次对话
× 每次对话 5,000 token

= 1 万亿 token/天
```

示例：

- AI 搜索引擎
- AI 导师
- AI 翻译工具
- AI 陪伴产品
- AI 购物助手
- AI 呼叫中心

用户看到的是：

> 向 AI 提问

但在幕后：

```
查询
 ↓
检索文档
 ↓
总结
 ↓
推理
 ↓
调用工具
 ↓
生成答案
```

许多内部 token 是用户看不见的。

---

## 3. 数据处理 pipeline

公司让模型处理数百万份文档：

```
1000 万份文档
× 每份文档 10,000 token

= 100B token
```

任务：

- 总结合同
- 提取发票信息
- 对邮件分类
- 分析客户反馈
- 迁移旧代码
- 翻译文档

银行可以处理多年积累的：

```
PDF
邮件
工单
日志
源代码
```

通过 LLM 处理。

---

## 4. 全天候运行的自主 agent

这可能是未来最大的 token 消耗场景。

不再是：

```
人类 → AI → 答案
```

而是变成：

```
AI agent
 |
 +-- 读取邮件
 +-- 监控系统
 +-- 撰写报告
 +-- 创建 PR
 +-- 协商 API
 +-- 调研竞争对手
 +-- 更新数据库
```

一家公司可能有：

```
1000 个 agent

每个：
1M token/天

=

1B token/天
```

企业级 AI 使用已经在从简单的聊天转向委派式 agent 工作流。[OpenAI](https://openai.com/signals/enterprise-data/?trk=public_post_comment-text\&utm_source=chatgpt.com)

---

## 5. 训练与评估

实验室也会消耗大量 token：

```
100,000 个 benchmark 任务
× 每个任务 100k token

= 10B token
```

用于：

- 模型评估
- synthetic data 生成
- RL 训练
- red teaming
- prompt 优化

---

## 一个现实的“每周 5B token”初创公司

一家小型 AI 公司可以达到这个量级：

```
20 名工程师使用编码 agent
    ↓
20 × 50M token/周

= 1B token/周


10 个客服 AI agent
    ↓
10 × 300M token/周

= 3B token/周


文档处理
    ↓
1B token/周

总计：
5B token/周
```

这不是科幻小说。大型组织已经报告了超大规模的 AI token 处理量，token 消耗正越来越多地由 agent 驱动，而不仅仅是聊天使用。[McKinsey & Company](https://www.mckinsey.com/capabilities/quantumblack/our-insights/is-that-ai-agent-worth-it-agentic-economics-and-the-modern-operating-model?utm_source=chatgpt.com)

---

## 为什么这对 AI 咨询公司/初创公司很重要

对传统软件公司来说：

```
出售工时
↓
10 名工程师 × 每月 160 小时
```

对 AI 原生公司来说：

```
出售智能
↓
100 个 agent × 每天数百万 token
```

你的“工厂”变成：

```
客户问题
      |
      v
AI agents
      |
      v
token + GPU + 工具
      |
      v
业务产出
```

构建这些系统的公司自然会成为高 token 消耗者。

一个有用的下一步是设计一套**小型 AI 咨询架构，使其能够实际产生 1B token/月，并将这些 token 转化为客户愿意付费的价值**。我可以帮你规划出来。