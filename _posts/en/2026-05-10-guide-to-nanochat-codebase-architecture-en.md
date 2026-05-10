---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guide to nanochat Codebase Architecture
translated: false
type: note
---

Now I have a comprehensive understanding of the codebase. Here is the guide:

---

nanochat Codebase Guide
========================

nanochat (by Andrej Karpathy) is a minimal, end-to-end LLM training harness that covers all major stages: tokenization, pretraining, SFT, RL, evaluation, inference, and a ChatGPT-like web UI. The entire philosophy is: one dial (`--depth`) controls model size, everything else auto-derives.

---

1. ARCHITECTURE OVERVIEW
-------------------------

The project has 4 directories:

```
nanochat/     -- Core library (model, data, optimizers, engine)
scripts/      -- Executable entry points (train, eval, chat)
tasks/        -- Evaluation task definitions (MMLU, GSM8K, etc.)
runs/         -- Shell scripts for full training pipelines
```

The training pipeline flows as:

  Tokenizer Training -> Base Pretraining -> SFT Finetuning -> RL (optional) -> Chat

All intermediate artifacts go to `~/.cache/nanochat/` (overridable via `$NANOCHAT_BASE_DIR`).

---

2. CORE LIBRARY (`nanochat/`)
-----------------------------

**gpt.py** -- The GPT Transformer model

  - `GPTConfig` dataclass: sequence_len, vocab_size, n_layer, n_head, n_kv_head, n_embd, window_pattern
  - `GPT(nn.Module)`: The full model. Key architectural choices:
    * Rotary position embeddings (no learned positional embeddings)
    * QK normalization after rotary
    * Untied token embedding (`wte`) and output projection (`lm_head`)
    * ReLU^2 (squared ReLU) activation in MLP
    * RMSNorm (no learnable params in norm)
    * No bias in any linear layer
    * Group-Query Attention (GQA): n_kv_head <= n_head for efficient inference
    * Per-layer learnable scalars: `resid_lambdas` (residual scaling) and `x0_lambdas` (initial-embedding blending)
    * Smear: mixes previous token's embedding into current position (cheap bigram info)
    * Backout: subtracts mid-layer residual before final norm to remove low-level features
    * Value Embeddings (ResFormer-style): alternating layers get a learned value embedding, gated per-head
    * Logit softcapping (15.0) to prevent extreme logits
    * Vocab padding to 64 for DDP/tensor core efficiency
    * Sliding window attention pattern: e.g. "SSSL" = 3 short + 1 long, tiled across layers
  - `init_weights()`: Careful init scheme (uniform for weights, zeros for projections, normal for embeddings)
  - `setup_optimizer()`: Returns mixed Muon+AdamW optimizer with separate param groups and LR scales
  - `forward()`: Full forward pass. Handles both training (targets given) and inference (kv_cache)
  - `generate()`: Naive autoregressive generation (no KV cache, for testing)

**engine.py** -- Efficient inference engine

  - `KVCache`: Pre-allocated cache for Flash Attention 3 (B, T, H, D layout, not B, H, T, D)
  - `Engine`: Wraps model + tokenizer. Uses prefill-then-decode strategy:
    * Batch-1 prefill of prompt -> clone KV cache for N samples -> parallel decode
  - `RowState`: Per-row tracking for tool use state machine (Python REPL)
  - `use_calculator()`: Safe eval for Python tool calls (math expressions + `.count()`)
  - Supports `<|python_start|>` / `<|python_end|>` / `<|output_start|>` / `<|output_end|>` tokens for tool use

**flash_attention.py** -- Unified Flash Attention interface

  - Auto-detects FA3 on Hopper (sm90) GPUs, falls back to PyTorch SDPA everywhere else
  - Exports `flash_attn` module as drop-in replacement: `flash_attn_func()` and `flash_attn_with_kvcache()`
  - SDPA fallback handles sliding window, GQA, and KV cache management manually

