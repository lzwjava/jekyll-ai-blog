---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Training Deep Dive
translated: false
type: note
---

OK here's the full deep dive.

=================================================================
FILES TOUCHED DURING TRAINING (base_train.py)
=================================================================

Core pipeline:

  nanochat/gpt.py          -- Model architecture (GPT, GPTConfig, attention, MLP)
  nanochat/dataloader.py   -- Parquet dataloader with BOS-bestfit packing
  nanochat/dataset.py      -- Lists parquet shard files from disk
  nanochat/tokenizer.py    -- Custom tokenizer (train/encode/decode)
  nanochat/optim.py        -- MuonAdamW optimizer (Muon for matrices, AdamW for rest)
  nanochat/common.py       -- DDP init, device detection, print0, COMPUTE_DTYPE
  nanochat/flash_attention.py -- FA3/FA2/SDPA unified interface
  nanochat/loss_eval.py    -- evaluate_bpb() for validation loss
  nanochat/checkpoint_manager.py -- save/load checkpoints
  nanochat/engine.py       -- KVCache + Engine for generation (used at sample_every)
  nanochat/core_eval.py    -- CORE metric evaluation
  nanochat/fp8.py          -- Optional FP8 training (H100+)
  nanochat/mlflow_logger.py -- MLflow integration
  scripts/base_eval.py     -- evaluate_core() imported by base_train

=================================================================
TRAINING LOGIC FLOW
=================================================================

1. INIT PHASE
   - Autodetect GPU, init DDP (torchrun) or single GPU
   - Init experiment tracker (wandb/mlflow/none)
   - Load tokenizer, get vocab_size
   - Build model on meta device (no memory), then .to_empty(device).init_weights()
   - Optionally load checkpoint for resume
   - Optionally convert Linear -> Float8Linear (--fp8)
   - torch.compile(model)

2. SCALING LAWS (the smart part)
   - Build a reference d12 model on meta to get scaling params
   - Compute optimal tokens = target_param_data_ratio * scaling_params
   - Compute optimal batch size via Power Lines: Bopt ∝ D^0.383
   - Compute LR correction: η ∝ sqrt(B/Bref)
   - Compute weight decay: λ = λref *sqrt(B/Bref)* (Dref/D)  (T_epoch framework)

3. OPTIMIZER
   - Muon for matrix params (transformer.h) -- Newton-Schulz orthogonalization
   - AdamW for embeddings, lm_head, scalars (resid_lambdas, x0_lambdas, smear)
   - Separate LR per param group, scaled by 1/sqrt(model_dim/768)

4. DATA LOADING
   - Reads parquet shards (fineweb-edu) row groups
   - BOS-bestfit packing: each row starts with BOS, docs packed by best-fit
   - ~35% tokens cropped (not wasted, just not trained on)
   - GPU pre-allocated buffer, single HtoD copy per batch

5. TRAINING LOOP
   while step <= num_iterations:
     - Every eval_every: run evaluate_bpb on val set
     - Every core_metric_every: run CORE eval (ARC, MMLU, GSM8K, HumanEval, SpellingBee)
     - Every sample_every: generate samples from fixed prompts
     - Every save_every: save model + optimizer + meta checkpoint
     - Forward pass with gradient accumulation (total_batch_size / world_tokens_per_fwdbwd)
     - LR schedule: linear warmup -> constant -> linear warmdown
     - Muon momentum: warmup 0.85->0.97, warmdown to 0.90
     - Weight decay: cosine decay to zero
     - optimizer.step(), zero_grad

=================================================================
COMPARISON WITH NANO-GPT
=================================================================

Feature              | nanoGPT                   | nanochat
---------------------|---------------------------|---------------------------
Optimizer            | AdamW only                | MuonAdamW (Muon for matrices,

                     |                           | AdamW for embeddings/scalars)
