---
audio: false
generated: true
image: false
lang: en
layout: post
title: "TongDaXin: China's Bloomberg Terminal"
translated: false
type: note
---

**Question:** What is <https://www.tdx.com.cn>?

**Answer:**

It's **通达信 (TongDaXin)** — one of China's most dominant stock market analysis and trading software platforms, built by **深圳市财富趋势科技股份有限公司 (Shenzhen CaiFu QuShi Technology Co., Ltd.)**.

Think of it as the Bloomberg Terminal equivalent for Chinese retail and institutional investors, but far more mass-market. It's been the de facto standard for Chinese A-share trading software for decades.

**What they offer:**

- **Broker systems** — white-label trading terminals that most Chinese brokerages (券商) use as their underlying platform
- **Personal editions** — tiered from free basic to paid Professional/Research versions, covering A-shares, HK stocks, US stocks, and futures
- **Market data** — real-time quotes, historical tick data, full order book; their data format (`.dat` files) is widely used in Chinese quant circles
- **Research terminal** — institutional-grade tool, including a bond terminal
- **AI platform** — they've recently added: `问小达AI` (their own LLM-based Q&A), an agent marketplace, and notably **通达信MCP** (an MCP server for financial data) and **TdxClaw** — which is interesting given you build CLI agents

**Why it's relevant to you specifically:**

The `TdxClaw` and `通达信MCP` products suggest they're building MCP-compatible financial data APIs — meaning you could potentially connect Claude or your own agents to real-time Chinese market data via MCP. Given you already build tools like `iclaw` and `zz`, this is worth a look if you ever want to build a Chinese equity research agent.

Also their historical data format (`通达信数据`) is well-documented and widely used in Chinese open-source quant projects — worth knowing if you ever touch A-share data pipelines.
