---
audio: false
generated: true
image: false
lang: en
layout: post
title: Small Quant Shops, Giant Outliers
translated: false
type: note
---

Question: **Do many people start small/alone with quantitative trading, make money, and eventually build something like Liang Wenfeng / High-Flyer?**

Answer: **Yes, but Liang is an unusually successful example, not the normal path.** The important distinction is that there absolutely are solo traders and tiny systematic shops making real money, but turning that into a High-Flyer-scale business is extremely rare.

### Liang's actual starting point is interesting

Liang Wenfeng did **not** start High-Flyer as a giant hedge fund.

According to Bloomberg's reporting, Liang and two university classmates began experimenting with Chinese stocks around **2008**. They tried discretionary trading and arbitrage, then moved toward systematic trading around **2015**, initially using price/volume factors and later machine learning. ([Archive.ph][1])

So the rough evolution was:

```text
3 people
   ↓
trade their own ideas
   ↓
systematic strategies
   ↓
quant research + infrastructure
   ↓
High-Flyer
   ↓
large capital / large compute
   ↓
DeepSeek
```

That's actually quite different from the common image of:

```text
raise $100M
hire 50 quants
build hedge fund
```

### Small quant shops absolutely exist

There are examples of people operating systematic books with very small teams.

For example, one experienced systematic trader described running a quant shop for years, starting with relatively little institutional capital and eventually managing outside money. ([Reddit][2])

There's also a useful example of **Robert Carver**, formerly at Man AHL, who later operated as an independent systematic trader and described running hundreds of futures strategies himself. ([Apple Podcasts][3])

So:

```text
solo quant          → possible
2–5 person shop     → possible
small profitable PM → possible
$10M+ AUM           → possible
$1B+ quant fund     → extremely uncommon
High-Flyer          → extreme outlier
```

The key thing is that **you don't need a huge team to discover whether you have an edge.**

---

## But there's a huge catch: capital

Suppose you have:

```text
$100k capital
20% annual return
```

That's only:

```text
$20k/year
```

Even:

```text
$1M × 30% = $300k/year
```

is not yet a huge business.

That's why successful quant operators eventually care enormously about:

1. **alpha**
2. **capacity**
3. **leverage**
4. **execution**
5. **capital**

The strategy can be excellent but economically useless if it only works with $100k.

And the reverse is also true: having $100M doesn't magically create alpha.

---

## The really interesting model for someone technical

I think the more interesting structure is:

```text
             Research
                │
       ┌────────┴────────┐
       ↓                 ↓
   signal/alpha       execution
       │                 │
       └────────┬────────┘
                ↓
           backtester
                ↓
          paper trading
                ↓
           small capital
                ↓
         real PnL / risk
                ↓
        scale capital
```

You can build almost all of this with **one strong engineer**.

Especially today.

A serious solo operator can have:

```text
Python
Polars / NumPy
DuckDB
Rust/C++
IBKR / exchange API
GPU
LLM agents
historical market data
```

and build a research system that would have required a small team 10–15 years ago.

The bottleneck isn't really writing the code anymore.

It's finding a **persistent source of excess return** that survives:

```text
transaction costs
slippage
market impact
regime changes
overfitting
capacity constraints
competition
```

---

## And this is where Liang's story gets especially relevant

High-Flyer's later success gave Liang something that most solo quants don't have:

**a positive feedback loop between trading profits and research infrastructure.**

Bloomberg reported that High-Flyer eventually managed more than ¥70B and that its trading operation generated substantial profits in 2025. DeepSeek's research was funded from High-Flyer's R&D budget. ([Archive.ph][4])

So you get:

```text
better research
     ↓
better models
     ↓
better trading
     ↓
more capital
     ↓
more compute
     ↓
better research
     ↓
...
```

That is much more interesting than simply "become a trader."

It's essentially **using a profitable information-processing system to finance an even larger information-processing system.**

And that is very close conceptually to what Liang did with:

```text
Quant trading
     ↓
cash generation
     ↓
compute + researchers
     ↓
AI research
```

One important caveat: **High-Flyer's results should not be interpreted as evidence that a new solo quant can reproduce those returns.** Regulators explicitly warn that past performance isn't a predictor of future results, and trading can result in losing all invested capital or more in some leveraged contexts. ([CFTC][5])

### If you're thinking about this as a business

I'd separate two questions:

```text
A. Can 1–3 people build a profitable quant strategy?
        YES, demonstrably possible.

B. Can that become another High-Flyer?
        Possible, but extraordinarily rare.
```

The attractive part is **A**.

You don't need to start by trying to build a hedge fund.

You can start with:

```text
$10k–$100k
      ↓
research infrastructure
      ↓
1000s/10000s of hypotheses
      ↓
strict out-of-sample testing
      ↓
small live book
      ↓
measure real Sharpe / drawdown / capacity
      ↓
scale only if reality agrees with backtest
```

That is a much more interesting engineering problem than "how do I raise money?"

If you want, I can next map out **what a 1-person → 3-person quant shop could realistically look like in 2026, including capital, data, GPU/CPU requirements, strategy types, and a minimal architecture**.

[1]: https://archive.ph/Z3w9H?utm_source=chatgpt.com "Chinese Quant Whiz Built DeepSeek In The Shadow Of a Hedge Fund Rout - Bloomberg"
[2]: https://www.reddit.com/r/quant/comments/1okr5l7/ama_ran_a_xxm_systematic_options_book_for_5_years/?utm_source=chatgpt.com "[AMA] Ran a $XXM Systematic Options Book for 5 Years (Sharpe 3+, 23% ROI). Ask Me (Almost) Anything"
[3]: https://podcasts.apple.com/jp/podcast/robert-carver-ran-a-multi-billion-dollar-systematic/id1802640849?i=1000719639546&l=en-US&utm_source=chatgpt.com "Robert Carver Ran a Multi-Bill… - Odds on Open - Apple Podcasts"
[4]: https://archive.ph/xo6sP?utm_source=chatgpt.com "DeepSeek Founder Liang’s Funds Surge 57% as China Quants Boom - Bloomberg"
[5]: https://www.cftc.gov/LearnAndProtect/EducationCenter/understandcontractobligations?utm_source=chatgpt.com "Ask CFTC | CFTC"