**optim.py** -- Mixed Muon + AdamW optimizer

  - `adamw_step_fused`: `@torch.compile` fused AdamW step (weight_decay -> momentum -> bias_correction -> update)
  - Muon optimizer: Newton-Schulz iteration for orthogonalization + Polar Express sign method + NorMuon variance reduction
  - `MuonAdamW`: Single-GPU version. `DistMuonAdamW`: Distributed version with all-reduce across ranks
  - Matrix parameters (attention + MLP weights) -> Muon; embeddings, lm_head, scalars -> AdamW

**tokenizer.py** -- BPE Tokenizer

  - Two backends: `HuggingFaceTokenizer` (train+inference) and `RustBPETokenizer` (rustbpe training + tiktoken inference)
  - 9 special tokens: `<|bos|>`, `<|user_start/end|>`, `<|assistant_start/end|>`, `<|python_start/end|>`, `<|output_start/end|>`
  - `render_conversation()`: Converts chat-format dicts -> token ids + loss mask (mask=1 for assistant tokens to train on)
  - `render_for_completion()`: Same but drops last assistant message (used in RL for rollouts)
  - GPT-4 style split pattern with `\p{N}{1,2}` (not 1-3, optimized for small vocab)
  - Default vocab size: 32768

**dataloader.py** -- BOS-aligned best-fit packing

  - Documents packed using best-fit algorithm (minimizes cropping)
  - Every row starts with BOS token (cleaner attention patterns)
  - 100% utilization (no padding), ~35% tokens cropped at T=2048
  - `_document_batches()`: Infinite multi-epoch iterator over parquet files with DDP sharding

**dataset.py** -- Data download/management

  - Downloads pretraining data shards (parquet files) from HuggingFace
  - Default dataset: NVIDIA ClimbMix (used in current speedrun)

**common.py** -- Utilities

  - `COMPUTE_DTYPE`: Auto-detected (bf16 on Ampere+, fp32 otherwise). Override with `$NANOCHAT_DTYPE`
  - `compute_init()`: Seed, precision, DDP setup (torchrun env detection)
  - `get_peak_flops()`: Hardcoded BF16 peak FLOPS table for MFU calculation
  - `print0()`, `DummyWandb`, colored logging

**checkpoint_manager.py** -- Save/Load

  - Three checkpoint directories: `base_checkpoints/`, `chatsft_checkpoints/`, `chatrl_checkpoints/`
  - Files per step: `model_XXXXXX.pt`, `optim_XXXXXX_rankN.pt`, `meta_XXXXXX.json`
  - `build_model()`: Meta-device init -> load state dict -> patch missing keys for backward compat
  - `load_model(source)`: Convenience; source is "base", "sft", or "rl"

**core_eval.py** -- DCLM CORE metric evaluation

  - Implements the DCLM benchmark (multiple choice, schema, language modeling tasks)
  - Few-shot prompting with Jinja2 templates
  - Uses loss-based selection for MC tasks, exact-match for LM tasks

**loss_eval.py** -- Bits Per Byte (BPB) evaluation

  - Vocab-size-invariant loss metric: normalizes cross-entropy by token byte length
  - Special tokens (BOS, etc.) excluded from metric

**fp8.py** -- FP8 training support (requires H100+ and torchao)

**execution.py** -- Python code execution tool for the model

---

3. SCRIPTS (`scripts/`)
-----------------------

**base_train.py** -- Pretraining (the main training loop)

  - Key args: `--depth` (single complexity dial), `--target-param-data-ratio`, `--fp8`, `--device-batch-size`
  - Auto-derives: n_embd = depth * aspect_ratio, n_head = n_embd / head_dim, etc.
  - Learning rate schedule: linear warmup + cosine warmdown
  - Logs to wandb: val_bpb, core_metric, MFU, tok/sec, VRAM
  - Periodic: BPB eval, CORE metric eval, text sampling, checkpoint saving