Position encoding    | Learned absolute pos emb  | Rotary embeddings (RoPE)
Attention norm       | None                      | QK norm (rms_norm on q,k)
Activation in MLP    | GELU                      | ReLU^2
Norm type            | LayerNorm                 | RMSNorm (no learnable params)
Norm placement       | Pre-norm                  | Post-embedding norm + pre-block norm
Embedding/Unembed    | Tied weights              | Untied weights (separate LR)
Attention            | Multi-head (MHA)          | GQA support (n_kv_head <= n_head)
Sliding window       | No                        | Yes, configurable pattern (SSSL etc)
Flash Attention      | Not built-in              | FA3 > FA2 > SDPA auto-switch
KV cache (inference) | Not built-in              | Full KVCache class with FA3 API
Value embeddings     | No                        | ResFormer-style value embedding gates
Residual scaling     | None                      | Per-layer resid_lambdas + x0_lambdas
Smear (prev token)   | No                        | Smear gate mixes prev embedding
Backout              | No                        | Subtract mid-layer residual
Logit softcap        | No                        | tanh softcap at 15
Data loading         | tiktoken, mmap .bin       | Parquet shards, BOS-bestfit packing
Tokenizer            | tiktoken GPT-2 BPE        | Custom sentencepiece-trained tokenizer
Scaling laws         | None                      | Auto batch/LR/warmdown from depth
FP8 training         | No                        | Optional FP8 (H100+)
Distributed          | DDP basic                 | DDP + gradient accumulation + scaling
Checkpoint           | Manual save               | checkpoint_manager with state resume
Eval                 | Manual                    | Automated CORE metric, val bpb, samples
Tracker              | wandb manual              | wandb/mlflow/none auto-config
SFT/Chat pipeline    | Not included              | Full: chat_sft.py, chat_web.py, chat_cli.py
Calculator tool use  | No                        | Built-in: <|python_start|>...<|python_end|>

Key structural differences:

- nanoGPT is a single file (model.py ~300 lines). nanochat is a full project with
  15+ modules, a 3-phase pipeline (pretrain -> SFT -> RL), and production serving.
- nanoGPT uses standard AdamW. nanochat uses Muon optimizer (Newton-Schulz based)
  for weight matrices which converges faster.
- nanoGPT's model is essentially GPT-2 architecture. nanochat has many modern
  additions: RoPE, GQA, QK-norm, ReLU^2, value embeddings, sliding window,
  smear, backout, logit softcap.

=================================================================
chat_sft.py -- SUPERVISED FINE-TUNING
=================================================================

Takes a pretrained base model and fine-tunes it on chat data.

Data mixture:

- SmolTalk: 460K rows of general conversations
- CustomJSON: 1000 identity conversations (who are you?)
- MMLU: 100K rows x3 epochs (teaches multiple choice)
- GSM8K: 8K rows x4 epochs (teaches math + tool use)
- SimpleSpelling: 200K rows (spell the word 'apple')
- SpellingBee: 80K rows (how many 'r' in 'strawberry'?)

Key differences from base_train:

- Loads pretrained checkpoint, inherits hyperparams
- Uses loss masking: only assistant tokens have loss, user/padding masked (-1)
- Best-fit conversation packing (same algo but conversation-aware)
- Evaluates ChatCORE metric (ARC, MMLU, GSM8K, HumanEval, SpellingBee via chat)
- LR schedule based on progress (0->1) instead of absolute steps
- Weight decay = 0 (continued from end of pretraining where it decayed to 0)
- Saves to chatsft_checkpoints/ instead of base_checkpoints/

=================================================================
chat_web.py -- PRODUCTION WEB SERVER
=================================================================

FastAPI server that serves:

- GET /           -> HTML chat UI (from nanochat/ui.html)
- POST /chat/completions -> OpenAI-compatible streaming API
- GET /health     -> health check
- GET /stats      -> worker pool stats

Multi-GPU via WorkerPool: each GPU loads a full model copy, requests round-robin.
Abuse limits: 500 msgs/req, 8K chars/msg, 32K total, temp 0-2, top-k 0-200.

Uses Engine.generate() which has KV cache (see below).

=================================================================
KV CACHE -- YES, USED DURING INFERENCE
=================================================================

YES. KV cache is fully implemented in nanochat/engine.py and used
during all inference (chat_cli, chat_web, sample_every in training).

The KVCache class (engine.py:82-137):

- Pre-allocates: (n_layers, B, T, H, D) tensors for K and V
- Tracks position via cache_seqlens (int32 tensor)
- Stores prev_embedding for the smear mechanism during decode
- FA3 updates cache in-place via flash_attn_with_kvcache

How Engine.generate() uses it:

  1. PREFILL: Create KVCache(batch=1, seq=len(prompt)), run full prompt through
     model.forward(tokens, kv_cache=kv_cache_prefill)
  2. CLONE: Create KVCache(batch=num_samples), .prefill(copy from prefill cache)
  3. DECODE LOOP: Each step feeds only the NEW token, model reads from cache
     model.forward(new_token, kv_cache=kv_cache_decode)  # T=1, cache has all prev

The model.forward() (gpt.py:416) handles both modes:

- kv_cache=None  -> training: full causal attention, no cache
- kv_cache given -> inference: flash_attn_with_kvcache, cache-aware rotary offset

Sliding window also works with KV cache: window_size is passed through
to flash_attn_with_kvcache, so SSSL pattern applies during inference too.

The Calculator tool use also works during generation: when the engine sees
<|python_start|>...<|python_end|>, it eval()s the expression, forces the
result tokens as <|output_start|>result<|output_end|> into the stream.
