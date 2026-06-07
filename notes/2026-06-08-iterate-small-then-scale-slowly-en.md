---
audio: false
generated: true
image: false
lang: en
layout: post
title: Iterate Small, Then Scale Slowly
translated: false
type: note
---

**Question:** Isn't Han Dong's 80M yuan dump like newbie LLM startups burning millions on failed GPU training runs? And shouldn't the principle be: iterate small (1M shrimp/H100s), run stable for months, then scale — scale down fast, not dump everything?

**Answer:**

Exactly. You've nailed the **core operational principle across all capital-intensive domains**. And yes, the pattern is identical:

## The Scaling Mistake Pattern

**Han Dong's error:**
- Built 300M yuan supply chain
- Tried to prove it at scale (full Egypt ops)
- One execution failure → dump 80M yuan inventory instead of pausing and diagnosing
- Never ran the "small stable experiment" long enough to catch failure modes before going big

**LLM startup equivalent:**
- Raise 50M funding
- Immediately spin up 10,000 H100s to train "our proprietary 70B model"
- Hit a data pipeline bug at week 3 → waste 5M on compute for corrupted runs
- Fail to ship before capital dries up
- Never did a 7B test run on 100 H100s first to validate the training loop

**You're describing the correct mental model:**

```
Phase 1 (Validation): Small, run 2-3 months
├─ 1M shrimp / 100 H100s / 10 person team
├─ Measure unit economics, failure rates, quality consistency
├─ Iterate on operations until stable
└─ Cost: 500K (tolerable loss)

Phase 2 (Prove repeatability): 3-5M shrimp / 500 H100s / 50 people
├─ Run 2-3 months, verify scale doesn't break assumptions
└─ Cost: 3-5M (still within reasonable loss budget)

Phase 3 (Full deploy): 80M shrimp / Egypt ops / 500 people
├─ Only after Phase 1&2 proven
└─ Cost: justified by evidence
```

## Why Startups Break This Rule

1. **Narrative pressure** — Investors fund you for "visionary" big plays, not "small test runs." After raising 370M yuan, running 1M test shrimp for 2 months looks like wasting time

2. **Founder psychology** — Success bias. After winning once, skipping intermediate validation feels like you "know" this time. (Han Dong had built a 1B yuan business before — he thought he could scale Egypt ops immediately)

3. **Capital efficiency narrative** — "We'll burn less if we go big immediately" (false). One failed 80M experiment > three 3M experiments that catch bugs early

4. **Team inexperience** — Most founders haven't managed **hardware-heavy operations** (GPU clusters, supply chains, manufacturing). Software startups scale incrementally because they *have to* (can spin up servers cheaply). Physical ops founders often don't know this yet.

## The Hiring Parallel You Mentioned

Exactly right. Same principle:

**Wrong:** Hire 500 people → build org structure → discover nobody knows your actual workflow
**Right:** Hire 30 → run 2 months → understand what breaks → hire 100 → run 2 months → scale to 500

The companies that survive understand: **scale slowly, descale fast**.

- Descale: shut down 80M shrimp batch, pivot to 1M, re-stabilize (cost: 1-2M not 80M)
- Not descale: throw away the whole batch, blame supplier, keep paying salaries, spiral debt

## Why This Matters for Your AI Work

You're training models on GPU clusters. Apply this exact principle:

```python
# Phase 1: Validate on RTX 4070
- Train 160M params, 1B tokens, 2 weeks
- Measure: loss curve, inference latency, VRAM efficiency
- Cost: ~$200 in electricity

# Phase 2: Prove on AMD MI300X subset
- Train 1B params, 10B tokens, 2 weeks
- Measure: does it still scale linearly? any new failure modes?
- Cost: ~$2K

# Phase 3: Full 7B/760M run
- Only if Phase 1&2 clean
```

Han Dong didn't do Phase 1&2 for Egypt supply. That's the mistake.

---

**The deeper insight:** This is why **small founders with limited capital often succeed better** than well-funded ones. Constraints force the right rhythm. You're forced to validate at 1M before going to 80M. Elon's approach works because he iterates publicly (Starship explosions are controlled Phase 1&2 failures, not 80M shrimp dumps).
