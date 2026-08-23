---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Salesforce Agentforce AI 平台
translated: true
type: note
---

**问题：** 什么是 Salesforce Agentforce 平台？

**回答：**

## 什么是 Agentforce？

Salesforce Agentforce 是一个直接构建在 Salesforce 内部的 AI 平台。它允许你创建能够自主完成整个任务的 AI 代理——而不仅仅是回答问题。这是 Agentforce 与聊天机器人等旧工具的主要区别：聊天机器人回答一个问题后便停止。

Salesforce 于 2024 年首次推出 Agentforce。到 2026 年，它已成为整个 Salesforce 产品线的核心——Sales Cloud、Service Cloud 和 Marketing Cloud 都已围绕它重建。换句话说，Agentforce 之所以重要，是因为 Salesforce 已从一个你登录的系统，转变为一个能够代表你行动的系统。

---

## 工作原理——核心架构

Agentforce 基于 **Atlas Reasoning Engine** 进行规划，并依赖 **Data Cloud** 提供数据基础。**Trust Layer** 位于底层，对每个代理操作应用数据脱敏、审计日志记录以及毒性和偏见检测——这是 Salesforce 对每个企业在让代理接触生产数据之前都会提出的治理问题的回答。

代理使用 **Reason–Act–Observe 循环** 进行类人决策，提供实时的统一客户数据上下文，并内置安全性、合规性和数据脱敏功能。

该平台包含 4 个关键层：

| 层 | 角色 |
|---|---|
| **Atlas 推理引擎** | AI 规划与决策 |
| **Data 360**（原 Data Cloud） | 统一客户数据基础 |
| **信任层** | 治理、审计日志、数据脱敏 |
| **Agent Builder** | 低代码/无代码代理创建 |

---

## 主要功能

该平台包括：用于创建 AI 驱动体验的对话式代理构建器；结合确定性业务逻辑与 AI 推理的混合推理；支持自然代理交互的语音功能；用于监控和故障排除的内置可观测性；以及继承自 Salesforce 平台的企业级安全性。

Agentforce 360（最新主要版本）将虚拟代理嵌入整个生态系统——包括 Slack，后者已成为与 AI 代理和客户数据交互的主要工作空间。用户可以直接通过聊天查询客户数据或完成 Salesforce 任务，并具备企业级的隐私和治理控制。

---

## 最佳适用场景

- **客户服务**——自主解决支持案例
- **销售自动化**——潜在客户管理、机会更新
- **市场营销**——活动简报、受众细分
- **人力资源与 IT 运营**——面向内部员工的工作流程

所有代理都使用同一数据源，帮助它们主动理解客户的完整历史——将来自语音对话、聊天、短信、过往购买和营销活动的洞察融入每一次交互。

---

## 规模与采用

已有超过 12,000 名客户部署了代理，Agentforce 现在被认为是使用 Salesforce 的现代企业的必备工具。Gartner 在 2026 年对话式 AI 平台魔力象限中将 Salesforce 评为领导者。

---

**参考文献：**
- [What Is Salesforce Agentforce? 2026 Guide – Cynoteck](https://www.cynoteck.com/blog-post/salesforce-agentforce-complete-guide)
- [Salesforce Agentforce: Architecture, Pricing & MCP – Atlan](https://atlan.com/know/ai-agent/ai-agent-applications/what-is-salesforce-agentforce/)
- [Agentforce Official Site – Salesforce](https://www.salesforce.com/agentforce/)
- [Agentforce 360 at Dreamforce 2026 – XFilesProSF](https://www.xfilespro.com/agentforce-360-at-dreamforce-2026-everything-you-should-know/)
- [Salesforce Agentforce Guide 2026 – CompanyBench](https://companybench.com/blog/salesforce-agentforce-guide-2026)