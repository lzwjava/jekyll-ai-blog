---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI's Changing Landscape
translated: false
type: note
---

Question: What's the long-term trajectory of AI tech — what's structurally changing vs what's invariant?

Answer:

**Invariant (won't change):**

1. **The objective function.** Next-token cross-entropy + gradient descent is still the substrate for everything — reasoning models, agents, RLHF/RLVR. Nobody has replaced this. RL post-training is just reshaping the same autoregressive distribution with a different loss signal (reward instead of NLL).

2. **Bitter lesson holds, but the resource split changed.** Compute + general methods > hand-crafted priors is still true. What changed is compute now splits three ways instead of one: pretraining compute, post-training/RL compute, and test-time compute. Together, pretraining scaling, post-training scaling and test-time scaling reflect how the field has evolved with techniques to use additional compute in increasingly complex use cases. The power-law shape is invariant; where you spend the compute isn't.

3. **Transformer bones stay.** Attention + FFN blocks, whether dense or MoE, are still the substrate. MLA/GQA are compression tricks on the same skeleton, not a replacement.

**What's actually changing:**

1. **Pretraining scaling is hitting a data ceiling, not a math ceiling.** Epoch AI projects the stock of quality-filtered public text will be fully utilized somewhere between 2026 and 2032 under current training rates, with frontier labs already facing constraints on unique token budgets. Muennighoff et al. showed repeated tokens don't dilute linearly — their value decays exponentially per repetition with a learnable half-life. This is why "just add more internet text" stopped being the free lunch it was in 2020-2023.

2. **Compute moved from train-time to test-time.** Models like o1, o3, DeepSeek-R1, and Gemini Flash Thinking use chain-of-thought reasoning at inference — thinking longer before answering — distributing cognitive work across inference steps instead of encoding it all into weights during training. This is the single biggest architectural shift of the last 18 months. It directly rewards your hardware situation — a small, well-trained model + more inference-time search beats a bigger dense model you can't afford to train.

3. **Post-training now obeys its own scaling law.** The relationship between test loss, compute, and data during RL post-training follows a predictive power law across both base and instruction-tuned models — but with a latent saturation trend: larger models achieve higher learning efficiency, yet returns diminish as scale grows. RLVR (verifiable rewards — math, code, unit tests) is becoming the dominant lever precisely because raw text is drying up and reward signal from executable/verifiable tasks is not.

4. **Sub-scaling / density effects are real.** Recent research studying over 400 models found performance improvements decelerate faster than standard scaling laws predict as datasets grow very large — the marginal uniqueness of each new sample decreases with data density, causing redundancy and diminishing returns that compound. This is why Falcon 180B lost to Llama 3 8B a year later — architecture/data quality/post-training now beats raw param count.

5. **Sparsity (MoE) is the mainstream answer to "compute is capped but you still want more capacity."** Active-param-only inference is why DeepSeek, Kimi, and most 2026 frontier releases are MoE by default rather than dense. This is exactly the axis you're already building toward.

**Bottom line for your build**: pretraining a bigger dense model from scratch on a 4070 was never the play, and it's now not the play for anyone (even labs are data-bound there). The frontier moved to: small efficient base model → MoE for capacity-per-FLOP → RLVR/test-time compute for capability without more pretraining tokens. Your nanoGPT-MoE plan lines up with where the field's actual constraint is, not where it was in 2022.

References:

- [AI Scaling Laws Guide Billions in Compute Spend: Weng Reveals the Cracks](https://www.techtimes.com/articles/319204/20260627/ai-scaling-laws-guide-billions-compute-spend-weng-reveals-cracks.htm)
- [LLM Scaling Laws: Analysis from AI Researchers](https://aimultiple.com/llm-scaling-laws)
- [AI Scaling Laws Are Breaking Down: What It Means for AI Builders](https://www.mindstudio.ai/blog/ai-scaling-laws-breaking-down-what-it-means-for-builders)
- [LLM Scaling Laws Explained: Will Bigger AI Models Always Win? (2026)](https://www.buildfastwithai.com/blogs/llm-scaling-laws-explained)
- [How Scaling Laws Drive Smarter, More Powerful AI — NVIDIA Blog](https://blogs.nvidia.com/blog/ai-scaling-laws/)
