---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanochat Engine Architecture
translated: false
type: note
---

Here's how `nanochat/engine.py` works — it's the **efficient batched inference engine** for nanochat's GPT model. It's a token-level engine: it takes token ID sequences in and streams token ID sequences out, knowing nothing about text.

## The three pieces

### 1. Calculator tool (`use_calculator`)
A small, sandboxed "tool use" hook. The model can emit a Python expression between `<|python_start|>` / `<|python_end|>` special tokens, and the engine evaluates it and injects the result between `<|output_start|>` / `<|output_end|>` tokens. Safety via:
- `eval` with `{"__builtins__": {}}` and a **3-second SIGALRM timeout**
- Character whitelist (only math chars, or letters/quotes/dots for string ops)
- Blacklist of dangerous patterns (`__`, `import`, `exec`, `open`, `getattr`, ...)
- Only `.count()` string methods allowed, and `**` (power) is disallowed in math mode

### 2. `KVCache`
A KV cache built specifically for **Flash Attention 3's `flash_attn_with_kvcache` API**. Key differences from the classic FA2 layout:
- Tensors are `(n_layers, B, T, H, D)` — FA3's native layout, **no transpose needed**
- FA3 updates the cache **in-place** during attention, so the engine just passes views in
- Position is tracked per batch element via a `cache_seqlens` int32 tensor (not a Python counter)
- Also stores `prev_embedding` — the previous token's normalized embedding needed by the model's **"smear"** trick (mixing prev-token embedding into the current position for cheap bigram info)
- `prefill(other)` copies a finished batch-1 cache into a larger batch cache (and expands the smear embedding from batch 1 to N)

### 3. `Engine.generate` — the main loop (generator)
This is the clever part. Strategy: **prefill once at batch 1, then clone the KV cache to run many samples in parallel**.

1. **Batch-1 prefill** of the prompt → one forward pass over all prompt tokens.
2. **Clone** the KV cache into a `num_samples`-sized decode cache (via `prefill()`), freeing the prefill cache.
3. Per-row **`RowState`** tracking: current token sequence, a deque of *forced* tokens, whether we're inside a Python block, the accumulated expression tokens, and completion status.

The loop per step:
- Samples one token per row (`sample_next_token`: argmax if `temperature=0`, else top-k + softmax + `multinomial` with a seeded RNG)
- But each row can instead **force** tokens from its deque (e.g. injected calculator output), so a batch can contain rows at different "logical" positions — token column is a mix of sampled and forced tokens, and the returned `token_masks` records which is which (1 = sampled, 0 = forced/prompt)
- Runs the **tool state machine**: on `<|python_start|>` starts accumulating expression tokens; on `<|python_end|>` evaluates via the calculator and pushes `<|output_start|>` + result + `<|output_end|>` into the forced deque
- Completes a row on `<|assistant_end|>` or `<|bos|>`
- `yield`s `(token_column, token_masks)` before the next forward pass — so callers can stream/decode incrementally
- Next forward is **one token per row** (shape `(B, 1)`) with the KV cache, which is the fast decode path

### 4. `Engine.generate_batch`
A non-streaming wrapper that just drains the generator, appends tokens to per-row result lists (excluding terminal tokens), and returns `(results, masks)`. Used by RL rollout sampling (`scripts/chat_rl.py`) and eval (`scripts/base_eval.py`), where masks mark which tokens were model-sampled vs. prompt/tool-forced — important for RL loss masking.

## Key integration points

- **Model side** (`nanochat/gpt.py`): each attention layer calls `kv_cache.get_layer_cache(layer_idx)` and hands the views to `flash_attn_with_kvcache`; the last layer advances `cache_seqlens`. The model reads/writes `kv_cache.prev_embedding` for the smear residual, and offsets rotary embeddings by `kv_cache.get_pos()`.
- The `__main__` block is a self-test verifying `Engine.generate` matches the naive `model.generate` (used by eval scripts).

## The big picture

The engine's main optimization is trading a one-time KV cache copy for **batched parallel sampling** — prefill once, then generate N samples/rollouts simultaneously sharing the same prompt, with a per-row tool-use state machine on top. The tradeoffs are documented inline in `scripts/chat_rl.py`: it runs in fp32 (`COMPUTE_DTYPE`), and it needs the tokenizer only for the tool-use special tokens.