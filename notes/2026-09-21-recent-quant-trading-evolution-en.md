---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recent Quant Trading Evolution
translated: false
type: note
---

**Question:** How do people do quant trading in recent years? Have firms like Jane Street and Citadel improved their methods?

**Answer:**

Yes, significantly. The last few years have been a landmark period for quantitative trading, both in scale and methodology. Here's a breakdown:

---

### 📈 Scale & Dominance

Algorithmic and high-frequency strategies now account for nearly 65% of US equity trading volume as of 2024, up from about 45% in 2010. The leading firms have grown almost incomprehensibly large:

- Jane Street generated a record $20.5 billion in net trading revenue in 2024 — more than Bank of America or Citigroup — with net income of $13 billion from roughly 3,000 employees. Citadel Securities posted $9.7 billion, a 55% increase.
- In 2025, Jane Street reached $39.6 billion in net trading revenue, and Hudson River Trading (HRT) hit approximately $12.3 billion.

---

### 🏦 How Jane Street Actually Makes Money

Jane Street's dominant edge is in **ETF market-making**. In 2024, Jane Street averaged $707 billion in monthly ETF trading volumes, taking 24% of the US primary market and 16% of the secondary market in US-listed funds, and 17% of secondary market activity in Europe. They also made up 8% of all OCC options volumes.

A major recent driver: the launch of spot Bitcoin ETFs in the US in early 2024 created enormous new markets requiring sophisticated market makers, and Jane Street positioned itself as an authorised participant for products from BlackRock and others — capturing arbitrage every time ETF prices deviate from net asset value.

---

### 🤖 Methodological Improvements: AI & ML

This is where the biggest evolution is happening:

**1. LLMs for Alpha Discovery**
Prompt-based LLMs are now being used to automate the alpha generation process — taking in specific financial prompts and generating formulaic signals aligned with desired prediction tasks. This combines domain-specific financial knowledge with the generative power of language models.

**2. Reinforcement Learning (RL) for Execution & Portfolio Optimization**
Reinforcement learning, predictive modeling, and execution algorithms are driving measurable improvements in portfolio execution efficiency. Adaptive AI frameworks — such as agent-based models and meta-learning systems — are shaping autonomous trading in complex, dynamic environments.

**3. Multi-Agent LLM Systems**
Recent research has produced frameworks where multiple AI agents collaborate: one reads news/filings, one generates signals, one manages risk — all coordinated in real-time. Systems like TradingAgents and FLAG-Trader (RL + LLM fusion) represent this frontier.

---

### 🏎️ Firm-by-Firm Specialization

Firms tend to specialize: HRT, Tower, Jump, and Citadel Securities lean heavily on C++ systems and ultra-low latency infrastructure; Jane Street, Optiver, SIG, and IMC favor probability theory and trading judgment; XTX, Two Sigma, AQR, and WorldQuant are most research/ML-focused.

---

### ⚠️ The Arms Race Problem

The core challenge for quant firms is **alpha decay** — as more capital chases the same signals, edges erode. The response has been to push into:

- More exotic asset classes (crypto, fixed income ETFs, emerging markets)
- Faster execution (custom silicon, co-location)
- Better alternative data (satellite imagery, credit card flows, NLP on earnings calls)
- AI-driven alpha discovery to find signals humans wouldn't think to look for

Jane Street has even signed chip startup Etched as a customer for custom AI inference chips, signaling how seriously the top firms are investing in specialized hardware for their models.

---

**References:**

- [What Is Quant Trading? A Complete 2026 Guide - Tradermath](https://www.tradermath.org/articles/what-is-quant-trading)
- [Top HFT and Prop Trading Firms in 2026 - QuantInsti](https://www.quantinsti.com/articles/hft-prop-trading-firms/)
- [Jane Street took 10% of US equity market in 2024 - Global Trading](https://www.globaltrading.net/?p=38181)
- [Adaptive Alpha Weighting with PPO - arXiv](https://arxiv.org/html/2509.01393)
- [Jane Street Institutional Services](https://www.janestreet.com/institutional-services/)
