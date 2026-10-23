---
audio: false
generated: true
image: false
lang: en
layout: post
title: China's AI Agent and Automation Ecosystem
translated: false
type: note
---

**Question:** What's the AI agent and workflow automation ecosystem like in China specifically — tools, platforms, players?

**Answer:**

China's market is structurally different from the global market. Three super-ecosystems dominate, government is a tailwind, and the tooling is increasingly homegrown. Here's the full picture.

---

## The Big Picture

The enterprise AI agent solutions market in China is projected to grow from ¥5.6 billion in 2024 to ¥59.1 billion in 2029 — a 60.2% CAGR — moving from proof-of-concept to commercial realization. And China's Five-Year Plan specifically calls for deploying AI agents across manufacturing, logistics, education, and healthcare as core infrastructure — meaning government contracts and SOE procurement are a real channel, not just private enterprise.

The domestic agent industry in H2 2026 is at the critical juncture of moving from validation to scale.

---

## Layer 1 — Foundation Models (What Agents Are Built On)

China has strong domestic options, which matters because data sovereignty and censorship compliance rules out using OpenAI/Claude directly for most enterprise clients.

| Model | Company | Notes |
| --- | --- | --- |
| **DeepSeek V3 / R1** | DeepSeek | Open source, cheapest, best price/perf, huge developer adoption |
| **Qwen3** | Alibaba | Strong, integrates natively with DingTalk/Alibaba Cloud |
| **ERNIE 4.0** | Baidu | Largest user base (200M+), Qianfan enterprise platform |
| **Doubao** | ByteDance | Powers Coze, integrated into Feishu |
| **GLM-4** | Zhipu AI (Tsinghua) | Strong in multi-agent coordination |
| **Kimi** | Moonshot AI | Long context, popular with developers |

**Practical pick:** Most developers in China today default to **DeepSeek** for cost + performance, with **Qwen** as the second choice for enterprise DingTalk integration.

---

## Layer 2 — Agent Building Platforms

### 🟦 Coze (扣子) — ByteDance

Coze runs as `coze.com` internationally and `coze.cn` for the China market (separated). It's a low-barrier bot/agent builder with drag-and-drop interface, templates you can use immediately, and a "Coze 2.5 Agent World" ecosystem launched in April 2026. Best for: quick prototypes, customer-facing bots, non-technical users. Deep integration with Douyin and Feishu.

### 🟩 Dify — Open Source

The developer favorite. Dify keeps continuously updating its RAG and workflow editors in 2026 and can be self-hosted on your own servers — critical for enterprise clients worried about data leaving their environment. Supports DeepSeek, Qwen, and any OpenAI-compatible API. Best for: technical teams, RAG systems, custom agentic workflows.

### 🟧 Baidu AgentBuilder — Baidu Ecosystem

Baidu's AgentBuilder offers zero-code and low-code modes for agent development and deployment, offering developers a distribution path through Baidu's ecosystem matrix. It has served over 160,000 developers and 50,000+ enterprises, covering 100+ application scenarios. Best for: reaching Baidu's massive user base through Baidu Search and ERNIE Bot.

### 🟪 QwenWork — Alibaba/DingTalk

In August 2026, QwenWork integrates directly with DingTalk, equipping sales, reception, marketing, and compliance with specialized agents. Best for: enterprise clients already on Alibaba Cloud and DingTalk.

---

## Layer 3 — RPA + AI (The "Hands" of Enterprise Automation)

This is where the money is for traditional enterprise. These tools do what LLMs alone can't: click buttons, fill forms, operate legacy software, scrape screens.

### 来也科技 (Laiye) — Market Leader

Recognized in the 2026 Gartner Magic Quadrant for Robotic Process Automation for six consecutive years — the only Chinese company on it. Laiye has built an enterprise-grade agent platform that calls enterprise-grade skills to get work done, with any third-party agent able to call Laiye skills directly. Clients include China Mobile, China Southern Power Grid, major insurers. This is the UiPath equivalent for China.

### 影刀 (Yingdao) — Developer-Friendly RPA

Popular among smaller businesses, easier to learn than Laiye, strong in e-commerce automation (Taobao, JD.com workflows). Lower cost.

### 实在智能 (Shizai Intelligence)

Positioned as "full-stack AI + automation" with core technology called ISSUT (screen semantic understanding), emphasizing "what you see is what you get" and zero-code development. Bypasses the need for API integrations by understanding screens visually — useful for legacy systems with no APIs.

### 艺赛旗 (IS-RPA)

Deeply embedded in finance and accounting verticals, with emphasis on process mining and efficiency analysis.

---

## Layer 4 — Enterprise Communication Platforms (The Distribution Channels)

This is unique to China. Your agent needs to live *inside* these platforms to reach workers:

| Platform | Owner | Users | Notes |
| --- | --- | --- | --- |
| **DingTalk (钉钉)** | Alibaba | 700M+ | Dominant in enterprise, especially SMEs and manufacturing |
| **WeChat Work (企业微信)** | Tencent | 180M+ | Banks, real estate, retail |
| **Feishu (飞书/Lark)** | ByteDance | Growing fast | Tech companies, startups |

If you build an agent that doesn't integrate with at least one of these, enterprise clients won't buy it. The workflow lives in the chat app.

---

## Layer 5 — The Three Ecosystems That Control Everything

Tencent's WorkBuddy, Alibaba, and ByteDance generated approximately 56.5 million of 60.6 million total measured office agent visits in June 2026 — about 93% of total traffic. The race is shifting from launching standalone products to controlling the primary entry point for AI-enabled work.

This means:

- **ByteDance** → Coze + Doubao + Feishu
- **Alibaba** → Qwen + DingTalk + Alibaba Cloud
- **Tencent** → WorkBuddy + WeChat Work + Tencent Cloud

As a solo builder, you're not competing with them — you're **building on top of them**.

---

## Practical Stack for a Solo Developer in China

```
LLM:          DeepSeek V3 (cheapest, best) or Qwen3
Agent builder: Dify (self-hosted for enterprise) or Coze (fast prototype)
RPA layer:    Yingdao or Laiye (if budget allows)
Distribution: DingTalk bot or WeCom integration
Hosting:      Alibaba Cloud / Tencent Cloud (domestic ICP compliance)
Vector DB:    Milvus (open source, Chinese origin) or pgvector
```

---

## The Opportunity Gap for a Solo Engineer

The three giants own the platforms but **don't own the vertical implementations**. The gap is:

- A **manufacturing SME in Guangdong** needs their invoices and QC reports automated — Alibaba won't fly down to configure that
- A **real estate agency** needs WeChat lead follow-up automated with their CRM
- A **logistics company** needs DingTalk approval workflows connected to their WMS

The giants sell platforms. **You sell working solutions for a specific industry.** That's the gap — and in China, with thousands of mid-size manufacturers, logistics firms, and service companies still running manual processes, it's a large gap.
