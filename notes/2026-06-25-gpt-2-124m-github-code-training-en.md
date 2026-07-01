---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 124M GitHub Code Training
translated: false
type: note
---

**Question:** Based on the training note and config/scripts in `lzwjava/zz`, provide a comprehensive technical summary of the GPT-2 124M GitHub Code training run.

---

## GPT-2 124M on GitHub Code — Comprehensive Training Summary

### 1. Pipeline Overview

Three-stage pipeline, all custom-built in `lzwjava/zz`:

```
codeparrot/github-code (HuggingFace)
        ↓ download_github_code.py
   38 of 1126 parquet shards (~27 GB)
        ↓ tokenize_github_code.py
   282 .npy shards (GPT-2 BPE via tiktoken)
   140 train shards + 1 val shard
        ↓ train.py + config/train_github_code_124m.py
   nanoGPT training loop, 427k steps
```

**Dataset:** `codeparrot/github-code` is a large-scale open-source code dataset. You pulled 38/1126 parquet shards, covering ~14B tokens across 140 train shards. The val shard is 1 file — likely a held-out language or shard index, giving a clean OOD-ish validation signal.

---

### 2. Model Architecture

Standard GPT-2 124M — no modifications:

| Hyperparameter | Value |
| --- | --- |
| `n_layer` | 12 |
| `n_head` | 12 |
| `n_embd` | 768 |
| `block_size` | 1024 |
| `dropout` | 0.0 |
| `bias` | False |
| Total params | ~163M (124M non-embedding) |

The param count difference (124M named vs 163M total): embedding table is `50257 × 768 ≈ 38.6M` params, not counted in the "124M" label. The forward pass is a standard causal transformer: token + positional embeddings → 12 decoder-only attention blocks → LM head (weight-tied to embedding). `bias=False` follows the GPT-3 paper's finding that biases are unnecessary at scale.

---

### 3. Training Configuration

**Batch geometry:**

```
micro_batch = 4 sequences × 1024 tokens = 4,096 tokens
grad_accum  = 8
effective_batch = 4,096 × 8 = 32,768 tokens/step
```

32,768 tokens/step is the same effective batch size Karpathy uses in the nanoGPT Shakespeare/OpenWebText runs — a solid choice for a single GPU.

**Optimizer (GPT-3 style AdamW):**

```python
lr            = 6e-4        # peak
min_lr        = 6e-5        # 10× decay via cosine schedule
warmup_iters  = 2000        # linear warmup
max_iters     = 427000
lr_decay_iters = 427000     # full cosine decay over entire run
weight_decay  = 0.1
beta1, beta2  = 0.9, 0.95  # GPT-3 defaults
grad_clip     = 1.0
```

The cosine decay runs the full 427k steps — LR hits `min_lr` right at the end, which is the standard approach (no cooldown phase). This is exactly what GPT-3/Chinchilla-style runs do.

**Chinchilla framing:**
Chinchilla optimal for 124M params → ~2.5B tokens. You trained on **14B tokens**, which is ~5.6× over-compute relative to the naive Chinchilla ratio. This is intentional for inference efficiency — an overtrained smaller model runs faster at serving time (the "Llama philosophy"). But it also means diminishing gradient signal late in training, which is why you see val_loss *increase* after ~70k steps.

---

### 4. Hardware & Throughput

| Metric | Value |
| --- | --- |
| GPU | RTX 4070 12GB |
| VRAM used | ~5,050 MiB |
| Power draw | ~208W |
| Temperature | ~65°C |
| Step time | ~636 ms/step avg, 621 ms steady |
| Throughput | ~51,900 tokens/sec |
| MFU | **14.44%** |

**MFU analysis:** Model FLOP Utilization of 14.44% on an RTX 4070 is typical for a single consumer GPU running nanoGPT with `torch.compile`. The RTX 4070's theoretical BF16 throughput is ~165 TFLOPS. GPT-2 124M forward+backward is ~`6 × N × D = 6 × 14B × 163M ≈ 13.7 × 10^18` total FLOPs over the run. The gap from peak MFU is explained by:

- Memory bandwidth saturation (activations, optimizer states)
- Python overhead between compiled steps
- eval/checkpoint I/O every 1000 steps

