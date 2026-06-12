---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Additions Over nanoGPT
translated: false
type: note
---

Here's the full breakdown of what nanochat adds over nanoGPT:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  nanochat vs nanoGPT — What's Extra
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT is a pretraining-only harness. It has:
  - model.py (~340 lines): vanilla GPT-2 architecture (LayerNorm, GELU, learned positional embeddings, weight tying, bias in Linears)
  - train.py (~300 lines): pretraining loop on raw text
  - sample.py: basic text generation
  - That's it. 2 Python files.

nanochat is the full LLM lifecycle in one repo. Here's every major addition:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. MODEL ARCHITECTURE (gpt.py) — significantly upgraded
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Feature                  | nanoGPT                  | nanochat                          |
|--------------------------|--------------------------|-----------------------------------|
| Positional encoding      | Learned (wpe embedding)  | Rotary (RoPE) — no wpe            |
| Normalization            | LayerNorm (learnable)    | RMSNorm (no learnable params)     |
| Activation               | GELU                     | ReLU² (relu squared)              |
| Attention                | Single combined c_attn   | Separate c_q, c_k, c_v, c_proj   |
| KV heads                 | MHA only                 | Grouped-Query Attention (GQA)     |
| QK norm                  | No                       | Yes (q,k normalized after RoPE)   |
| Bias                     | Yes (configurable)       | No bias anywhere                  |
| Weight tying             | Yes (wte = lm_head)      | No — untied embeddings            |
| Dropout                  | Yes                      | No dropout at all                 |
| Logit softcap            | No                       | Yes (tanh softcap at ±15)         |
| Sliding window attention | No                       | Yes (SSSL pattern per layer)      |
| Value Embeddings         | No                       | ResFormer-style value residual    |
| Smear (prev token mix)   | No                       | Gate-mixed prev token embedding   |
| Backout (mid-layer sub)  | No                       | Subtract halfway residual         |
| Residual scaling         | Fixed                    | Per-layer resid_lambdas + x0      |
| Flash Attention          | PyTorch SDPA             | FA3 → FA2 → SDPA fallback chain   |
| KV Cache                 | None (crop-based)        | Proper FA3 KV cache for inference |
| FP8 training             | No                       | Dynamic tensorwise FP8 (e4m3/e5m2)|
| Optimizer                | Single AdamW             | MuonAdamW (Muon for matrices,     |
|                          |                          | AdamW for embeddings/scalars)     |
| Weight init              | Normal(0, 0.02)          | Uniform for attn, zeros for proj, |
|                          |                          | explicit per-layer resid/x0 init  |
| Vocab padding            | Yes (to 50304)           | Yes (to nearest 64)               |

