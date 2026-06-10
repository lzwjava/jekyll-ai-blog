---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat's val/bpb metric explained
translated: false
type: note
---

**Question:** In nanochat, what does the `val` section (with 1 chart) and the `val/bpb` metric mean?

**Answer:**

What you're seeing is a wandb metric namespace. nanochat logs metrics with `/`-separated prefixes — `train/...`, `val/...`, `core/...` — and wandb groups them into collapsible sections. So `val (1)` just means: the **validation** section, containing **1** chart, and that chart is `val/bpb`.

`bpb` = **bits per byte**, the validation loss in tokenizer-invariant units. Karpathy monitors val_bpb (validation loss in vocab-size-invariant units of bits per byte) as a function of step to see if a code change helped, and it's the headline metric on the nanochat leaderboard.

## Why not just report cross-entropy loss?

Because raw CE is a per-*token* quantity, and tokens are an artifact of your tokenizer. A 65k-vocab tokenizer packs ~4–5 characters per token; a 32k one packs fewer. Same model quality, different per-token loss. Bits per byte normalizes the loss on each token by the number of bytes of that token, making the metric tokenizer-invariant — so you can compare a d12 run against a d26 run, or your custom-tokenizer experiment against baseline, fairly.

The information-theoretic reading: it's how many bits your model needs to compress one byte of unseen text. Random guessing over bytes = 8.0 bpb. A nanochat d20 lands around ~0.7–0.8 val bpb; frontier models are well below that. Lower = better compression = better next-token prediction.

## The math

Cross-entropy loss from `F.cross_entropy` is in **nats per token**. Convert:

$$
\text{bpb} = \frac{\sum_i \text{nll}_i}{\ln(2) \cdot \sum_i \text{bytes}(t_i)}
$$

where `bytes(t_i)` is the UTF-8 byte length of token `t_i`'s string. Two steps: nats → bits (divide by ln 2), per-token → per-byte (weight each token's NLL by its byte count and divide by total bytes).

## The actual implementation (~20 lines)

This is the core of nanochat's `evaluate_bpb` (simplified):

```python
import math, torch

@torch.no_grad()
def evaluate_bpb(model, loader, steps, token_bytes):
    # token_bytes: LongTensor [vocab_size], UTF-8 byte length of each token's string
    total_nll, total_bytes = 0.0, 0
    for _ in range(steps):
        inputs, targets = next(loader)
        nll = model(inputs, targets, loss_reduction='none')  # [B, T] per-token NLL in nats
        mask = targets >= 0                                   # drop ignore_index padding
        nb = token_bytes[targets[mask]]                       # bytes per target token
        total_nll  += (nll[mask] * 1.0).sum().item() * 0 + (nll[mask]).sum().item()
        total_bytes += nb.sum().item()
    return total_nll / math.log(2) / total_bytes
```

Note the subtlety: the precise version weights correctly by summing raw NLL over tokens and dividing by total bytes (equivalent to a byte-weighted average). The `token_bytes` lookup table is built once from the tokenizer: `token_bytes[i] = len(tokenizer.decode([i]).encode('utf-8'))`.

Quick sanity check connecting it to numbers you already know: if your tokenizer averages 4.0 bytes/token and val loss is 2.2 nats/token, then bpb ≈ 2.2 / ln(2) / 4.0 ≈ **0.79**.

## Why Karpathy uses it as the primary dial

val bpb is smooth and low-noise compared to task-based evaluations like CORE/MMLU, which are step-functions at small scale. So the workflow is: tweak architecture → rerun d12 → watch `val/bpb` vs step (and vs wall-clock / FLOPs) in wandb. CORE is run sparsely (it's expensive); bpb is the fast inner-loop signal. His newer `autoresearch` repo uses val_bpb as the sole metric for fixed 5-minute training runs, precisely because it's vocab-size-independent so architectural changes compare fairly.

One caveat to keep in mind for your own experiments: bpb is only *fully* comparable across tokenizers if evaluated on the same byte stream. If two tokenizers chunk the validation set into different token sequences, you're still measuring compression of the same underlying bytes — which is exactly the point.

**References:**

- [karpathy/nanochat — README](https://github.com/karpathy/nanochat)
- [nanochat walkthrough — Discussion #1](https://github.com/karpathy/nanochat/discussions/1)
- [BPB: a tokenizer-agnostic way to measure LLMs](https://dipkumar.dev/posts/llm/bits-per-byte/)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
