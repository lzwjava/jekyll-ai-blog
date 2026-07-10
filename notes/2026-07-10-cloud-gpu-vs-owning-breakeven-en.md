---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Cloud GPU vs. Owning: Breakeven?"
translated: false
type: note
---

Question: One conclusion: the future is remote-first work, unless a company can supply 3-5 machines or 2-3 GPUs per person — companies' real advantage is having enough money to fund large model training, so it's really just a handful of well-funded companies vs. everyone else. Otherwise, a company can't out-compete a solo or small-team AI founder who runs experiments faster and burns tokens faster. The future engineer is like a workshop, similar to today's factories. Is cloud GPU the better solution?

Answer:

Your framing is directionally right, but it collapses two very different competitions into one, and that distinction is exactly where cloud GPU changes the math.

**Competition 1: Pretraining frontier models.** This is compute-scale warfare — DeepSeek-V4, Llama, Kimi — where you need thousands of H100/H800/MI300X-class chips running for weeks, plus a data pipeline team, plus RLHF infra. No solo founder competes here, cloud or not. Not because of $/hr pricing, but because of *aggregate* GPU-hours needed (10^23+ FLOPs) and the interconnect (NVLink/InfiniBand fabric) that a rented single-node pod simply doesn't give you. This tier stays locked to labs with $100M+ budgets regardless of how cheap cloud GPU gets.

**Competition 2: Everything downstream of a base model** — fine-tuning, LoRA, RLHF/GRPO on top of an open model, agent architectures, RAG, deployment, custom tool-use pipelines, dataset engineering. This is where you and I actually operate, and here your thesis is correct: a solo founder with fast iteration loops and zero bureaucracy can out-experiment a mid-size company's ML team, because the bottleneck isn't raw FLOPs, it's **iteration velocity** — how fast you can try an idea, fail, and try the next one. A company with 3-5 dedicated machines has more raw compute than you, but if there's a ticket queue, a data governance review, and a manager sign-off before someone runs an experiment, they lose to you on wall-clock time per idea tested, even with less hardware.

**Is cloud GPU the better solution? Yes, and the numbers back it hard right now.**

The rental market has cratered in price through 2026. Current representative on-demand H100 rates:

| Provider tier | H100 $/hr |
|---|---|
| RunPod Secure Cloud | $2.39–2.89 |
| RunPod Community Cloud | $1.99 |
| Vast.ai (cheapest) | ~$1.49 |
| Spheron spot | $1.66 |
| Lambda / CoreWeave | $2.89–3.90+ |

Purchasing an H100 outright costs upwards of $25,000–$30,000 per card. Quick breakeven math for owning vs. renting:

```python
def breakeven_hours(purchase_price, rental_rate_per_hr, power_cost_per_hr=0.15):
    """Hours of use before owning beats renting (ignoring depreciation/resale, interest, obsolescence)."""
    net_rental_cost = rental_rate_per_hr  # already includes power in cloud pricing
    return purchase_price / (net_rental_cost - power_cost_per_hr)

# H100 SXM purchase vs RunPod Secure Cloud rental
hrs = breakeven_hours(27000, 2.69)
print(f"{hrs:.0f} hours ({hrs/24:.0f} days of 24/7 use) to break even")
```

At $27K purchase vs $2.69/hr rental, that's roughly 10,600 hours — **~440 days of continuous 24/7 use** — before ownership pays off, and that's before counting depreciation (H100 resale value drops fast as H200/B200/next-gen ship), electricity, cooling, failure risk, and the opportunity cost of capital tied up in a card that sits idle most of the time for a solo dev doing bursty experiments.

For your actual workload pattern — bursty fine-tuning runs, occasional pretraining experiments (GPT-2 760M scale, nanochat-scale), not 24/7 saturation — **renting wins decisively**. Your own AMD Dev Cloud droplet at ~$2/hr is the correct instinct: you get MI300X-class 192GB HBM3 compute on demand, pay only for active hours, and never carry depreciation risk. Your RTX 4070 box is right for iteration/dev/debugging (cheap, always-on, no per-hour meter), and cloud is right for the actual expensive training runs.

**The real "workshop vs factory" dynamic** isn't compute ownership — it's this:

- **Factories (well-funded labs):** own the fab-scale compute, competing on pretraining frontier models and foundational research
- **Workshops (you):** rent compute elastically, compete on specialization, speed, and direct client relationships — you can serve a client in Hong Kong doing custom fine-tuning in the time it takes a company's internal ML team to get GPU allocation approved

This actually maps closely to how software already works — nobody owns their own AWS datacenter to run a SaaS product; you rent EC2. GPU compute for AI is just repeating that same commoditization curve, a few years behind. The "moat" was never owning hardware — it's model/data/pipeline expertise plus the willingness to move without approval chains. That's exactly your Tinker-level-skills-as-moat thesis, and it holds up.

One caveat worth tracking: as spot/community pricing keeps falling (Vast.ai already near $1.49/hr, some tracked listings <$1/hr), the economics tilt even further toward rent-everything. The one place I'd still consider owning hardware is your dev-loop machine (the 4070 box) for cheap always-on iteration where the meter-anxiety of cloud billing would otherwise slow you down psychologically — that's a real cost even if it's not in the spreadsheet.

References:

- [H100 Rental Prices Compared — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [RunPod H100 PCIe Pricing](https://www.runpod.io/gpu-models/h100-pcie)
- [RunPod Pricing Calculator — UsagePricing](https://www.usagepricing.com/tools/pricing-calculator/runpod)
- [H100 Cloud Pricing Comparison — getdeploying.com](https://getdeploying.com/gpus/nvidia-h100)
