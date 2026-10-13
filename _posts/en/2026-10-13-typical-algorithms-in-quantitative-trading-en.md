---
audio: false
generated: true
image: false
lang: en
layout: post
title: Typical Algorithms in Quantitative Trading
translated: false
type: note
---

**Question:** What are the typical algorithms used in quantitative trading — such as those used by DeepSeek (High-Flyer Capital), ML-driven funds, and firms like Jane Street?

---

**Answer:**

Quant trading algorithms generally fall into several layers — **alpha generation**, **execution**, and **risk management** — each with its own techniques.

---

## 1. Classic Statistical / Mathematical Strategies

These remain the foundation even at cutting-edge firms:

| Strategy | Core Idea |
|---|---|
| **Mean Reversion** | Prices deviate from equilibrium → trade back to mean (pairs trading, stat-arb) |
| **Momentum / Trend** | Assets trending in one direction → ride the trend |
| **Factor Models** | Fama-French style exposure to risk premia (value, size, quality, etc.) |
| **Statistical Arbitrage** | Cointegrated pairs or baskets → exploit temporary mispricing |
| **Market Making** | Quote bid/ask continuously, profit from the spread with inventory control |

---

## 2. Machine Learning Approaches

This is where modern quant funds (Two Sigma, DE Shaw, High-Flyer/DeepSeek) differentiate:

### Supervised Learning (Alpha Prediction)
- **Tree ensembles**: XGBoost, LightGBM — industry workhorses for cross-sectional alpha; interpretable, handle non-linearity well
- **Linear models with regularization**: LASSO/Ridge for feature selection across hundreds of signals
- **Neural networks (MLP, ResNet)**: Tabular financial data prediction

### Sequence / Time-Series Models
- **LSTM / GRU**: Capture temporal dependencies in price/volume series
- **Transformers (Attention)**: Applied to tick data, order book snapshots, or cross-asset correlation — increasingly popular post-2020

### Reinforcement Learning (Execution & Strategy)
- Train an agent to optimize order execution (minimize market impact) or portfolio rebalancing
- DeepMind-style RL is used by firms like Goldman Sachs and Citadel for optimal execution

### NLP / LLM Signals
- Sentiment from earnings calls, news wires, Reddit/X (formerly Twitter)
- **DeepSeek's parent company High-Flyer (幻方科技)** heavily leverages large language models for alternative data signal extraction — they even built DeepSeek partly to reduce GPU costs for these workloads

---

## 3. High-Frequency Trading (HFT) Algorithms

Used by Virtu, Optiver, IMC — and Jane Street in some product lines:

- **Order Book Modeling**: Predict short-term price direction from Level 2/3 order book dynamics
- **Latency Arbitrage**: Race to be first to arbitrage price discrepancies across venues
- **Fill Probability Models**: ML models predicting if a passive limit order will be filled
- **Queue Position Modeling**: Poisson processes for order arrival / queue dynamics

---

## 4. Jane Street Specifically

Jane Street is less "ML-first" and more **probabilistic reasoning + market microstructure**:

- **Market Making in Options and ETFs**: They dominate ETF arbitrage and options market making globally
- **Kelly Criterion / Bayesian updating**: Size bets based on edge × probability in real-time
- **Systematic discretion**: Quantitative models inform but humans often override in stressed markets
- Their tech stack is famously built in **OCaml** — they value correctness and speed of reasoning over raw ML firepower
- They recruit heavily for **mathematical probability** and **game theory** skills

---

## 5. DeepSeek / High-Flyer Capital's Approach

High-Flyer pioneered deep learning in Chinese A-share markets (~2015 onward):

- **End-to-end deep learning**: Raw OHLCV + order book data → alpha signals directly via neural nets
- **Very large feature sets**: Thousands of technical and alternative data features fed into gradient boosting + neural ensembles
- **GPU clusters**: They built one of China's largest private GPU clusters specifically for model training
- DeepSeek (the LLM lab) was spun out partly to develop efficient AI infrastructure, which cross-pollinates back into trading model development

---

## Quick Comparison

| Firm Type | Primary Approach | Edge |
|---|---|---|
| **Renaissance / Two Sigma** | Statistical patterns + ML ensembles | Data breadth + signal diversity |
| **Jane Street / Optiver** | Market making + probabilistic models | Microstructure expertise |
| **High-Flyer (DeepSeek)** | Deep learning on price/alt data | Neural nets + GPU scale |
| **Citadel Securities** | HFT + market making + stat-arb | Latency + cross-asset scope |
| **DE Shaw** | Systematic multi-strategy | Breadth of strategies + risk management |

---

The real "secret sauce" at all these firms isn't a single algorithm — it's the **combination of data quality, feature engineering, robust backtesting infrastructure, and disciplined risk management**.

---

**References:**
- [Advances in Financial Machine Learning – Marcos López de Prado](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- [Jane Street: How We Think About Markets](https://www.janestreet.com/what-we-do/)
- [High-Flyer Capital / DeepSeek Background](https://www.reuters.com/technology/chinas-deepseek-ai-was-trained-high-flyer-quant-funds-gpu-cluster-2025-01-29/)
- [Two Sigma: Data Science in Finance](https://www.twosigma.com/articles/)
- [QuantLib & Academic Papers on Execution Algorithms (Almgren-Chriss)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=488769)