Key architecture changes explained:

  RoPE vs learned positional: nanoGPT adds a learned embedding per position (wpe). nanochat uses rotary embeddings — relative position encoded via rotation in complex space. Better length generalization.

  ReLU² vs GELU: `F.relu(x).square()` — simpler, faster, empirically competitive at this scale. No erf computation.

  GQA: n_kv_head can be < n_head. E.g. 6 query heads but only 6 KV heads (equal here, but the infrastructure supports GQA ratios). Saves KV cache memory during inference.

  Sliding window: The `SSSL` pattern means 3 layers use short window (1/4 context), 1 layer uses full context. Tiled across layers. Final layer always full. Saves FLOPs on most layers while preserving long-range capability.

  Value Residuals (ResFormer): Every other layer has learned per-token embeddings (value_embeds) that get gated into the V tensor. `v = v + gate * ve`. Alternating layers, last always included.

  Smear: Mixes previous token's embedding into current via a learned gate. Cheap bigram-like information flow at the embedding level. `x = x + sigmoid(gate(x)) * x_prev`

  Backout: At the halfway layer, caches the residual stream. Before the final norm, subtracts `lambda * x_backout` to remove low-level features before logit projection.

  Muon optimizer: Matrix params use Muon (momentum + Newton-Schulz orthogonalization), embeddings use AdamW. Separate LR schedules per param group. Much more efficient for large matrix params.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. SFT — Supervised Fine-Tuning (chat_sft.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT has NO SFT. nanochat has a full SFT pipeline:

What SFT does:
  Takes a pretrained base model and fine-tunes it on conversations (user/assistant pairs) so it learns to follow instructions and chat.

How it works in nanochat:

  a) Conversation rendering (tokenizer.render_conversation):
     - Conversations are tokenized with special tokens:
       <|bos|> <|user_start|> ... <|user_end|> <|assistant_start|> ... <|assistant_end|>
     - A loss mask is generated: mask=1 only for assistant tokens
     - User prompts, BOS, special tokens = mask=0 (not trained on)

  b) Data mixture (TaskMixture):
     - SmolTalk: 460K rows of general conversations
     - CustomJSON: 1000 synthetic identity conversations ("Who are you?" "I am nanochat...")
     - MMLU: 100K rows × 3 epochs (multiple choice knowledge)
     - GSM8K: 8K rows × 4 epochs (math with tool use)
     - SimpleSpelling: 200K rows (spell the word 'apple')
     - SpellingBee: 80K rows (how many 'r' in 'strawberry'?)

  c) BOS-aligned packing (bestfit):
     - Conversations are packed into fixed-length rows using best-fit algorithm
     - No tokens discarded (padding with masked targets instead)
     - Each row starts with BOS

  d) Tool use support:
     - The tokenizer has <|python_start|> <|python_end|> <|output_start|> <|output_end|> tokens
     - GSM8K trains the model to invoke a Python calculator tool
     - At inference, the Engine actually evals the Python expressions and feeds results back

  e) ChatCORE evaluation during SFT:
     - Runs 6 benchmarks every N steps: ARC-Easy, ARC-Challenge, MMLU, GSM8K, HumanEval, SpellingBee
     - ChatCORE = mean centered accuracy (normalized against random baseline)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. RL — Reinforcement Learning (chat_rl.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT has NO RL. nanochat implements a simplified GRPO/REINFORCE on GSM8K:

The pipeline:
  1. Load the SFT model
  2. For each GSM8K question:
     - Generate N=16 samples from the model
     - Check each sample against the ground truth answer
     - Reward = 1 if correct, 0 if wrong
  3. Compute advantages: reward - mean_reward (not z-score, just subtract mean)
  4. Policy gradient: loss = -sum(logp * advantage) / num_valid_tokens
  5. No KL penalty, no PPO ratio/clip — pure on-policy REINFORCE

What makes it "GRPO-inspired" but simplified:
  - No trust region / KL to reference model
  - On-policy (no need for PPO ratio + clip)
  - DAPO-style token-level normalization
  - Advantage = (r - mu) not (r - mu)/sigma

Tracks pass@k metrics: probability that at least 1 of k samples is correct.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. INFERENCE ENGINE (engine.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT: basic generate() that crops to block_size, no caching.

nanochat: Full inference engine with:
  - KV Cache (FA3-native, pre-allocated tensors)
  - Prefill: batch=1 prompt forward, then replicate cache for N samples
  - Tool use state machine: detects <|python_start|>, evals expressions, injects results
  - Multi-sample generation (generate N completions in parallel)
  - Streaming yields (token_column, token_masks) per step

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. EVALUATION SUITE (tasks/ + core_eval.py + chat_eval.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT: only val loss on OpenWebText.

nanochat has 8 evaluation tasks:

  Categorical (logit-based, fast):
    - ARC-Easy / ARC-Challenge (science reasoning, 4-way MC)
    - MMLU (57 subjects, 4-way MC)

  Generative (sample + check):
    - GSM8K (math word problems)
    - HumanEval (Python code generation)
    - SpellingBee (letter counting)
    - SimpleSpelling (word spelling)

  Pretraining metrics:
    - DCLM CORE score (perplexity-based across 5 tasks)
    - val_bpb (bits per byte, vocab-size-invariant)

  ChatCORE: composite metric across all 6 chat eval tasks, centered against random baselines.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. TOKENIZER (tokenizer.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT: uses tiktoken (GPT-2 encoding) or trains a char-level tokenizer. No special tokens.

nanochat: Custom BPE tokenizer (RustBPE for training, tiktoken for inference):
  - 32K vocab (configurable)
  - 8 special tokens: <|bos|>, <|user_start|>, <|user_end|>, <|assistant_start|>, <|assistant_end|>, <|python_start|>, <|python_end|>, <|output_start|>, <|output_end|>
  - render_conversation() method: turns chat messages into token ids + loss mask
  - render_for_completion(): strips last assistant message for RL generation
  - visualize_tokenization(): debug helper with color-coded output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. OTHER INFRASTRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - Checkpoint manager: saves/loads model + optimizer + metadata per stage (base/sft/rl)
  - MLflow logger: experiment tracking alternative to wandb
  - Scaling laws support: miniseries.sh, scaling_laws.sh, --depth as single dial
  - Report system: structured logging of eval results
  - Chat UI: web-based ChatGPT-like interface (scripts/chat_web.py)
  - Chat CLI: terminal-based chat interface (scripts/chat_cli.py)
  - Distributed training: proper DDP with Gloo patches
  - compute_init/cleanup: device detection, distributed setup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary: The Full LLM Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT covers:
  [pretrain] → [generate text]

nanochat covers:
  [train tokenizer] → [pretrain] → [eval CORE] → [SFT on conversations] →
  [RL on math tasks] → [eval ChatCORE] → [serve via chat UI]

The biggest conceptual additions are:
  1. SFT: teaching a base model to be a chat assistant via conversation fine-tuning
  2. RL: improving math/tool-use via reward-based policy gradient
  3. Tool use: the model can invoke a Python calculator and get results fed back
  4. Full eval suite: 6+ benchmarks with a composite metric (ChatCORE)
  5. Modern architecture: RoPE, GQA, sliding window, value residuals, ReLU², Muon optimizer
