---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kirin's constrained engineering achievement
translated: false
type: note
---

Question: **How good are Huawei Kirin chips today?**

Answer: **Kirin is technically impressive, but it is not yet competitive with Apple/Qualcomm at the absolute performance-per-watt frontier. Its real achievement is that Huawei rebuilt a modern smartphone SoC stack under severe manufacturing constraints.**

The interesting part is *how* they did it.

### 1. Kirin 9000S was the turning point

The **Kirin 9000S** in Mate 60 Pro was manufactured by SMIC on its **7nm-class N+2 process**, using DUV rather than EUV. TechInsights confirmed this through physical analysis. ([TechInsights][1])

That is significant because normally you'd expect:

```text
TSMC/Samsung
    ↓
EUV
    ↓
5nm / 4nm / 3nm
    ↓
high transistor density + high efficiency
```

Huawei/SMIC instead had roughly:

```text
DUV
 ↓
multiple patterning
 ↓
SMIC N+2 7nm
 ↓
Kirin 9000S
```

This is much harder and more expensive because DUV requires many more patterning steps.

So **"Kirin is 7nm" does not mean "Huawei simply has a normal 7nm process."** The manufacturing path is fundamentally more constrained.

---

### 2. But raw CPU performance isn't the strongest part

Kirin 9020, for example, is still around the performance level of older flagship Snapdragon generations rather than today's best Apple/Qualcomm silicon. ([Notebookcheck][2])

Conceptually:

```text
                    CPU performance
Apple A-series          ██████████
Snapdragon flagship     █████████
MediaTek flagship       █████████
Kirin 9020              ██████
```

And the problem isn't only CPU architecture.

It's:

```text
Architecture
     ×
Process node
     ×
Frequency
     ×
Power efficiency
     ×
Memory subsystem
     ×
GPU
```

Huawei is constrained on several of these simultaneously.

---

### 3. The more interesting chip is Kirin 9030

This is where things get much more interesting for someone looking at hardware/LLM systems.

Recent teardown work found that **Kirin 9030 uses SMIC's N+3 process**, still fundamentally derived from the 7nm family. TechInsights says N+3 is getting close to 5nm-class density. ([TechInsights][3])

More surprising:

* local metal pitch: **32.5 nm**
* transistor density: **~113.4 MTr/mm²**
* no EUV
* heavy use of multi-patterning / design-technology co-optimization

The density can actually exceed TSMC N6 in some measurements. ([Tom's Hardware][4])

But there's an important distinction:

> **transistor density ≠ chip performance**

The 9030 still trails current Apple/Qualcomm chips substantially in CPU performance and efficiency. ([Tom's Hardware][4])

That's exactly the kind of thing you should pay attention to as an engineer: **node name alone tells you surprisingly little.**

---

### 4. Huawei's real strength is system-level engineering

This is probably the most interesting thing about Kirin.

Huawei doesn't control the entire semiconductor stack:

```text
ASML EUV       ❌
TSMC           ❌
NVIDIA GPU     ❌
ARM latest IP  constrained
        ↓
Huawei/HiSilicon
        ↓
architecture + SoC + firmware
        ↓
SMIC
        ↓
DUV multi-patterning
```

So they compensate with:

* custom CPU cores
* custom GPU architecture
* aggressive physical design
* larger dies
* packaging
* memory optimization
* software optimization
* workload-specific engineering

The Kirin 9020, for example, moved further toward Huawei's own CPU cores rather than simply using standard Cortex cores. ([Notebookcheck][2])

That's why I wouldn't evaluate Kirin as:

> "Is it as fast as Snapdragon?"

I'd evaluate it as:

> **"How much performance can Huawei extract from constrained manufacturing technology?"**

That is a much more interesting question.

---

### 5. And Huawei is now attacking the scaling problem differently

Huawei announced its **τ (Tau) Scaling Law** in 2026, proposing techniques such as **LogicFolding** to improve system efficiency without relying purely on transistor shrinking. Reuters reports Huawei is targeting much more advanced effective capabilities through this approach. ([Reuters][5])

This is conceptually important:

```text
Traditional scaling

smaller transistor
       ↓
more transistors
       ↓
higher performance
       ↓
lower energy


Huawei's alternative direction

same-ish process
       ↓
better physical organization
       ↓
shorter data movement
       ↓
better utilization
       ↓
higher system efficiency
```

For AI hardware, **data movement is often more important than arithmetic itself**, so this direction is not crazy at all.

---

## My assessment

I'd rate Kirin roughly like this:

| Area                           | Kirin  |
| ------------------------------ | ------ |
| CPU peak performance           | 🟡     |
| CPU efficiency                 | 🟡     |
| GPU                            | 🟡     |
| Modem/connectivity integration | 🟢     |
| SoC integration                | 🟢     |
| Semiconductor engineering      | 🟢🟢   |
| Manufacturing efficiency       | 🔴     |
| Absolute leading-edge process  | 🔴     |
| Ability to survive sanctions   | 🟢🟢🟢 |
| Strategic importance           | 🟢🟢🟢 |

The key point is:

**Kirin isn't currently the world's fastest mobile SoC.**

But **Kirin is one of the world's most interesting semiconductor engineering projects**, because Huawei is demonstrating that you can compensate for a manufacturing disadvantage with architecture + physical design + packaging + software + enormous engineering effort.

And this is very similar to what you're seeing in **Huawei Ascend vs NVIDIA**: the interesting question isn't necessarily *"can Huawei beat NVIDIA's H100/B200 at FLOPS?"* but **"how much system-level capability can Huawei build despite not having access to the same semiconductor supply chain?"**

I can also break down **Kirin → Ascend → SMIC → EUV/DUV → why Huawei's strategy is relevant to LLM GPUs**, which connects directly to the GPU/LLM work you've been doing.

[1]: https://www.techinsights.com/blog/hisilicon-kirin-9000s-smic-7nm-n2-process-flow-full-analysis?utm_source=chatgpt.com "HiSilicon Kirin 9000s (SMIC 7nm, N+2) Process Flow (Full) Analysis | TechInsights"
[2]: https://www.notebookcheck.net/HiSilicon-Kirin-9020-Processor-Benchmarks-and-Specs.953640.0.html?utm_source=chatgpt.com "HiSilicon Kirin 9020 Processor - Benchmarks and Specs - Notebookcheck Tech"
[3]: https://www.techinsights.com/blog/smic-n3-confirmed-kirin-9030-analysis-reveals-how-close-smic-5nm?utm_source=chatgpt.com "Kirin 9030 Analysis Reveals How Close SMIC Is to 5nm"
[4]: https://www.tomshardware.com/tech-industry/semiconductors/smics-third-gen-7nm-node-shows-smaller-metal-pitch-than-intel-18a-higher-transistor-density-than-tsmc-n6-without-euv-analysis-of-n-3-shows-significant-advancement-for-chinese-semi-manufacturing?utm_source=chatgpt.com "SMIC's third-gen 7nm node shows smaller metal pitch than Intel 18A, higher transistor density than TSMC N6 without EUV - analysis of N+3 shows significant advancement for Chinese semi manufacturing"
[5]: https://www.reuters.com/world/asia-pacific/huawei-proposes-new-path-chip-development-amid-us-sanctions-2026-05-25/?utm_source=chatgpt.com "China's Huawei reveals chip design breakthrough amid US sanctions"
