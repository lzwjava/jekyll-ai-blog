---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warmup in LLM Training Explained
translated: false
type: note
---

**Question:** What does "warmup" mean in LLM training?

**Answer:**

Warmup means starting training with a tiny learning rate and ramping it up to the target LR over the first N steps, instead of hitting the optimizer with the full LR from step 0.

**The schedule (nanoGPT-style)**

You've seen this in `train.py`:

```python
def get_lr(it, warmup_iters=2000, max_iters=600000,
           max_lr=6e-4, min_lr=6e-5):
    # 1) linear warmup
    if it < warmup_iters:
        return max_lr * (it + 1) / (warmup_iters + 1)
    # 2) cosine decay down to min_lr
    if it > max_iters:
        return min_lr
    ratio = (it - warmup_iters) / (max_iters - warmup_iters)
    coeff = 0.5 * (1.0 + math.cos(math.pi * ratio))  # 1 → 0
    return min_lr + coeff * (max_lr - min_lr)
```

So for GPT-2-scale runs: LR goes 0 → 6e-4 linearly over ~2k steps, then cosine-decays for the rest of training.

**Why it's needed — three first-principles reasons**

1. **Adam's moment estimates are garbage early.** Adam scales updates by `m_t / (sqrt(v_t) + eps)`, where `v_t` is an EMA of squared gradients with `beta2=0.95–0.999`. At step 1, `v_t` is estimated from ~1 sample. Bias correction fixes the *expectation* but not the *variance* — the effective per-parameter LR is wildly noisy. A few unlucky large steps early can throw weights into a bad region you never recover from (or NaN outright). Warmup keeps step sizes small until `v_t` has seen enough gradients to be a meaningful estimate. This is literally the motivation for RAdam (Liu et al. 2019), which showed warmup ≈ variance reduction for Adam's adaptive LR.

2. **Sharp curvature at init.** At initialization the loss landscape near a random transformer is poorly conditioned — attention logits, LayerNorm gradients, and the embedding/unembedding produce large, badly-scaled gradients. Large early steps push you into high-curvature regions; once attention entropy collapses (some heads saturate to one-hot) it's hard to undo. Warmup lets the network gently settle into a smoother basin first.

3. **Large-batch stability.** LLM pretraining uses huge effective batch sizes (0.5M–4M tokens). Big batch → low gradient noise → you want big LR for efficiency — but big LR at init diverges. Warmup is the bridge (this is the original Goyal et al. 2017 "ImageNet in 1 hour" trick, where linear LR scaling with batch size only worked with warmup).

**Symptoms without warmup**: loss spikes or NaNs in the first few hundred steps, or a run that trains but plateaus at a permanently worse loss than the warmed-up run with identical hyperparameters.

**Practical numbers**

- nanoGPT/GPT-2 124M–760M: ~700–2000 warmup iters
- Big runs (LLaMA, DeepSeek): typically warmup over ~0.1–1% of total tokens (e.g., 2000 steps for LLaMA-2)
- Too-long warmup just wastes compute; too-short risks instability. It's one of the more forgiving hyperparameters — order of magnitude matters, exact value doesn't.

**One layer deeper: warmup is partly a patch.** Several works show you can reduce or eliminate it by fixing the underlying instability instead: better init (e.g., scaled residual init `0.02/sqrt(2*n_layer)` that GPT-2/nanoGPT already use), Pre-LN instead of Post-LN (Xiong et al. 2020 proved Post-LN has exploding gradients at init, which is *why* the original Transformer needed warmup so badly), z-loss / logit soft-capping, QK-norm, or μP-style parametrizations. Modern relevance: DeepSeek and others use **WSD (warmup–stable–decay)** schedules — warmup, then long constant LR, then short sharp decay — because it lets you resume/extend training from any checkpoint without committing to a total step count upfront, unlike cosine.

Since you're training GPT-2 760M on the MI300X: keep warmup at ~2000 iters, and if you see loss spikes early despite warmup, drop `beta2` from 0.99 to 0.95 and/or tighten grad clipping to 1.0 — those interact directly with the same early-training variance problem warmup addresses.

**References:**

- [Attention Is All You Need — original warmup schedule, §5.3](https://arxiv.org/abs/1706.03762)
- [On the Variance of the Adaptive Learning Rate and Beyond (RAdam)](https://arxiv.org/abs/1908.03265)
- [On Layer Normalization in the Transformer Architecture (Pre-LN vs Post-LN)](https://arxiv.org/abs/2002.04745)
- [Accurate, Large Minibatch SGD (Goyal et al., warmup for large batches)](https://arxiv.org/abs/1706.02677)
- [nanoGPT train.py — get_lr implementation](https://github.com/karpathy/nanoGPT/blob/master/train.py)
