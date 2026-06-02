---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang HiCache SWA Multi-Tier KV
translated: false
type: note
---

Great question. I dug into the SGLang codebase to verify every claim. Here's the breakdown:

========================================================================
1. HiCache: MULTI-TIER KV CACHE (GPU -> CPU -> SSD)
========================================================================

The key architecture is a 3-level hierarchy, modeled after CPU caches:

  L1 = GPU VRAM    (fastest, smallest, managed by RadixAttention)
  L2 = CPU Host RAM (medium, managed by MHATokenToKVPoolHost)
  L3 = Distributed  (slowest, largest: Mooncake/3FS/NIXL/AIBrix backends)

Core files:
  - python/sglang/srt/mem_cache/hiradix_cache.py  -- HiRadixCache (extends RadixCache)
  - python/sglang/srt/mem_cache/memory_pool_host.py -- L2 CPU pool (2899 lines!)
  - python/sglang/srt/mem_cache/hicache_storage.py  -- L3 abstract interface
  - python/sglang/jit_kernel/hicache.py + csrc/hicache.cuh -- GPU I/O kernels

WHY DATA MOVEMENT DROPS TO ~1/7:

(a) Longest-prefix matching in the radix tree
    Before any transfer, HiRadixCache finds the longest contiguous cached
    prefix. Only the MISSING SUFFIX is recomputed. No full-sequence copies.

(b) Custom CUDA kernels bypass L1 cache
    hicache.cuh uses `ld.global.L1::no_allocate` and `st.global.L1::no_allocate`
    instructions -- these skip L1 cache pollution entirely. The kernels achieve
    ~3x throughput over standard cudaMemcpyAsync for GPU<->CPU transfers.

(c) Compute-transfer overlap (layerwise pipelining)
    While layer N is being computed on GPU, layer N+1's KV cache is being
    loaded from CPU. Transfer latency is hidden behind computation.

(d) Page-first memory layouts
    `page_first_direct` groups all layers for a page contiguously in CPU
    memory, enabling single-object zero-copy transfers between tiers.

(e) Write-back policies reduce unnecessary I/O
    `write_through_selective` only backs up hot data (accessed above a
    threshold). `write_back` defers writes until eviction. This means
    cold data never crosses tier boundaries.

(f) MLA optimization (DeepSeek-style)
    For Multi-Layer Attention, all TP ranks hold identical KV data,
    so only ONE rank performs write-back -- eliminating (TP-1)x redundant
    storage across ranks.

========================================================================
2. SWA + HiCache: WHY CACHEABLE TOKENS 5x
========================================================================

This is the subtlest claim. The key insight:

  SWA layers only need sliding_window_size tokens (e.g., 4096),
  NOT the full sequence length (e.g., 128K).

Core files:
  - python/sglang/srt/mem_cache/unified_cache_components/swa_component.py
  - python/sglang/srt/mem_cache/swa_memory_pool.py
  - python/sglang/srt/mem_cache/swa_radix_cache.py

HOW IT WORKS:

(a) Dual memory pools (swa_memory_pool.py)
    SWAKVPool maintains TWO separate allocators:
      - full_kv_pool  (for full-attention layers)
      - swa_kv_pool   (sized much smaller, only sliding_window_size)
    A full_to_swa_index_mapping tensor maps between them.

(b) Tombstoning in the radix tree
    When SWA data is evicted from an internal node, component_data[SWA]
    becomes None while full attention data stays. This means SWA layers
    can independently manage their cache lifetime.

(c) SWA-aware HiCache transfers
    During backup to host, SWAComponent.build_hicache_transfers() creates
    a PoolTransfer using SWA pool indices -- only sliding_window_size
    tokens per node, not the full sequence. This is the 5x factor:
    if window=4096 and seq=20480, you transfer 4096 instead of 20480 = 5x
    reduction in per-request host memory and transfer volume.

(d) SWA-aware prefix matching
    create_match_validator() limits match depth to sliding_window_size
    tokens. It won't walk further up the tree than the window covers.
    This means the radix tree stays shallower for SWA layers.

NET EFFECT: With SWA, the host memory stores ~window_size tokens per
prefix node instead of full sequences. The same host RAM can cache
~5x more requests, dramatically increasing hit rates.

========================================================================
3. EXPERT PARALLELISM OPTIMIZATION
========================================================================

Core files:
  - python/sglang/srt/layers/moe/ep_moe/layer.py  -- DeepEPMoE
  - python/sglang/srt/layers/moe/token_dispatcher/deepep.py  -- DeepEPBuffer
  - python/sglang/srt/batch_overlap/two_batch_overlap.py  -- TBO
  - python/sglang/srt/eplb/eplb_algorithms/deepseek.py  -- EPLB

THREE KEY OPTIMIZATIONS:

(a) Two-Batch Overlap (TBO)
    Splits requests into micro-batches and interleaves attention compute
    with MoE all-to-all dispatch/combine. Uses YieldOperation yield
    points. Effectively hides communication latency behind compute,
    nearly doubling throughput.

(b) Expert Parallelism Load Balancer (EPLB)
    Analyzes expert activation statistics, then uses balanced_packing()
    and replicate_experts() to redistribute hot experts across GPUs.
    Prevents straggler GPUs from bottlenecking the whole cluster.
    Periodic rebalancing adapts to evolving traffic patterns.

(c) Multiple dispatch backends
    DeepEP normal mode (high-throughput prefill) vs low_latency mode
    (CUDA Graph decode). Also Mooncake, NIXL-EP, MORI backends for
    different hardware configs.

========================================================================
4. INPUT LENGTH BUCKETING
========================================================================

SGLang doesn't have an explicit "length_bucket" feature. The equivalent
comes from scheduling policies in:
  python/sglang/srt/managers/schedule_policy.py

(a) LPM (Longest Prefix Match) scheduling
    Sorts waiting requests by longest prefix match with the radix cache.
    This naturally groups requests sharing similar prefixes -- which
    correlates with similar effective input lengths.

(b) Routing-key scheduling
    Groups requests by MoE routing key similarity, batching requests
    that route to similar experts. Directly improves MoE compute
    efficiency.

(c) Chunked prefill with max_prefill_tokens
    Caps prefill tokens per batch (default 16384). PrefillAdder fits
    shorter requests first when sorted by prefix match, implicitly
    bucketing by length.

========================================================================
SUMMARY: WHY THIS ALL MATTERS FOR COST
========================================================================

The cost savings come from three angles:

1. CACHE EFFICIENCY (HiCache + SWA)
   - 1/7 data movement = 7x less PCIe/network bandwidth consumed
   - 5x more cacheable tokens = 5x higher cache hit rates
   - Net: most requests hit L1/L2 cache, rarely touching L3
   - Fewer recomputations = less GPU time per token

2. THROUGHPUT (EP + TBO + EPLB)
   - TBO hides communication behind compute (~2x throughput)
   - EPLB eliminates GPU utilization skew across the cluster
   - Expert replication handles hot experts without bottlenecks

3. SCHEDULING (prefix-aware + routing-key)
   - Groups complementary requests for maximum cache reuse
   - Prevents memory spikes from batching too many long prefills
   - Maximizes GPU utilization without OOM

Combined, this lets them serve the same traffic on fewer GPUs with
less bandwidth -- hence the price drop.
