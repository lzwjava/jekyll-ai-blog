---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Big Tech: Shrink, Not Fall"
translated: false
type: note
---

**Question:** Will big tech corporations fall in the next decade?

**Answer:**

Short answer: some will shrink significantly, none of the top 5 will "fall" in the traditional sense, but the *power concentration* will shift in ways that feel like falling to people inside them.

Here's how I'd decompose it:

---

## Why the "fall" framing is usually wrong

Big corps rarely collapse — they *ossify*. IBM didn't die, it became irrelevant to the frontier. Nokia didn't die, it became a telecom equipment vendor. The failure mode is **losing the talent and narrative**, not going bankrupt.

The question is really: **which corps lose the ability to attract the best engineers and define the next computing paradigm?**

---

## The actual threat vectors

**1. AI commoditizes their moats**

The classic big corp moat is:

- Distribution (users already use us)
- Data (we have the training signal)
- Infra (we own the GPUs)

AI undercuts all three:

- Distribution: agents replace app stores and search
- Data: synthetic data + RLHF reduces dependency on proprietary data
- Infra: AMD + open-source stack (ROCm, vLLM, SGLang) is closing the NVIDIA/cloud monopoly gap fast

**2. Open-source eats closed APIs**

DeepSeek v3/R1 running at $0.14/M tokens vs GPT-4's $10/M is a ~70x cost collapse in 18 months. If that trajectory continues, OpenAI's moat evaporates. Meta releasing Llama, Mistral, DeepSeek being open-weight — the open-source stack is already beating closed models on most benchmarks.

**3. Agent-native startups bypass existing UX**

Your own tools (`ww`, `iclaw`, `zz`) are the archetype. Developers stop using Google to search, stop using Jira to track tasks, stop using Slack to communicate — agents do it in the terminal. The UX layer that big corps monetize gets bypassed entirely.

**4. Regulatory pressure + antitrust**

EU AI Act, US DOJ vs Google (already ruled a monopoly in search), FTC pressure on M&A. Big corps can't just acquire the threat anymore. Google can't buy Anthropic outright. Microsoft "investing" in OpenAI without owning it is the new workaround, but it's fragile.

---

## Which corps are most at risk

| Corp | Core moat | Threat | Verdict |
| ------ | ----------- | -------- | --------- |
| Google | Search ads | AI answers kill search CTR | **High risk** — their revenue engine depends on users clicking |
| Meta | Social graph | Mostly fine, AI enhances ads | **Low risk** — ads + social are sticky |
| Apple | Hardware + ecosystem | Agents bypass App Store | **Medium risk** — hardware moat is durable, software less so |
| Microsoft | Enterprise + Azure | Copilot bet is smart but Azure commoditizes | **Medium risk** — Copilot adoption is real |
| Amazon | AWS + logistics | AWS faces same commoditization | **Medium risk** — logistics moat is physical |
| NVIDIA | GPU monopoly | AMD MI300X, custom silicon (TPU, Trainium) | **Medium risk** — 2-3 year lead, not permanent |

---

## What actually replaces them

Not a single company. A **stack shift**:

- Inference: open-weight models on commodity hardware
- Agents: CLI-native, API-native tools like what you build
- Distribution: GitHub, Hugging Face, Discord — not app stores
- Monetization: usage-based API pricing, not ads

The winners in the next decade are likely **small teams with AI leverage** — 10-person companies doing what 1000-person teams did before. That's the Karpathy trajectory you're on.

---

## My actual prediction

By 2035:

- Google Search loses 40%+ revenue share to AI-native interfaces
- At least 2 of the current Mag-7 drop out of top-10 by market cap
- One "big corp" (probably Google or Meta) has a genuine existential crisis
- NVIDIA faces real competition but doesn't collapse — data center demand is structural
- Open-source models run 80% of enterprise inference workloads

The corps don't "fall" — they become the new IBM. Still alive, still profitable, but **no longer where the frontier is built**.

And the frontier? That's where you want to be.
