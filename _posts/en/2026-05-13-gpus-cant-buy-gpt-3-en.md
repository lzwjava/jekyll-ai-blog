---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPUs Can't Buy GPT-3
translated: false
type: note
---

**Question:** My entrepreneur friend is willing to give me a 5,000 CNY budget for GPU training to build a GPT-3-level model. Is that a good deal? And should we collaborate with others instead of working alone?

---

**Answer:**

## Reality Check: 5,000 CNY Is Nowhere Near Enough for GPT-3 Training

Let's be very direct with you — this budget is **orders of magnitude too small** for training a GPT-3-scale model.

### Currency Context First

5,000 CNY is currently worth approximately **$735 USD** at today's mid-market exchange rate.

### What Does GPT-3 Training Actually Cost?

The compute cost for training GPT-3 (175 billion parameters) was estimated to range from about **$500,000 up to $4.6 million**, depending on the hardware and optimization techniques used.

OpenAI reportedly used thousands of NVIDIA V100 GPUs, each costing around $10,000, and a typical training cluster might include hundreds of these GPUs, quickly pushing total hardware costs into the millions.

So your $735 budget vs. the minimum ~$500,000 cost means you are **roughly 680× short** of even the most optimistic estimate.

### What Can You Actually Do With ~$735?

The most effective cost optimization strategies are: **fine-tuning** existing pre-trained models using LoRA/QLoRA adapters (80–95% savings), cloud spot instances (40–80% savings), and using parameter-efficient architectures (30–70% savings). Combining these strategies can achieve over 90% total cost reduction.

With ~$735, here is what is **realistically possible**:

| Goal | Feasibility |
| --- | --- |
| Fine-tune a small open-source model (e.g. Llama 3 8B) with LoRA | ✅ Yes |
| Train a tiny custom model (< 1B parameters) | ✅ Possible |
| Pre-train GPT-3 (175B parameters) from scratch | ❌ Completely impossible |

For fine-tuning open-source LLMs, most startups succeed with a single A100 80GB GPU for models up to 13B parameters, using techniques like LoRA or QLoRA to reduce memory requirements.

---

## On Collaboration: Yes, But Be Strategic

You are right that collaboration is important — **but the right kind matters**.

Here is a realistic framework for what you and your friend should do:

1. **Reframe the goal.** Don't aim to re-train GPT-3. Instead, fine-tune an existing open-source model (like Llama 3, Mistral, or Qwen) for a specific use case. That is where the $735 can actually stretch.

2. **Collaborate smartly.** Look into communities like Hugging Face, EleutherAI, or academic partnerships. These groups pool compute resources and datasets for collaborative AI training.

3. **Use the budget as seed money.** Use the 5,000 CNY to run experiments and demonstrate a proof of concept, then seek cloud credits (AWS, Google, Azure all offer startup AI credits worth thousands of dollars).

4. **Be honest with your friend.** A good partnership starts with transparency. Tell your friend that while the budget is appreciated, training GPT-3 from scratch is not feasible at this scale — but there are meaningful things you *can* build with it.

---

## Summary

- ✅ Your friend's support and willingness to invest is genuinely a good start for a partnership.
- ❌ 5,000 CNY (~$735) is not enough to train a GPT-3-level model — the real cost is **$500K to $4.6 million**.
- ✅ With this budget, you can fine-tune existing open-source models, which is actually how most AI startups and researchers work today.
- ✅ Collaboration is the right instinct — leverage communities, open-source tools, and cloud credit programs to go further.

---

**References:**

- [AI Model Training Costs 2026 Analysis](https://localaimaster.com/blog/ai-model-training-costs-2025-analysis)
- [What is the Cost of Training Large Language Models? — Cudo Compute](https://www.cudocompute.com/blog/what-is-the-cost-of-training-large-language-models)
- [How Much Does It Cost to Train GPT-3? — BytePlus](https://www.byteplus.com/en/topic/499187)
- [GPU Cloud Costs for AI Startups 2026 — GMI Cloud](https://www.gmicloud.ai/en/blog/how-much-do-gpu-cloud-platforms-cost-for-ai-startups-in-2026)
- [5000 CNY to USD — CurrencyRate](https://cny.currencyrate.today/convert/amount-5000-to-usd.html)
