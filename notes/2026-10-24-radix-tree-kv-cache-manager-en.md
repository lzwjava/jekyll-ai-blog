---
audio: false
generated: true
image: false
lang: en
layout: post
title: Radix Tree KV Cache Manager
translated: false
type: note
---

This is a **radix tree (prefix tree) based KV cache manager** — it caches KV entries under *shared token prefixes* so that repeated prompt prefixes can be reused instead of recomputed. Here's how it works end to end:

## The tree structure (`RadixTreeNode`)

Each node stores:
- `key` / `value`: `(page_size, num_kv_heads, head_dim)` chunks — a token sequence plus the KV indices backing it
- `children`: map from a `key_fn(key)` fingerprint → child node
- `ref_count`: number of active requests referencing this node (refcount > 0 = **protected**, can't be evicted)
- `timestamp`: last access time (used for LRU eviction via a heap)

Nodes form a tree where **every ancestor's key is a prefix of its descendants' keys**. The root is a dummy node with `ref_count = 1` (always protected, never evicted).

The routing key `key_fn` is the first token in a page: `x[0].item()` if `page_size == 1`, otherwise `tuple(x[:page_size].tolist())`. That means each node's key is exactly one page (or the aligned remainder after a split).

## Tree walk (`_tree_walk`)

```
while prefix_len < seq_len:
    child = node.children[key_fn(input_ids[prefix_len:])]   # descend by next page's first tokens
    match_len = align_down(fast_compare_key(child.key, rest), page_size)  # how many tokens match
    prefix_len += match_len
    if match_len != node.length:      # partial page match → split the node
        node = node.split_at(match_len)
        return node, prefix_len
    node.timestamp = tic              # LRU touch
```

`fast_compare_key` (a TVM/CUDA kernel in `kernel/csrc/src/radix.cpp`) compares the node's key tensor against the input and returns the first differing position.

## Split (`split_at`)

When only part of a node's page matches, the node is split in place: a new parent node takes the first `pos` tokens and inherits the refcount, while the original node keeps the remainder as its child. This lets a *partial* prefix of an existing node be cached/reused without breaking the tree invariants.

## Public API

- **`match_prefix(input_ids)`** → walks the tree, returns a `RadixCacheHandle` wrapping the deepest matched node. The handle's `get_matched_indices()` walks back up to the root concatenating `node.value` chunks — i.e., the physical KV indices for the whole matched prefix.
- **`insert_prefix(input_ids, indices)`** → aligns both to `page_size`, walks the tree, and if the new prefix isn't fully present, creates one new node for the `(prefix_len, insert_len]` tail and attaches it under the matched node. Returns `InsertResult(cached_len, handle)`.
- **`lock_handle(handle, unlock)`** → walks the node up to the root, incrementing/decrementing `ref_count` and moving bytes between `evictable_size` / `protected_size`. Handles must be locked before the matched values are used, or another request's `evict` could free them.
- **`evict(size)`** → collects all leaf nodes with `ref_count == 0` into a min-heap ordered by `timestamp` (LRU), pops leaves, removes them from the parent's `children`, and pushes newly-orphaned leaves. Returns the concatenated `value` tensors (the freed KV slots). Root is never collected.

## Tracking

`size_info` reports `evictable_size` (bytes in refcount-0 nodes) vs `protected_size` (bytes in live-referenced nodes), and the `counter` on `RadixTreeNode` gives each node a unique `uuid`.

**In short**: requests reuse cached attention KV for shared prefixes (matching + locking), new tails are inserted as nodes, and when the KV pool runs low the least-recently-used unreferenced leaves are evicted, with splits enabling fine-grained reuse. This is the vanilla SGLang radix cache design (with GPU-side key comparison and page-level granularity).
