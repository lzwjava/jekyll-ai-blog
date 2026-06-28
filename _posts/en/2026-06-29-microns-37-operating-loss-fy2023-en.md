---
audio: false
generated: true
image: false
lang: en
layout: post
title: Micron's 37% Operating Loss FY2023
translated: false
type: note
---

Question: Did Micron Technology (MU) have a gross/operating margin around -35% in fiscal 2023, and if so, why?

Answer:

Let me pull the actual numbers first.Your number is close but the metric matters. Here are Micron's actual fiscal 2023 (ended Aug 31, 2023) full-year figures:

- GAAP gross margin was -9.1% of revenue (-$1,416M on $15,540M revenue), down from +45.2% in FY2022
- GAAP operating margin (operating loss) was -37.0% of revenue (-$5,745M), versus +31.5% the prior year
- Net loss was $5,833M, or -$5.34 per diluted share

So the **-35%/-37% figure is the operating margin**, not gross margin. Gross margin was -9% for the year, and bottomed even lower at the quarterly level. The worst single quarter was FQ2-23: GAAP gross margin of -32.7% (-$1,206M on $3,693M revenue), with an operating loss of $2,303M. Revenue itself collapsed from $30.8B (FY22) to $15.5B (FY23) — roughly cut in half.

## Why it cratered

This was a textbook memory-industry downcycle, the deepest in over a decade. The mechanics:

**1. Demand collapse + inventory glut.** Post-COVID, the PC and smartphone markets crashed simultaneously. Data center customers (hyperscalers) had massively over-ordered in 2021–2022 and spent 2023 burning down inventory instead of buying. So demand fell off a cliff right as supply was peaking.

**2. Pricing free-fall.** DRAM and NAND are commodities sold at spot prices. When supply exceeds demand, prices don't soften — they collapse. Bit prices fell ~40–50% year-over-year. Memory has near-zero pricing power in a glut because every bit is fungible.

**3. The cost structure is the killer.** This is the part worth internalizing as an engineer. Memory fabs are extreme fixed-cost businesses — you've sunk $15–20B into a fab whether it runs at 100% or 60% utilization. Depreciation, EUV/DUV tool amortization, and clean-room overhead don't shrink when demand drops. When ASP per bit falls below per-bit manufacturing cost, gross margin goes negative — you're selling chips for less than the variable+allocated cost to make them.

**4. Inventory write-downs.** A big chunk of the negative gross margin was non-cash: Micron wrote down the carrying value of finished/WIP inventory to net realizable value because market prices had fallen below book cost. That's why GAAP gross margin (-32.7% in FQ2) was actually worse than the non-GAAP figure (-31.4%) in some quarters — write-downs hit GAAP harder.

**5. China CAC ban.** A secondary blow: the Cyberspace Administration of China's decision in 2023 barred Micron products from Chinese critical-infrastructure operators, which management called a significant headwind slowing the recovery.

The response was classic downcycle discipline: cut capex hard (FY23 capex of $7.01B produced negative $5.45B adjusted free cash flow), idle/underload fabs, and slash bit supply growth to force the industry back toward supply-demand balance.

The recovery, for context, was driven by AI/HBM — by FY2025 Micron hit record revenue with gross margins back above 50%. The memory cycle is brutal but mean-reverting: the same fixed-cost leverage that destroys margins in a glut amplifies them violently on the way up.

## The mental model

```
operating_margin = (revenue - COGS - opex) / revenue

# In a glut, for a fab-heavy commodity:
#   revenue ↓↓  (price collapse × volume drop)
#   COGS stays high (fixed depreciation/overhead don't scale down)
#   + one-time inventory write-downs inflate COGS further
#   opex roughly flat (R&D for next node can't stop)
# => margin goes deeply negative, and operating margin
#    swings harder than gross margin because opex is fixed too
```

FY23: revenue halved, gross margin -9%, operating margin -37%. The gap between -9% and -37% is your fixed opex (R&D + SG&A of ~$4.3B) divided over collapsed revenue — operating leverage working in reverse.

References:

- [Micron FQ4-23 / FY23 Annual Results (8-K)](https://www.sec.gov/Archives/edgar/data/0000723125/000072312523000051/a2023q4ex991-pressrelease.htm)
- [Micron FQ2-23 Results (8-K) — trough quarter](https://www.sec.gov/Archives/edgar/data/0000723125/000072312523000018/a2023q2ex991-pressrelease.htm)
- [Micron FQ3-23 Results (8-K) — China CAC headwind](https://www.sec.gov/Archives/edgar/data/0000723125/000072312523000038/a2023q3ex991-pressrelease.htm)
