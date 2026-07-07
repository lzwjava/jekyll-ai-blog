---
audio: false
generated: true
image: false
lang: en
layout: post
title: Single H200 Pretraining Feasibility Analysis
translated: false
type: note
---

**Question:** For pretraining a GPT-3 style model on a single H200, is FineWeb-Edu at 25B tokens sufficient, and is the pasted analysis correct?

**Answer:**

The pasted answer has the right overall shape (data quality > GPU, mix in code/books, don't attempt 175B) but contains two significant errors and a few outdated framings worth fixing before you act on it.

## Error 1: The GPT-3 / Chinchilla claim is backwards

The answer says GPT-3's `175B params : 300B tokens` "roughly follows Chinchilla scaling: tokens ≈ 20 × parameters." That's wrong by more than an order of magnitude:

```
Chinchilla-optimal for 175B:  20 × 175B = 3.5T tokens
GPT-3 actually trained on:              300B tokens  (~1.7 tokens/param)
```

The entire point of the Chinchilla paper (Hoffmann et al., 2022) was that GPT-3 and Gopher were *severely undertrained* — that's why 70B Chinchilla beat 280B Gopher. GPT-3 predates Chinchilla and follows the older Kaplan scaling laws, which over-weighted parameters. Also a small nuance: the ~500B table is the corpus size; GPT-3 trained on 300B tokens with weighted sampling (Common Crawl seen ~0.44 epochs, Wikipedia ~3.4 epochs).

The per-size token recommendations (1B → 20B, 7B → 140B) are correct *as Chinchilla-optimal points*, but note Chinchilla is compute-optimal, not quality-optimal. Modern practice massively overtrains for inference economics: Llama 3 8B saw 15T tokens (~1,900 tokens/param, ~95× Chinchilla). For a learning run, Chinchilla-optimal is the right target; for a usable model, it's a floor.

## Error 2: Single-H200 wall-clock estimates are off by ~20×

"7B on 140B tokens: days" on one H200 is fantasy. Do the 6ND math:

```python
def train_days(params, tokens, mfu=0.40, peak_flops=989e12):  # H200 BF16 dense
    return 6 * params * tokens / (mfu * peak_flops) / 86400

train_days(0.76e9, 25e9)    # ≈ 3.3 days   (your GPT-2 760M scale)
train_days(1.3e9,  26e9)    # ≈ 6 days
train_days(7e9,   140e9)    # ≈ 172 days   ← "days" in the answer, actually ~6 months
train_days(13e9,  260e9)    # ≈ 590 days
```

40% MFU is a realistic single-GPU number for a well-tuned Llama-style decoder with FlashAttention and `torch.compile`; you might hit 45–50%, which doesn't change the conclusion. On **one H200, your practical ceiling is ~1–2B params at Chinchilla-optimal tokens**. This is exactly why Karpathy's nanochat targets an 8×H100 node for a ~$100–1000 run — a single-GPU 7B pretrain is not a sane project. The suggested first run (1.3B, 50B tokens) is fine, but budget ~11 days, not hours.

## So: is 25B tokens of FineWeb-Edu enough?

Enough for what:

- **≤1.3B param model, Chinchilla-optimal:** yes. 25B tokens is compute-optimal for ~1.25B params. For your 760M-class runs it's actually a bit more than optimal (20 × 0.76B ≈ 15B).
- **Anything ≥3B, or a model you'd overtrain for quality:** no. Pull `sample-100BT` or `sample-350BT` from the same HF repo — FineWeb-Edu's full set is ~1.3T tokens, so scaling up is a config change, not a data hunt.

One correction to the "FineWeb-Edu is incomplete" section: at ablation scale (≤2B params), FineWeb-Edu *alone* is competitive — it was built precisely by showing it beats mixed web corpora on MMLU/ARC-style benchmarks. The proposed 60/15/10/5/5/5 mix is a reasonable modern recipe, but the missing ingredients (code, math) mainly matter for downstream capabilities you probably won't measure at 1.3B anyway. For your first H200 runs, FineWeb-Edu only, single source, is the cleaner experiment. Add StarCoder/FineMath when you scale past ~3B or start caring about eval breadth.

## Smaller corrections

**uint16 tokenization** (2 bytes/token) only works while vocab < 65,536. GPT-2/NeoX (~50K) fits — this is what nanoGPT/nanochat do. If you switch to a Llama 3-style 128K vocab, you need uint32 and storage doubles. The answer's 500GB-for-250B-tokens figure silently assumes the small vocab.

**Storage math is roughly right** otherwise: FineWeb-Edu parquet runs ~3–4 bytes/token compressed, so 25B ≈ 100GB checks out, and 1–2TB NVMe is the right provisioning for a 100B-token run (raw parquet + tokenized shards + checkpoints; a 1.3B model's Adam checkpoint alone is ~16GB, and you'll keep several).

**175B memory numbers** are directionally right (weights + FP32 master + Adam m,v ≈ 16 bytes/param ≈ 2.8TB before activations) — correct conclusion, don't attempt it.

## What I'd actually run

Given you've already done GPT-2 760M on MI300X, the H200 run that teaches you the most per dollar:

```
Model:     1.3B Llama-style (RoPE, SwiGLU, RMSNorm, no biases) — don't replicate literal GPT-3 arch
Data:      FineWeb-Edu sample-100BT, take 26B tokens (Chinchilla) — single source, clean ablation
Tokenizer: GPT-NeoX or train your own 32K BPE (fits uint16)
Precision: BF16 + FlashAttention + torch.compile, target ≥40% MFU
Wall time: ~6 days @ 40% MFU
Cost check: ~$3-4/hr H200 → ~$500. Compare against renting 8×H100 for ~1 day at similar cost —
           the node is often the better deal if you want iteration speed.
```

Then the interesting second experiment isn't "scale to 7B" (172 GPU-days — rent a node instead); it's **overtraining the 1.3B to 100B+ tokens** and watching where the loss curve flattens versus the Chinchilla point. That's the scaling-law intuition that transfers directly to your DeepSeek v4 MoE work.

**References:**

- [Language Models are Few-Shot Learners (GPT-3 paper, Table 2.2 for the data mix and sampling weights)](https://arxiv.org/abs/2005.14165)
- [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)
- [FineWeb-Edu dataset (sample-10BT / 100BT / 350BT / full ~1.3T)](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- [The FineWeb technical report — includes the FineWeb-Edu ablations](https://arxiv.org/abs/2406.17557)
- [karpathy/nanochat — reference for single-node full-pipeline training budgets](https://github.com/karpathy/nanochat)
