---
audio: false
generated: true
image: false
lang: en
layout: post
title: Designing a Custom Midsize GPT-2 Model
translated: false
type: note
---

**Question:** Can we design and train a custom GPT-2 model with a parameter count between the small (124M) and medium (350M) sizes, and is it feasible to train such a model on a single RTX 4070?

---

**Answer:**

Yes, absolutely. The GPT-2 architecture in nanoGPT is fully configurable — you are not restricted to the four official OpenAI sizes. You simply dial in `n_layer`, `n_head`, and `n_embd` to land at any parameter count you want between 124M and 350M.

---

## How GPT-2 Sizing Works

The four standard configs in nanoGPT's `model.py` are:

| Model | n_layer | n_head | n_embd | Params |
|---|---|---|---|---|
| gpt2 | 12 | 12 | 768 | 124M |
| gpt2-medium | 24 | 16 | 1024 | 350M |
| gpt2-large | 36 | 20 | 1280 | 774M |
| gpt2-xl | 48 | 25 | 1600 | 1558M |


These are just defaults. nanoGPT's `GPTConfig` accepts arbitrary values, so you can design anything in between.

---

## Example "Middle" Configs (~200M)

There is no single canonical ~200M config, but here are three well-behaved options. The rule of thumb: `n_embd` must be divisible by `n_head`, and prefer powers-of-2-friendly numbers for GPU efficiency.

**Option A — Wider, shallower (~190M)**
```python
n_layer = 16
n_head  = 16
n_embd  = 896   # 896 / 16 = 56 head_dim (fine)
```
Estimated params: ~190M

**Option B — Balanced (~220M)**
```python
n_layer = 18
n_head  = 16
n_embd  = 896
```
Estimated params: ~215M

**Option C — Closer to medium (~260M)**
```python
n_layer = 20
n_head  = 16
n_embd  = 960   # 960 / 16 = 60 head_dim
```
Estimated params: ~255M

You can use nanoGPT's own `transformer_sizing.ipynb` notebook to get exact parameter counts for any config before committing to training.

---

## VRAM Estimation on RTX 4070 (12 GB)

A rough rule for training in bfloat16:

| Component | Memory |
|---|---|
| Model weights | ~2 bytes × params |
| Gradients | ~2 bytes × params |
| AdamW optimizer states | ~8 bytes × params |
| Activations (batch-dependent) | variable |

For a ~200M model with `batch_size=1`, `block_size=1024`, `bfloat16`:

- Weights + gradients + optimizer states ≈ 200M × 12 bytes ≈ **~2.4 GB** (base)
- Activations at `batch_size=1` add another ~3–5 GB
- **Total estimate: ~6–8 GB** → fits within 12 GB VRAM with room to spare

This is meaningfully more comfortable than trying to squeeze the 350M model (which pushes 11–12 GB even at `batch_size=1`).

---

## Recommended Config for RTX 4070

```python
# config/train_gpt2_200m_4070.py
n_layer = 18
n_head  = 16
n_embd  = 896
block_size = 1024
vocab_size = 50257

batch_size                  = 2    # micro-batch; try 4 if it fits
gradient_accumulation_steps = 240  # keeps ~0.5M effective tokens/step
dtype   = 'bfloat16'
compile = True  # torch.compile gives ~20–30% speedup on Ada

# Optional but recommended:
# gradient checkpointing (patch Block.forward) to trade ~25% speed for ~2–3x activation memory savings
# 8-bit AdamW via bitsandbytes saves ~1–2 GB on optimizer states
```

---

## Training Time Estimate

| Model | 4070 (12 GB) solo | Expected val loss |
|---|---|---|
| 124M (small) | ~1–2 weeks | ~3.0–3.1 |
| **~200M (custom)** | **~3–5 weeks** | **~2.92–3.0** |
| 350M (medium) | 1–3 months (aggressive tricks) | ~2.85–2.95 |

A ~200M custom model is the practical "sweet spot" for a single RTX 4070: it trains from scratch in a matter of weeks (not months), fits in VRAM without aggressive surgery, and gives noticeably better loss than the 124M model.

---

## Practical Recommendation

- If your goal is the **best result possible on one 4070**, train a ~200M custom model from scratch — it is the best balance of VRAM headroom, training time, and final quality.
- If you want **pretrained weights to finetune**, use `init_from='gpt2'` (124M) or `init_from='gpt2-medium'` (350M) — note there are no official OpenAI weights for a custom intermediate size, so custom intermediate configs must always be trained from scratch.

---

**References:**

- [nanoGPT model.py — official size configs](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [nanoGPT transformer_sizing.ipynb — parameter count notebook](https://github.com/karpathy/nanoGPT/blob/master/transformer_sizing.ipynb)
- [nanoGPT model parameters reference](https://www.mintlify.com/karpathy/nanoGPT/configuration/model-params)
- [llm.c discussion: reproducing GPT-2 350M](https://github.com/karpathy/llm.c/discussions/481)
