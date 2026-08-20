---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Qwen3 Query Shift: Small Loss, Stable Accuracy"
translated: false
type: note
---

Question: Why does shifting the Query source up by 0.5 layers in Qwen3-27B cause only ~2.7% quality loss, and why do the BF16 and FP8 measurements agree so closely?

Answer:

**Why the quality loss is so small (~2.7% bpb)**

The core insight is that Query representations are surprisingly stable across adjacent layers. In a transformer, the residual stream changes slowly — each layer adds a relatively small delta on top of the previous state. When you shift Q's source up by 0.5 layers (concretely: use the pre-FFN activation of layer *n* as the Q for what was layer *n*'s attention, instead of the post-FFN activation), you are feeding attention a representation that is only "half a layer stale." The residual stream at that point is already ~97% of what the full layer would produce, so attention still computes a meaningful pattern.

This also aligns with the **model dissection / model anatomy** conclusion your friend references: attention heads are reading coarse positional/semantic routing information from Q, not fine-grained transformed features. The FFN's contribution to Q's expressiveness is marginal — K and V benefit more from the full post-FFN representation because they encode the *content* being retrieved, while Q mainly encodes *what to look for*.

**Why the gain exists at all (motivation for the trade-off)**

By sourcing Q from *before* the FFN in layer *n*, you can pipeline attention and FFN in parallel:

```
Layer n:  [Attention(Q=x_pre, K/V=x_pre)] ∥ [FFN(x_pre)]
                    ↓                              ↓
          attention output            ffn output   → sum → x_{n+1}
```

This is the same idea as in **Parallel Attention + FFN** architectures (e.g., PaLM, some GPT-J variants). The ~2.7% quality cost buys you real wall-clock latency reduction on hardware where attention and FFN can overlap.

**Why BF16 and FP8 measurements agree so closely (+0.0181 vs +0.0191 bpb)**

| Factor | Effect |
| --- | --- |
| The perturbation is architectural, not numerical | The Early-Q shift introduces a structural bias; FP8 quantization noise is largely orthogonal to it |
| FP8 already degrades baseline slightly | Both baseline and Early-Q degrade proportionally, so the *delta* is preserved |
| SGLang's FP8 path is well-calibrated for Qwen3 | Activation outliers in Q/K/V are handled by per-tensor or per-channel scaling, keeping relative differences stable |
| 24552 evaluation positions is large enough | Measurement variance is low; the two setups differ only in dtype/harness, not in the structural change being measured |

The near-perfect replication (+2.66% vs +2.68%) is actually strong evidence that the effect is a **clean architectural signal**, not an artifact of either evaluation setup. If numerical precision were interacting with the perturbation, you would expect larger divergence between BF16 and FP8 deltas.

**Bottom line**

The small loss confirms that Q is a low-sensitivity input — transformers can tolerate stale Q with minimal routing error, making Early-Q a practical knob for trading a small quality cost for compute parallelism, without any fine-tuning.

References:

- [PaLM: Scaling Language Modeling with Pathways (parallel attention+FFN)](https://arxiv.org/abs/2204.02311)
- [GPT-J architecture (parallel layers)](https://github.com/kingoflolz/mesh-transformer-jax)
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)
