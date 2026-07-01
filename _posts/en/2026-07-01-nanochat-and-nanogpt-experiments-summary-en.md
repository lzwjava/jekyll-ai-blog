---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat and nanoGPT Experiments Summary
translated: false
type: note
---

Question: Give me a complete summary of my nanochat and nanoGPT experiments and what I should do next.

---

## nanochat — Training Runs

### d8 (~40M params) — First pass, proof of concept

**Config:** depth=8, batch=32,768, seq_len=1,024, 5k iterations
**Data:** ~164M tokens from fineweb-edu shards (8 shards, ~2B chars)
**Pipeline:** pretrain → SFT (Karpathy's identity_conversations) → eval

Checkpoints at `base_checkpoints/d8/` steps 1k and 5k. The SFT step ran as well (chatsft_checkpoints/d8/).

**Results:** Language modeling loss ~3.0, ARC-Easy 25.6%, MMLU 25.3%, GSM8K/HumanEval 0%. This is expected — 40M params at 164M tokens is roughly 4x data-to-params ratio (Chinchilla would say ~20x), so the model learns language structure but has zero reasoning capability.

### d12 (286M params) — The serious effort

**Config:** depth=12, dim=768, heads=6, seq_len=2,048, batch=65,536 tokens/step

**Phase 1 — Fresh 10k (MLflow tracked):** `run_d12_10k_mlflow.sh`. ~655M tokens. Validation BPB: 0.9349 (~val loss ~2.87). Sample output shows the model generating interleaved repetitions ("The capital of France is located in the south of the country. It is the capital of the French Republic") — it's learned surface structure but hasn't seen enough data for factual binding.

**Phase 2 — Chinchilla run (87k→200k steps):** `run_rtx4070_chinchilla.sh` planned 87k steps (~5.7B tokens), then `run_d12_130k.sh` resumed from 87k to 130k. Actually went further:

Checkpoints every 10k in `base_checkpoints/d12/`:

| Step | Date |
|------|------|
| 130k | Jun 7 |
| 140k | Jun 9 |
| 150k | Jun 9 |
| 160k | Jun 10 |
| 170k | Jun 10 |
| 180k | Jun 10 |
| 190k | Jun 10 |
| 200k | Jun 10 |

Total ~13.1B tokens seen (200k × 65,536). Each checkpoint 792MB (model) + 1.2GB (optimizer). Loss plateaus at ~3.0 — the model is still learning but the loss curve is flattening, which either means (a) data diversity is exhausted, (b) learning rate schedule needs adjustment, or (c) the 286M capacity is saturated on this data distribution.

**Phase 3 — Eval results (at ~10k fresh model):**

- ARC Easy: 25.63% — near random (25%)
- ARC Challenge: 25.77% — near random
- MMLU: 25.26% — near random (25%)
- GSM8K: 0.00% — no arithmetic reasoning
- HumanEval: 0.00% — no code generation

The eval was run on the fresh 10k-step model. The 200k-step model would likely score slightly better but still far from useful — these benchmarks need >10x more data for a 286M model.

### d4 distributed test

Tiny 20-step run across 2 ranks. CPU/DDP test, not meaningful beyond validating the distributed training path.

### d24 MI300X (~760M params)

**Config:** depth=24, dim=1,536, heads=12, batch=524,288, seq_len=2,048, 29k steps planned
**Data:** ClimbMix-400B, ~15.2B tokens target

Ran on AMD MI300X (192GB HBM3). Multiple config variants tested (FP8, FA2+FP8). Logs at `run_mi300x_d24.log`, `run_mi300x_d24_fa2_fp8.log`, `run_mi300x_d24_fp8.log`. The `run_mi300x_d24_pretrain.sh` script is the pretrain-only variant.

This was your most ambitious run — 760M params on a cloud GPU at $2/hr.

---

## nanoGPT — Training Runs

All based on Karpathy's original nanoGPT with GPT-2 124M architecture (n_layer=12, n_head=12, n_embd=768) unless noted.

### fineweb-gpt3 (124M, 10B token target)

**Config:** `config/train_fineweb_gpt3.py` — batch=4 × grad_accum=128 = 524,288 tokens/step effective, max_iters=19,073
**Data:** `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B`

Training stopped at ~15,180 steps (train loss 3.05, val loss 3.03) — the train.log shows `Command 'python3.13' not found` error. The actual run used the wrong Python binary. It reached ~7.9B tokens before crashing. Checkpoint saved at that point.

### fineweb (124M)

Standard run with same architecture. Checkpoint at `out-fineweb/ckpt.pt` (~1.4GB). Appears to be a completed single-pass run, but train.log wasn't kept.

### github-code-124m (124M, 14B token target)

**Config:** `config/train_github_code_124m.py` — batch=32,768 effective, max_iters=427,000
**Data:** `/mnt/data/zz/datasets/github-code-tok/` (27GB of tokenized GitHub code)

Checkpoint at `out-github-code-124m/ckpt.pt` (~1.4GB). The config targets 14B tokens. Need to check how far training progressed.

### sec-edgar-124m (124M, 1.55B token target)

**Config:** `config/train_sec_edgar_124m.py` — batch=32,768 effective, max_iters=47,400 (1 epoch)
**Data:** `/mnt/data/zz/datasets/sec-edgar-tok/` (3.1GB of tokenized SEC filings)

Checkpoint at `out-sec-edgar-124m/ckpt.pt` (~1.4GB). Should have completed ~1 epoch.

### gpt2-200m (200M params)

Larger architecture. Checkpoint at `out-gpt2-200m/ckpt.pt` (~2.5GB). train.log is empty (0 bytes) — either the run crashed immediately or logged elsewhere.

### Toy runs

`out-helloworld` (random init), `out-shakespeare` (empty), `out-shakespeare-char` (char-level GPT on Shakespeare), `out-wikipedia` (Wikipedia pretrain, 362MB checkpoint). These are the original nanoGPT demo runs.

### Available datasets

| Dataset | Size | Tokens |
|---------|------|--------|
| github-code-tok | 27GB | ~7-8B tokens |
| sec-edgar-tok | 3.1GB | ~1.5B tokens |
| edu_fineweb100B | ~15GB | split across shards |
| openwebtext | varies | ~9GB |

---

## What's Actually Interesting Right Now

### 1. nanochat d12 — Finish the eval loop

You have 8 checkpoints from 130k to 200k but never ran a proper eval sweep. The d12 training reached 200k steps (~13B tokens) which is roughly 45x data-to-params ratio — below Chinchilla-optimal (~20x) for 286M, so the model is technically under-trained for its capacity. But the flat loss curve (~3.0) suggests diminishing returns.

**Do this first:** Run `scripts.base_eval` on the 200k checkpoint to see if loss improvement translates to any benchmark gain over the 10k checkpoint:

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python -m scripts.base_eval --device-batch-size=8 --model-tag=d12-fresh
```

### 2. nanochat d12 — SFT the 200k checkpoint

The 286M d12 model has never been SFT'd. The d8 SFT proved the pipeline works. SFT would give you a chat-capable local model at 286M.

```bash
python -m scripts.chat_sft --max-seq-len=2048 --device-batch-size=8 --total-batch-size=32768 --run=rtx4070-d12-sft
```

This is the highest-leverage action: an SFT'd 286M chat model would be useful for fast local inference, agent sub-roles, and prompt experimentation without API costs.

### 3. nanoGPT github-code-124m — check training status

The 27GB GitHub code dataset is your largest curated dataset. If the 427k-step run completed, you have a 124M code model. If not, resume it. This directly feeds into your agent tooling work (ww, iclaw).

### 4. nanoGPT fineweb-gpt3 — resume from 15k

Trivially fixable — the run died because `python3.13` doesn't exist. Resume with the correct Python (`.venv/bin/python` or `python3.11`). Only ~4k steps remaining to hit 19,073.

### 5. Compare nanochat vs nanoGPT on the same data

Both frameworks can train GPT-2 124M architectures. You have the same github-code dataset tokenized for both frameworks. Benchmark training speed (tokens/sec) between nanochat and nanoGPT for the same model config. This answers: which framework should you use for future experiments?

### 6. GGUF quantization → local serving

The sec-edgar-124m checkpoint is small enough to convert to GGUF for llama.cpp inference. You have llama.cpp built at `~/projects/llama.cpp/build/bin/`. This gives you a locally-served model for SEC EDGAR tasks without API calls.

```bash
cd /mnt/data/nanoGPT
python3 scripts/convert_hf_to_gguf.py --outfile out-sec-edgar-124m/ggml-model-q4_0.gguf --model out-sec-edgar-124m/ckpt.pt
```

### 7. RL/GRPO on 124M is feasible but premature

You have TRL skills and the PEFT toolchain. A 124M model fine-tuned with GRPO on GSM8K would be a good learning exercise — you'd see the RL reward shaping dynamics in real time on a model you trained. But the base model needs to be in a reasonable loss regime first (~3.0 on 124M with 10B tokens is still high for RL to work well).

---

**Bottom line:** Highest ROI per hour is (1) eval sweep on d12, (2) SFT the d12 200k checkpoint. That gives you a working chat model you can evaluate, compare, and use. Then (3) assess github-code-124m status.
