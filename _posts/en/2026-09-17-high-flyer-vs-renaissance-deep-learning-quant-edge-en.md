---
audio: false
generated: true
image: false
lang: en
layout: post
title: "High-Flyer vs. Renaissance: Deep Learning Quant Edge"
translated: false
type: note
---

Question: **How does High-Flyer (幻方量化) compare with Renaissance, D. E. Shaw, Citadel, Bridgewater, etc.?**

Answer: **High-Flyer is much closer to Renaissance / Two Sigma than to Bridgewater.** And its unusually interesting feature is that it appears to have pushed *deep learning into the core alpha-generation loop* earlier and more aggressively than most Western quant firms publicly describe.

One caveat: **the public performance record is nowhere near as transparent as Renaissance's**, so I would not claim that High-Flyer has definitively beaten Renaissance over a comparable multi-decade period.

### Rough map

| Firm                        | Core approach                                         | Scale                    | Publicly known edge                  |
| --------------------------- | ----------------------------------------------------- | ------------------------ | ------------------------------------ |
| **Renaissance / Medallion** | Statistical + ML + enormous research/execution system | Small by design          | 🏆 legendary sustained alpha         |
| **High-Flyer / 幻方**         | **Deep learning + systematic equity quant**           | ~$10B-class historically | **AI-native quant research**         |
| **D. E. Shaw**              | Quant + systematic + fundamental                      | Very large               | Extremely broad research/engineering |
| **Two Sigma**               | ML/statistics + alternative data                      | Very large               | Data + ML                            |
| **Citadel**                 | Quant + HFT + fundamental multi-strategy              | Huge                     | Execution + diversification          |
| **Bridgewater**             | Systematic macro                                      | Huge                     | Economic models / macro              |

High-Flyer's own description is unusually explicit: it says it started exploring **machine learning for fully automated trading in 2008**, put its first **deep-learning-generated positions into production in October 2016**, and applied deep learning comprehensively in 2017. It also says it has accumulated **10+ PB of market and other financial data**. ([High Flyer][1])

That's a pretty remarkable timeline.

### The really interesting comparison

I'd characterize the philosophies approximately like this:

```text
Renaissance
    │
    ├── discover statistical regularities
    ├── enormous feature/model zoo
    ├── portfolio optimization
    └── execution
          ↓
       MONEY
```

versus High-Flyer:

```text
High-Flyer
    │
    ├── enormous financial dataset
    │
    ├── neural networks
    │     ├── nonlinear features
    │     ├── representation learning
    │     └── sequence relationships
    │
    ├── portfolio construction
    │
    ├── execution
    │
    └── huge compute infrastructure
          ↓
       MONEY
```

And that last part is important.

High-Flyer's quant business actually became the **compute/data/research substrate that eventually produced DeepSeek**. Reuters reported that High-Flyer had built a portfolio around **100 billion RMB (~$13.8B)** using AI models for investment decisions, before Liang Wenfeng shifted substantial attention toward frontier AI research in 2023. ([Reuters][2])

So there's a very interesting lineage:

```text
2008
  │
  │ machine learning for trading
  ↓
2016
  │
  │ deep learning enters production
  ↓
2017+
  │
  │ massive AI quant infrastructure
  ↓
2020+
  │
  │ enormous GPU / data capability
  ↓
2023
  │
  │ DeepSeek
  ↓
2024+
  │
  │ V3 / R1
```

And **that is not just marketing mythology**: High-Flyer's own site describes both the quant operation and its independently built AI training platform, while the DeepSeek technical report documents the resulting large-scale ML infrastructure. ([High Flyer][3])

### But here's where I'd be careful

There are two very different questions:

**"Who made the most money?"**

vs.

**"Who built the most interesting quant research machine?"**

For the first, **Medallion remains the benchmark**. Its reported long-run returns are extraordinary.

For the second, **High-Flyer is absolutely in the conversation**.

There is also fresh evidence that High-Flyer's quant operation remained extremely strong: SCMP reported that High-Flyer Quant returned **56.6% in 2025**, ranking second among Chinese quant firms that year. ([South China Morning Post][4]) But a one-year number isn't comparable with Medallion's multi-decade record, and Chinese quant-fund reporting has less publicly auditable performance data than we'd ideally want.

### My mental model

If you're trying to understand the **evolution of quantitative trading**, I'd put them into generations:

```text
        1980s–2000s
             │
       Renaissance
             │
    statistical arbitrage
             │
             ▼
        2000s–2010s
             │
    D.E. Shaw / Two Sigma
             │
      data + ML + compute
             │
             ▼
        2010s–2020s
             │
        High-Flyer
             │
     deep learning native
             │
             ▼
        2020s–?
             │
       LLM / foundation
       models + agents
```

And **this is why High-Flyer is especially interesting to you as an AI engineer**.

The DeepSeek story wasn't really:

> "A quant guy randomly started an AI company."

It's closer to:

> **A quantitative research organization progressively turned itself into a giant machine-learning research organization.**

That distinction matters.

If you want, I can go one level deeper and reconstruct **what a High-Flyer/Renaissance-style quant stack probably looks like internally — data → features → neural nets → alpha → portfolio optimizer → execution**, including the math and a minimal PyTorch implementation.

[1]: https://www.high-flyer.cn/fund/?utm_source=chatgpt.com "量化基金"
[2]: https://www.reuters.com/technology/artificial-intelligence/high-flyer-ai-quant-fund-behind-chinas-deepseek-2025-01-29/?utm_source=chatgpt.com "High-Flyer, the AI quant fund behind China's DeepSeek"
[3]: https://www.high-flyer.cn/?utm_source=chatgpt.com "幻方| 首页"
[4]: https://www.scmp.com/tech/tech-trends/article/3339633/deepseek-founders-high-flyer-ranks-among-chinas-top-hedge-fund-firms-2025?utm_source=chatgpt.com "DeepSeek founder's High-Flyer ranks among China's top ..."
