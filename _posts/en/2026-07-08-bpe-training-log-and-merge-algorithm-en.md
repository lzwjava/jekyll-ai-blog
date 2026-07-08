---
audio: false
generated: true
image: false
lang: en
layout: post
title: BPE Training Log and Merge Algorithm
translated: false
type: note
---

Question: What is happening in this nanochat rustbpe training log, and how does the underlying BPE merge algorithm work?

Answer:

## What the log is showing

This is `rustbpe` — nanochat's custom Rust-based BPE trainer (used instead of Python `tiktoken`/`sentencepiece` training because raw counting + merging over billions of byte-pairs is a hot loop that Python can't do fast enough). Each line is one **merge step**:

```
Progress: 97% (31528/32503 merges) - Last merge: (12696, 9604) -> 31783 (frequency: 1090)
```

- `12696, 9604` are token IDs being merged into a new token `31783`
- `frequency: 1090` is how many times that adjacent pair occurred in the training corpus at this point
- Total target is `32503` merges, meaning final vocab size = `256 (byte-level base tokens) + 32503 merges + special tokens` — this lands near nanochat's configured vocab size (check your `tokenizer_train.py` for `--vocab_size`, since it's not the stock 65536 default if you're getting 32503 merges).

The monotonically decreasing frequency (1109 → 1090 → 1070 → 1051 → 1033) is the expected signature of BPE: early merges consume very common pairs (whitespace+word, common bigrams), and as training proceeds, remaining unmerged pairs are progressively rarer.

## The core algorithm (what rustbpe is doing under the hood)

BPE training is:

1. Start with base vocab = 256 byte values (nanochat tokenizes raw UTF-8 bytes, not pre-split words — no Unicode normalization surprises)
2. Count all adjacent pair frequencies across the entire corpus
3. Merge the single most frequent pair into a new token
4. Repeat until you hit `vocab_size - 256 - num_special_tokens` merges

Minimal Python reference implementation (obviously not what rustbpe runs — this is O(n) rescans per merge, hence why Karpathy rewrote it in Rust with a priority queue + incremental count updates):

```python
from collections import Counter

def get_pair_counts(ids):
    counts = Counter()
    for chunk in ids:  # ids: list of token-id sequences (documents)
        for a, b in zip(chunk, chunk[1:]):
            counts[(a, b)] += 1
    return counts

def merge(ids, pair, new_id):
    out = []
    for chunk in ids:
        merged = []
        i = 0
        while i < len(chunk):
            if i < len(chunk) - 1 and (chunk[i], chunk[i+1]) == pair:
                merged.append(new_id)
                i += 2
            else:
                merged.append(chunk[i])
                i += 1
        out.append(merged)
    return out

def train_bpe(ids, vocab_size, base_vocab=256):
    ids = [list(bytearray(doc, "utf-8")) for doc in ids]  # byte-level start
    merges = {}
    next_id = base_vocab
    num_merges = vocab_size - base_vocab
    for i in range(num_merges):
        counts = get_pair_counts(ids)
        if not counts:
            break
        best_pair = max(counts, key=counts.get)
        ids = merge(ids, best_pair, next_id)
        merges[best_pair] = next_id
        print(f"merge {i+1}/{num_merges}: {best_pair} -> {next_id} (freq {counts[best_pair]})")
        next_id += 1
    return merges
```

This is exactly the log pattern you're seeing, just Python-speed instead of Rust-speed. `rustbpe`'s real gain over this naive version: it doesn't recompute `get_pair_counts` from scratch every merge (that's the killer — full corpus rescan per merge is O(vocab_size × corpus_size)). Instead it maintains a live count structure and only updates counts in the *local neighborhood* of each merge occurrence, plus uses a max-heap for O(log n) best-pair lookup instead of O(n) linear scan. That's the difference between "161.78s for 32503 merges" and what would be hours in pure Python on a nontrivial corpus.

## Why this matters for your MoE/nanochat work

Two things worth checking in your run given your DeepSeek v4 direction:

- **Vocab size vs MoE routing**: larger vocab → larger embedding + LM head matrices, which matters more for MoE models since you're already paying a big parameter budget on experts. DeepSeek v2/v3 use ~100k-128k vocab (byte-level BBPE) — if you're experimenting toward v4-scale, your tokenizer vocab choice interacts directly with embedding table size and thus HBM footprint on your MI300X runs.
- **Byte-level fallback**: since rustbpe (like GPT-2/nanochat) starts from raw bytes, you get guaranteed no-OOV-token behavior — worth confirming your merge list doesn't waste slots on rare byte sequences from noisy corpus data (check the tail of your merges log — merges near frequency ~1000 on a large corpus are borderline; you could stop earlier and put those extra slots toward more special/reserved tokens for agent/tool-use control tokens, which matters if you're heading toward agentic architectures).

If you want, paste your actual `tokenizer_train.py` args (vocab_size, corpus size) and I can help you tune where to cut off merges vs. reserve slots for structured control tokens (tool-call start/end, thinking tags, etc.) — relevant if you're building toward agent-native pretraining rather than just replicating stock nanochat.
