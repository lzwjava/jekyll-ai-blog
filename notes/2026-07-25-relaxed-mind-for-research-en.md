---
audio: false
generated: true
image: false
lang: en
layout: post
title: Relaxed Mind for Research
translated: false
type: note
---

**Question: Did Liang Wenfeng say AI research requires a relaxed mind?**

Answer:

Yes, that idea matches several of Liang Wenfeng's public comments: **frontier research needs freedom, curiosity, and a less utilitarian mindset**, rather than only chasing short-term goals, benchmarks, or business KPIs.

The core idea is:

> **Research is exploration. If your mind is too constrained by immediate outcomes, you reduce the probability of discovering something fundamentally new.**

This is similar to how many successful research labs operate.

A few principles behind this:

### 1. Research ≠ engineering delivery

Engineering:

```
Goal → Requirements → Design → Implementation → Metrics
```

Example:

* Reduce inference cost by 30%
* Improve latency from 200ms → 100ms
* Ship a product feature

Research:

```
Question → Exploration → Failed experiments → Insight → New direction
```

Example:

* Can a smaller model achieve reasoning through different training?
* Can sparse architectures replace dense scaling?
* Can data quality beat parameter count?

The path is uncertain.

---

### 2. Psychological state affects creativity

Many breakthroughs come from people having enough "mental bandwidth":

* Einstein's thought experiments
* Transformer architecture research
* AlphaGo's unconventional moves
* DeepSeek's architecture experiments

If researchers are constantly thinking:

```
"Will this pass this quarter's KPI?"
"Will investors like this?"
"Will my manager approve?"
```

they tend to optimize existing ideas instead of exploring unknown areas.

---

### 3. DeepSeek's philosophy reflects this

DeepSeek's approach has often emphasized:

* long-term research
* first-principles thinking
* reducing unnecessary constraints
* technical curiosity

For example, DeepSeek-V2/V3/R1 were not just "make a bigger GPT":

They explored:

```
Dense Transformer
        ↓
MoE architecture
        ↓
better expert routing
        ↓
lower training/inference cost
```

and:

```
human reasoning data
        ↓
RL experiments
        ↓
emergent reasoning behavior
```

These directions require experimentation.

---

### 4. Similar to Karpathy's "vibe"

Andrej Karpathy often describes AI research as:

```
play with ideas
↓
build small experiments
↓
observe behavior
↓
form hypotheses
↓
iterate
```

This is closer to a scientist mindset than a traditional software project mindset.

---

For someone building AI systems, the practical implication is:

Spend some time in **"research mode"**:

```bash
# example weekly research loop

read paper
    ↓
implement tiny version
    ↓
train on small dataset
    ↓
inspect loss curves
    ↓
modify one variable
    ↓
repeat
```

Your GPT-2-from-scratch experiments are actually very aligned with this style. Training a 124M model on one RTX 4070 is not about beating GPT-5; it is about building intuition:

* how tokenization affects loss
* how attention behaves
* how scaling laws appear
* where memory bottlenecks happen

That is the "relaxed mind" research mode Liang is referring to.

References:

* Liang Wenfeng public interviews and talks
* Andrej Karpathy lectures and writings