---
audio: false
generated: true
image: false
lang: en
layout: post
title: DJI Revenue and Profit Estimates
translated: false
type: note
---

Question: **How much does DJI cost to run, and how much revenue/profit does it make?**

Answer: DJI is private, so there is **no audited public annual report** like Apple/NVIDIA. The numbers circulating are estimates, but they give a surprisingly clear picture.

### Rough DJI economics

| Year |                      Revenue |             Net profit | Net margin |
| ---- | ---------------------------: | ---------------------: | ---------: |
| 2017 |                       ¥17.6B |                  ¥4.3B |       ~24% |
| 2023 |                        ~¥50B |               ~¥9–10B* |    ~18–20% |
| 2024 |                    **>¥80B** |            **~¥12.1B** |       ~15% |
| 2025 | estimates around **¥85–90B** | not reliably disclosed |          — |

The 2017 figures are based on historical financial disclosures: ¥17.57B revenue and ¥4.3B net profit. ([ITDCW][1])

For 2024, multiple later reports put DJI at **~¥80B revenue and ~¥12.06B net profit**. ([CBNData][2]) There are also conflicting estimates claiming >¥50B rather than ¥80B, so I would treat **¥80B / ¥12B** as an estimate, not audited fact. ([The Paper][3])

### What does "cost" mean?

If revenue is ~¥80B and net profit is ~¥12B:

```text
Revenue                         ¥80B
├── components / manufacturing
├── R&D
├── employees
├── sales + marketing
├── logistics
├── warranty / support
├── offices / factories
├── taxes / interest / misc.
│
└── Net profit                  ~¥12B
```

So the implied total expense is roughly:

**¥80B − ¥12B ≈ ¥68B/year**

or around:

* **¥6.7B/month revenue**
* **¥1.0B/month net profit**
* **¥5.7B/month total expenses**

But don't interpret ¥68B as "manufacturing cost." It includes **COGS + R&D + salaries + sales + administration + taxes and other expenses**.

### The crazy part: DJI is a hardware company with unusually strong economics

At ¥80B revenue and ¥12B profit:

```text
Net margin ≈ 12 / 80
          ≈ 15%
```

That's extremely good for a hardware company.

And DJI isn't just selling a camera attached to four motors. The stack includes:

```text
Flight controller
        ↓
IMU / sensors
        ↓
Motor control + ESC
        ↓
Computer vision
        ↓
Obstacle avoidance
        ↓
Video encoding
        ↓
Gimbal stabilization
        ↓
Radio / transmission
        ↓
Mobile app
        ↓
Cloud / ecosystem
```

That vertical integration is a big reason DJI can capture so much value.

DJI reportedly maintains around **70–80% of the global consumer-drone market**, while expanding into cameras, gimbals, enterprise drones, agriculture, inspection, etc. ([36Kr][4])

### Compared with a normal startup

This is what makes DJI particularly interesting from a founder/engineering perspective.

Suppose:

```text
Revenue       ¥80B
Net profit    ¥12B
Employees     ~tens of thousands
```

Then the company can potentially generate **billions of RMB of internally generated cash every year** without needing to IPO or constantly raise VC.

That's a fundamentally different company-building model from:

```text
AI startup:
raise $50M
→ hire 200 people
→ buy GPUs
→ burn $10M/month
→ hope revenue catches up
```

DJI instead built a **high-margin physical product + proprietary technology + global distribution machine**.

And historical numbers show just how dramatically it scaled: revenue went from **¥8.3B in 2013 to ¥175.7B in 2017**. ([EE Times China][5])

The exact modern financials are opaque, though, so I would **not** quote "DJI makes ¥120.56B profit"—that is almost certainly a unit/number confusion. The ¥120.56B figure circulating in some reports is inconsistent with the more credible estimates of roughly **¥12B** net profit. ([Zhihu][6])

I can also break down **DJI's estimated BOM for a ¥5,000–¥10,000 consumer drone**—motors, camera, gimbal, battery, flight controller, manufacturing, R&D allocation, retailer margin, and DJI's actual likely gross profit.

[1]: https://www.itdcw.com/?utm_source=chatgpt.com "大疆创新：从无人机到无所不能2017年营收175.7亿元_电池网"
[2]: https://www.cbndata.com/?utm_source=chatgpt.com "大疆降价风暴背后：顶流也有增长焦虑"
[3]: https://m.thepaper.cn/?utm_source=chatgpt.com "最低调的大疆，抢最狠的市场"
[4]: https://eu.36kr.com/?utm_source=chatgpt.com "素食者汪滔：深陷千亿大疆王国的困境"
[5]: https://www.eet-china.com/?utm_source=chatgpt.com "大疆创新2023年人均营收"
[6]: https://zhuanlan.zhihu.com/?utm_source=chatgpt.com "赚1块、花3块，刘靖康死磕汪滔"