**base_eval.py** -- Evaluate base model (CORE score + BPB + samples)

**chat_sft.py** -- Supervised Fine-Tuning

  - Loads base model checkpoint, trains on chat-formatted conversations
  - Task mixture: SmolTalk + MMLU + GSM8K + SpellingBee + CustomJSON (identity data)
  - Loss mask: only trains on assistant tokens (mask=1)
  - Inherits most hyperparams from pretrained checkpoint

**chat_rl.py** -- Reinforcement Learning (simplified GRPO/REINFORCE)

  - Trains on GSM8K via policy gradient
  - No KL regularization, no PPO clipping (on-policy, no trust region)
  - DAPO-style token-level normalization, mean-subtracted advantages
  - Evaluates pass@k on GSM8K test set

**chat_eval.py** -- Evaluate chat model on task suite

**chat_cli.py** -- CLI chat interface

**chat_web.py** -- FastAPI + uvicorn web UI (ChatGPT-like)

**tok_train.py** -- Train the BPE tokenizer

**tok_eval.py** -- Evaluate tokenizer compression rate

---

4. TASKS (`tasks/`)
-------------------

- `common.py`: `TaskMixture` (weighted mix) and `TaskSequence` (sequential)
- `mmlu.py`: Multiple-choice, 57 subjects
- `gsm8k.py`: Grade school math (8K problems), supports tool use (calculator)
- `arc.py`: Science questions (multiple choice)
- `spellingbee.py`: Letter counting / spelling tasks
- `humaneval.py`: Simple Python coding
- `smoltalk.py`: HuggingFace SmolTalk conversation dataset
- `customjson.py`: Load arbitrary JSONL conversations

---

5. RUN SCRIPTS (`runs/`)
------------------------

- **speedrun.sh** -- Full GPT-2 training pipeline (~3 hrs on 8xH100):
  1. Setup uv venv
  2. Download data shards (~170)
  3. Train tokenizer (32K vocab on ~2B chars)
  4. Pretrain d24 model with FP8
  5. Evaluate base model
  6. Download identity conversations
  7. SFT finetuning
  8. Evaluate chat model
  9. Generate report

- **miniseries.sh** -- Sweep over depths to produce scaling law data
- **scaling_laws.sh** -- Scaling law experiments
- **runcpu.sh** -- Tiny model training on CPU/MPS (for testing only)

---

6. THE DEPTH DIAL
-----------------

The single most important concept. Setting `--depth=N` auto-derives everything:

```
n_embd      = depth * aspect_ratio (default 64)
n_head      = n_embd // head_dim (default 128)
n_kv_head   = n_head (GQA can reduce this)
vocab_size  = 32768
sequence_len = 2048
```

GPT-2 capability ~ d24-d26 range. Quick experiments ~ d12 (~5 min on 8xH100).

---

7. DATA FLOW
------------

```
Raw parquet shards
    -> dataloader.py (BOS-aligned best-fit packing)
    -> tokenized batches (B, T) of ints
    -> model forward (cross-entropy loss)
    -> Muon + AdamW optimizer step
    -> checkpoint save
    -> SFT: chat-formatted conversations with loss masking
    -> RL: on-policy rollouts + REINFORCE
    -> Engine inference (KV cache + prefill/decode)
    -> CLI or Web UI
```

---

8. KEY DESIGN DECISIONS
------------------------

- No `torch.amp.autocast`. Explicit dtype management via `COMPUTE_DTYPE` and custom `Linear` layer
- No config objects / factories. Single `GPT` module, single `GPTConfig` dataclass
- No framework overhead. Plain PyTorch, minimal abstraction
- Vocab padding for DDP efficiency (avoids rank divergence on padding)
- Meta-device initialization pattern (init shapes first, then `init_weights()`)
- BOS-aligned packing trades ~35% token cropping for cleaner attention patterns
- Muon optimizer for matrix weights (faster convergence), AdamW for embeddings/scalars