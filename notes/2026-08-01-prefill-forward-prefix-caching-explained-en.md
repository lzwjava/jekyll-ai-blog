---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prefill Forward Prefix Caching Explained
translated: false
type: note
---

Here's `_prefill_forward` explained line by line. First, two key facts you need to know:

**Fact 1 — "packed" tensors.** q, k, v are *packed*: the sequences in the batch are concatenated into one flat tensor, and `cu_seqlens_q` / `cu_seqlens_k` (cumulative sequence lengths) tell you where each sequence starts/ends. E.g. `cu_seqlens_q = [0, 4, 9]` means seq 0 = tokens 0–3, seq 1 = tokens 4–8.

**Fact 2 — q and k can have different lengths.** During prefill with prefix caching, each sequence has:
- `seqlen_k` = cached prefix tokens + new tokens (everything that will be attended to)
- `seqlen_q` = only the new tokens (these are what we compute output for)

You can see this in `prepare_prefill`: `seqlen_q = seq.num_scheduled_tokens`, `seqlen_k = end = start + seqlen_q`.

## The two branches

```python
if context.block_tables is not None and k_cache is not None:
```

`block_tables` is only set when `cu_seqlens_k[-1] > cu_seqlens_q[-1]` — i.e. **a cached prefix exists**. So this condition splits into:

### Branch 1 — Prefix caching (K/V already in the paged cache)

```python
seqlens  = full KV length per seq (prefix + new)
q_lens   = new-token length per seq
k_gathered, v_gathered = _gather_kv_from_cache(...)   # read prefix + new K/V out of the paged blocks
k_flat = torch.cat([k_gathered[i, :seqlens[i]] ...])  # re-flatten into packed format
```

The story here:
1. The *new* tokens' K/V were already written into the paged cache by `store_kvcache` in `forward()` (before this function ran).
2. `_gather_kv_from_cache` reads the **entire** K/V sequence back out of the blocks — shared prefix + freshly written new tokens — into dense tensors.
3. They're flattened back to packed form, so `k_flat` = `[prefix_0, new_0, new_1, ...]` per sequence.
4. q stays as-is: it's only the new tokens.

Then the key bookkeeping line:

```python
cached_len_per_seq = [(seqlens[i] - q_lens[i], q_lens[i], seqlens[i]) ...]
#                    (  cached_len,             q_len,    kv_len  )
```

For each sequence: `cached_len = kv_len − q_len` = how many prefix tokens come before the queries.

### Branch 2 — Standard prefill (no existing cache)

```python
q_lens  = new-token lengths
kv_lens = full prompt lengths
cached_len_per_seq = [(kv_lens[i] - q_lens[i], q_lens[i], kv_lens[i]) ...]
```

Here every token is new, so `kv_len == q_len` and `cached_len = 0` for every sequence. q/k/v are the whole prompt, used directly.

## The magic: how the causal mask handles the prefix

Both branches call `_flash_attention(q, k, v, self.scale, causal=True, cached_len_per_seq=...)`. Since the lists are non-None, it uses `flash_attn_varlen_func` with **separate** `cu_seqlens_q` and `cu_seqlens_k` (that's why q and k can have different lengths).

The crucial behavior is documented in flash-attn itself — **causal mask aligned to the bottom-right corner**:

```
if seqlen_q = 2 and seqlen_k = 5:
    1 1 1 1 0
    1 1 1 1 1
```

So query position `i` attends to key position `j` iff `j ≤ i + (kv_len − q_len) = i + cached_len`.

Think about what this means for prefix caching: key positions `0..cached_len−1` are the prefix, and key position `cached_len + i` is the new token *after* query `i`. The mask says:

- query `i` attends to **all prefix tokens** (positions `0..cached_len−1`) ✓
- plus earlier new tokens (`cached_len..cached_len + i`) ✓
- but **not** future new tokens (positions `> cached_len + i`) ✓ (causal)

That's exactly the correct semantics: each new token can see the full history, not the future. No custom mask code needed — the bottom-right alignment does it for free.

## What comes out

`o` is the packed attention output for the **new tokens only** (`total_q_tokens` rows). It flows up through the rest of the transformer; the last token of each sequence eventually hits the LM head → first output token. Meanwhile the new K/V are already sitting in the paged cache, so the subsequent decode steps can attend to them.

One more nuance: in branch 1 the K/V went *into* the cache (`store_kvcache`) and were then *read back out* (`_gather_kv_from_cache`) so attention could be computed over the full sequence — a round-trip through the paged cache. In branch 2 (no prefix), q/k/v are used directly. And in `forward()` there's also a CUDA-graph-capture shortcut (`torch.cuda.is_current_stream_capturing()`) that skips all cache ops entirely, since `.item()` calls and tensor conditionals aren't allowed during graph capture.
