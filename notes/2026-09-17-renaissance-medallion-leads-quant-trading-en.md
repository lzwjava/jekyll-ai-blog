---
audio: false
generated: true
image: false
lang: en
layout: post
title: Renaissance Medallion Leads Quant Trading
translated: false
type: note
---

Question: **Who has done best in quantitative trading — D. E. Shaw, Bridgewater, Renaissance, etc.?**

Answer: If by “best” you mean **long-term quantitative/systematic trading performance**, the answer is pretty clearly **Renaissance Technologies, specifically the Medallion Fund**.

| Firm / fund                         | What it is                |              Long-term reported performance | Style                             |
| ----------------------------------- | ------------------------- | ------------------------------------------: | --------------------------------- |
| **Renaissance — Medallion**         | Pure-ish systematic/quant |           **~39–40% net CAGR** over decades | Short-horizon statistical trading |
| **D. E. Shaw — Oculus / Composite** | Quant + multi-strategy    |            ~13–14% net CAGR since inception | Systematic + fundamental          |
| **Bridgewater — Pure Alpha**        | Systematic macro          | Much lower CAGR, but enormous scale/history | Macro, rates, FX, commodities     |
| **Citadel**                         | Multi-strategy + quant    |       Very strong, especially recent decade | HFT/stat arb + fundamental        |
| **Two Sigma**                       | Systematic quant          |          Strong historically, more variable | ML/statistical                    |
| **AQR**                             | Quant factor investing    |         More traditional systematic factors | Value/momentum/quality            |

The insane outlier is **Renaissance**.

Medallion reportedly generated about **39% annualized net returns from 1988–2018**. A peer-reviewed paper by Bradford Cornell calculated a **63.3% gross compound return** over 1988–2018 and found no negative annual return over that period. ([SSRN][1])

And this isn't just “Jim Simons got lucky.” The interesting part is the **system architecture**:

```text
                    Renaissance
                         │
             ┌───────────┴───────────┐
             │                       │
       massive datasets         mathematicians
             │                       │
             └───────────┬───────────┘
                         │
                  statistical models
                         │
                    many signals
                         │
              portfolio construction
                         │
                   execution / costs
                         │
                  continuous feedback
```

The key distinction is that **Medallion isn't really comparable to Bridgewater**.

Bridgewater is essentially:

```text
macro data
   ↓
economic relationships
   ↓
rates / FX / bonds / commodities
   ↓
systematic portfolio
```

Renaissance is much closer to:

```text
tick / order / price / volume / alternative data
                    ↓
              feature generation
                    ↓
             statistical signal
                    ↓
          very large portfolio
                    ↓
             execution engine
                    ↓
             repeat thousands/millions
                    ↓
                  P&L
```

D. E. Shaw sits somewhere between the two. Its Oculus Fund returned about **28.2% in 2025**, with a reported **14.4% annualized net return since 2004**; its larger Composite Fund returned about **18.5% in 2025** and **12.9% annualized since 2001**. ([Investing.com][2])

### The interesting ranking depends on what you mean by "best"

If you mean **highest sustained return on capital**:

**Renaissance / Medallion is in a completely different league.**

If you mean **largest successful systematic trading organization**:

**Bridgewater / D. E. Shaw / Citadel** become more interesting because Medallion deliberately stayed relatively small to preserve alpha.

If you mean **most interesting engineering/scientific approach**:

I'd study **Renaissance first**, then **D. E. Shaw**, then **Two Sigma**.

And there's a particularly interesting lesson for someone building ML systems: **Medallion's edge wasn't “one genius model.”** The evidence points toward an entire research → feature → model → portfolio → execution → feedback pipeline, with thousands of small edges. ([Quartr][3])

[Bradford Cornell's Medallion research paper](https://papers.ssrn.com/abstract=3504766?utm_source=chatgpt.com)

[Acquired — Renaissance Technologies deep dive](https://podcasts.apple.com/us/podcast/renaissance-technologies/id1050462261?i=1000649514382&utm_source=chatgpt.com)

I can also map **Renaissance vs D.E. Shaw vs Two Sigma vs Citadel at the algorithm/data/compute/execution level**—basically what their actual quant stack probably looks like.

[1]: https://papers.ssrn.com/abstract%3D3504766?utm_source=chatgpt.com "Medallion Fund: The Ultimate Counterexample? by Bradford Cornell :: SSRN"
[2]: https://www.investing.com/news/stock-market-news/de-shaws-flagship-funds-trump-market-volatility-to-beat-sp-500-in-2025-source-says-4428076?utm_source=chatgpt.com "Top hedge funds led by D.E.Shaw, Bridgewater and Balyasny deliver big gains in 2025  By Reuters"
[3]: https://quartr.com/insights/edge/renaissance-technologies-and-the-medallion-fund?utm_source=chatgpt.com "Renaissance Technologies and The Medallion Fund"
