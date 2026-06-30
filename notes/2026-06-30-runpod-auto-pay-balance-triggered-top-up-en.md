---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Auto-Pay Balance-Triggered Top-Up
translated: false
type: note
---

Question: How does RunPod's auto-pay (automatic billing) work, based on the settings shown?

Answer:

It's a balance-triggered top-up. You prepay RunPod in credits (not postpaid invoicing), and auto-pay keeps that prepaid balance from hitting zero while your pods/endpoints are burning it down.

The two fields map directly to a threshold + reload pair:

- **"When my balance falls below: $10"** — the trigger threshold. The moment your credit balance drops under this, you become eligible for a recharge.
- **"Automatically add: $25"** — the reload amount. RunPod charges your default saved card for this and adds it as credit.

The rate limit matters: **billed max once per hour**. So even if you're draining credits fast (e.g., a multi-GPU pod at several $/hr), auto-pay won't fire repeatedly within the same hour — it tops up $25, waits up to an hour, and only re-triggers if you're still below $10 at the next eligible window.

Concrete walkthrough with your numbers:

```
balance = $12
running pod burns $4/hr

t=0h   balance $12  → above $10, no charge
t=0.5h balance $10  → at threshold
t=0.6h balance $9.20 → below $10 → CHARGE $25 → balance $34.20
t=1.6h balance $30.20 (1hr later, still draining) → above $10, no charge
...continues until balance dips below $10 again, then next charge eligible
```

The edge case to watch: if your burn rate exceeds **$25/hr**, auto-pay can't keep up. A single MI300X-class or 8×GPU pod can burn faster than $25/hr, and since reloads are capped at once/hour, your balance can still hit $0 mid-hour and your pod gets **stopped/terminated** before the next reload window. For high-burn workloads, either raise the "add" amount well above your hourly burn, or keep a manual buffer.

Practical config for your usage (AMD Dev Cloud ~$2/hr equivalent, occasional bigger pods):

- If you only run single GPUs around $2–4/hr → defaults ($10 / $25) are fine; that's ~6+ hours of runway per reload.
- If you spin up 8×GPU or high-end pods → set threshold higher (e.g., $50) and add higher (e.g., $100+) so one hourly reload comfortably exceeds your worst-case hourly spend.

One more thing: auto-pay is about *prepaid credit*, so there's no surprise end-of-month bill — your exposure per hour is bounded by the reload amount. That's a nice property if you want a hard-ish ceiling on accidental spend (forgot to stop a pod) — though a runaway pod will still drain and re-trigger hour after hour, so set [spend limits / pod time limits](https://docs.runpod.io) too if you want a true cap.
