---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 高缓存 SWA 多层 KV
translated: true
type: note
---

好问题。我深入研究了 SGLang 代码库以验证每项声明。以下为详细解析：

========================================================================
1. HiCache：多层 KV 缓存（GPU -> CPU -> SSD）
========================================================================

核心架构为三级层次结构，借鉴 CPU 缓存设计：

  L1 = GPU VRAM    （最快，最小，由 RadixAttention 管理）
  L2 = CPU 主机 RAM（中等，由 MHATokenToKVPoolHost 管理）
  L3 = 分布式存储  （最慢，最大：Mooncake/3FS/NIXL/AIBrix 后端）

核心文件：
  - python/sglang/srt/mem_cache/hiradix_cache.py  -- HiRadixCache（扩展了 RadixCache）
  - python/sglang/srt/mem_cache/memory_pool_host.py -- L2 CPU 池（2899 行！）
  - python/sglang/srt/mem_cache/hicache_storage.py  -- L3 抽象接口
  - python/sglang/jit_kernel/hicache.py + csrc/hicache.cuh -- GPU I/O 内核

数据移动量降至约 1/7 的原因：

(a) 基数树中的最长前缀匹配
    在任何传输之前，HiRadixCache 会找到最长的连续缓存前缀。仅对缺失的后缀进行重新计算。无需复制完整序列。

(b) 自定义 CUDA 内核绕过 L1 缓存
    hicache.cuh 使用 `ld.global.L1::no_allocate` 和 `st.global.L1::no_allocate` 指令——完全避免 L1 缓存污染。这些内核在 GPU<->CPU 传输中的吞吐量比标准 cudaMemcpyAsync 高约 3 倍。

(c) 计算-传输重叠（逐层流水线）
    当 GPU 计算第 N 层时，第 N+1 层的 KV 缓存正在从 CPU 加载。传输延迟被计算隐藏。

(d) 页面优先内存布局
    `page_first_direct` 将页面的所有层连续分组在 CPU 内存中，实现层级间的单对象零拷贝传输。

(e) 写回策略减少不必要的 I/O
    `write_through_selective` 仅备份热点数据（访问次数超过阈值）。`write_back` 将写入延迟到驱逐时。这意味着冷数据永远不会跨越层级边界。

(f) MLA 优化（DeepSeek 风格）
    对于多层注意力，所有 TP 秩持有相同的 KV 数据，因此只有一个秩执行写回——消除了跨秩的 (TP-1) 倍冗余存储。

========================================================================
2. SWA + HiCache：缓存令牌数为何提升 5 倍
========================================================================

这是最微妙的声明。关键洞察：

  SWA 层仅需滑动窗口大小的令牌数（例如 4096），而非完整序列长度（例如 128K）。

核心文件：
  - python/sglang/srt/mem_cache/unified_cache_components/swa_component.py
  - python/sglang/srt/mem_cache/swa_memory_pool.py
  - python/sglang/srt/mem_cache/swa_radix_cache.py

工作原理：

(a) 双内存池（swa_memory_pool.py）
    SWAKVPool 维护两个独立的分配器：
      - full_kv_pool  （用于全注意力层）
      - swa_kv_pool   （大小小得多，仅滑动窗口大小）
    一个 full_to_swa_index_mapping 张量在两者之间映射。

(b) 基数树中的墓碑标记
    当 SWA 数据从内部节点被驱逐时，component_data[SWA] 变为 None，而全注意力数据保持不变。这意味着 SWA 层可以独立管理其缓存生命周期。

(c) SWA 感知的 HiCache 传输
    在备份到主机时，SWAComponent.build_hicache_transfers() 使用 SWA 池索引创建 PoolTransfer——每个节点仅传输 sliding_window_size 个令牌，而非完整序列。这是 5 倍因子：如果窗口=4096，序列=20480，则传输 4096 而非 20480，每个请求的主机内存和传输量减少 5 倍。

(d) SWA 感知的前缀匹配
    create_match_validator() 将匹配深度限制为 sliding_window_size 个令牌。它不会在树中向上遍历超出窗口覆盖范围。这意味着对于 SWA 层，基数树保持更浅。

最终效果：使用 SWA 时，主机内存为每个前缀节点存储约窗口大小的令牌，而非完整序列。相同的主机 RAM 可以缓存约 5 倍的请求，显著提高命中率。

========================================================================
3. 专家并行优化
========================================================================

核心文件：
  - python/sglang/srt/layers/moe/ep_moe/layer.py  -- DeepEPMoE
  - python/sglang/srt/layers/moe/token_dispatcher/deepep.py  -- DeepEPBuffer
  - python/sglang/srt/batch_overlap/two_batch_overlap.py  -- TBO
  - python/sglang/srt/eplb/eplb_algorithms/deepseek.py  -- EPLB

三项关键优化：

(a) 双批次重叠（TBO）
    将请求拆分为微批次，并在注意力计算与 MoE 全对全分发/组合之间交错执行。使用 YieldOperation 产生点。有效将通信延迟隐藏在计算背后，吞吐量几乎翻倍。

(b) 专家并行负载均衡器（EPLB）
    分析专家激活统计信息，然后使用 balanced_packing() 和 replicate_experts() 在 GPU 之间重新分配热点专家。防止落后 GPU 拖慢整个集群。周期性重新平衡可适应不断变化的流量模式。

(c) 多种分发后端
    DeepEP 常规模式（高吞吐量预填充）与低延迟模式（CUDA Graph 解码）。还有 Mooncake、NIXL-EP、MORI 后端以适配不同硬件配置。

========================================================================
4. 输入长度分桶
========================================================================

SGLang 没有显式的 "length_bucket" 功能。等效功能来自以下文件中的调度策略：
  python/sglang/srt/managers/schedule_policy.py

(a) LPM（最长前缀匹配）调度
    按与基数缓存的最长前缀匹配对待处理请求进行排序。这自然地将共享相似前缀的请求分组——这与相似的有效输入长度相关。

(b) 路由键调度
    按 MoE 路由键相似性对请求分组，将路由到相似专家的请求批量处理。直接提高 MoE 计算效率。

(c) 分块预填充与 max_prefill_tokens
    限制每批次的预填充令牌数（默认 16384）。当按前缀匹配排序时，PrefillAdder 首先适配较短的请求，隐式地按长度分桶。

========================================================================
总结：这对成本为何重要
========================================================================

成本节约来自三个方面：

1. 缓存效率（HiCache + SWA）
   - 1/7 的数据移动 = PCIe/网络带宽消耗减少 7 倍
   - 5 倍的可缓存令牌 = 缓存命中率提高 5 倍
   - 净效果：大多数请求命中 L1/L2 缓存，极少触及 L3
   - 更少的重新计算 = 每个令牌更少的 GPU 时间

2. 吞吐量（EP + TBO + EPLB）
   - TBO 将通信隐藏在计算背后（约 2 倍吞吐量）
   - EPLB 消除集群内 GPU 利用率不均衡
   - 专家复制处理热点专家而无需瓶颈

3. 调度（前缀感知 + 路由键）
   - 将互补的请求分组以最大化缓存复用
   - 防止因批次中包含过多长预填充而导致内存峰值
   - 在避免 OOM 的前提下最大化 GPU 利用率

综合来看，这使得他们能够用更少的 GPU 和更低的带宽处理相同的流量——因此价格下降。