`torch.compile` with BF16 is doing the heavy lifting here. Without it you'd likely be at 8-10% MFU.

---

### 5. Loss Curve & Overfitting Analysis

| Step | val_loss | Notes |
| --- | --- | --- |
| 0 | 10.87 | Random init (ln(vocab) ≈ ln(50257) ≈ 10.8 ✓) |
| 14k | 5.87 | Fast early descent |
| 25k | ~3.6 | Syntactic structure emerging |
| 70k | 2.08 | **Best generalization** |
| 325k | 2.79 | Overfitting creeping in |
| 427k | 3.47 | Final checkpoint (degraded) |

The loss *increasing* from step 70k to 427k is the key signal. The saved `ckpt.pt` is the final step, not the best val_loss — you'd want to reload the checkpoint from around step 60-80k for the best model. A `best_val_loss` checkpoint-save strategy (save only when val_loss improves) would have caught this.

**Why does val_loss increase despite training loss decreasing?**
Classic overfitting + distribution shift from LR decay:

- As LR decays via cosine toward 6e-5, the optimizer takes smaller steps
- The model increasingly memorizes the exact token sequences in the 140 train shards
- The 1 val shard is diverging from what the model learned — the model is fitting the training distribution too tightly
- With `dropout=0.0`, there's no regularization beyond weight decay

The divergence at ~5.6× Chinchilla confirms: at this dataset size, the model was saturated around step 70k. The remaining 357k steps were gradient descent against memorization, not generalization.

---

### 6. Total Compute Budget

```
Total tokens: 14B
Compute (FWD+BWD): ~6 × 14B × 163M = 1.37 × 10^19 FLOPs
Wall time: 75.4 hours
GPU-hours: 75.4 GPU-hours on RTX 4070
RTX 4070 TDP: 200W, actual: 208W
Energy: 75.4h × 0.208 kW ≈ 15.7 kWh
```

Compare to GPT-2's original training: OpenAI used 256 TPU v3s for GPT-2 1.5B. You trained 124M on a single consumer GPU in 3 days. The relative cost is illustrative of how much compute has democratized.

---

### 7. What the Model Actually Learned

At val_loss ~2.08 (best), the model is generating code with:

- Correct indentation structure (Python, JavaScript patterns)
- Plausible function signatures and variable names
- Basic control flow (`if/else`, `for`, `return`)

At val_loss 3.47 (final), generation quality is actually *worse* on unseen code despite having seen more training steps — the distribution gap between the model's internalized training data and the val shard is real.

---

### 8. Lessons / What to Do Next

**Immediate fix for the current run:**

```python
# Add to train.py: save checkpoint only when val_loss improves
if val_loss < best_val_loss:
    best_val_loss = val_loss
    torch.save(checkpoint, 'ckpt_best.pt')
```

**For the next run — fix the overfitting:**

1. **Early stopping at step ~80k** — you have 14B tokens but the model saturates at ~2.5B (Chinchilla). Train to 80k steps (~2.6B tokens) with the same LR schedule compressed.

2. **Add dropout** — `dropout=0.1` will slow overfitting at the cost of ~5% throughput.

3. **More val diversity** — 1 val shard is a weak signal. Use 3-5 different language shards as val to catch language-specific overfitting.

4. **Scale up** — the AMI MI300X you used for GPT-2 760M can train this 124M to Chinchilla-optimal in ~6-8 hours. Or use it to train a 760M on this same 14B token dataset: `6 × 14B × 760M ≈ 6.4 × 10^19 FLOPs` — doable in ~12-15h on the MI300X vs months on 4070.

5. **Evaluate properly** — perplexity on HumanEval snippets or pass@k on simple completions would give a concrete code quality metric beyond val_loss.

---

**Bottom line:** Clean end-to-end run. 75 hours, 14B tokens, consumer hardware, custom pipeline. The real win is the infrastructure — download → tokenize → train → checkpoint works. The model peaked at step ~70k (val_loss 2.08) and the late-stage degradation is expected from training 5.6× past Chinchilla on a fixed dataset with no regularization. Next run: early stopping + compressed schedule = better model in 1/5 the time.
