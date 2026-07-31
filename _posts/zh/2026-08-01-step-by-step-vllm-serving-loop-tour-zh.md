---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 逐步 vLLM 服务循环之旅
translated: true
type: note
---

以下是我推荐的断点游览。此代码库是一个最小化的 vLLM 克隆，目标是观察**服务循环**：请求如何流经调度 → KV 缓存分配 → 模型前向 → token 追加，以及 prefill 和 decode 如何交错（连续批处理）。

最好通过已经逐步驱动循环的实验（而不是一次性的 `run_inference.py`）来运行：

```bash
python3.12 experiments/04_scheduler_watch.py
```

它会通过打补丁的日志打印调度器跟踪信息，这是断点的完美脚手架。

---

## 游览（按此顺序）

### 1. 外层循环——先看整个管道
- **`nanovllm/engine/llm_engine.py:66`**（`LLMEngine.step`）——*最*重要的停靠点。整个服务系统就是这 4 行管道：`schedule → run → postprocess`。在这里设置断点，你将看到每个阶段每次迭代都触发。
- **`llm_engine.py:76`**（`generate`）——主要的 `while not self.is_finished()` 循环，调用 `step()`。观察 `is_prefill`/`num_tokens` 如何在 prefill（正数）和 decode（负数）步骤之间切换。

### 2. 调度器——"连续批处理的啊哈时刻"
- **`nanovllm/engine/scheduler.py:27`**——prefill 循环。检查 `self.waiting` 和 `self.running` 双端队列，以及 `num_batched_tokens` 的累积。
- **`scheduler.py:46`**——`seq.num_scheduled_tokens = min(num_tokens, remaining)`。观察当 `max_num_batched_tokens` 被超过时，长提示如何被**分块**到多个步骤（这就是分块 prefill）。
- **`scheduler.py:58`**——decode 循环。此时等待的序列停止进入，运行的序列被选中，每个序列一个 token（`num_scheduled_tokens = 1`，第 67 行）。
- **`scheduler.py:60` / `preempt`（第 73 行）**——抢占，仅在 KV 缓存压力高时触发。运行实验 `05_kv_cache_pressure.py` 如果你想看到它触发。

### 3. KV 缓存块管理——PagedAttention 核心
- **`nanovllm/engine/block_manager.py:52`**（`can_allocate`）——前缀缓存命中检测（哈希查找）和空闲块计数检查。
- **`block_manager.py:69`**（`allocate`）——为序列分配块；注意 `seq.block_table`（逻辑→物理映射）。这是 vLLM 的反碎片技巧——块**不需要**是连续的。
- **`block_manager.py:101` / `105`**（`can_append` / `may_append`）——微妙的"仅在跨越块边界时增长块表"逻辑（`len(seq) % block_size == 1`）。
- **`block_manager.py:92`**（`deallocate`）——引用计数和在完成/抢占时释放。

### 4. 张量准备——最棘手的账本管理
- **`nanovllm/engine/model_runner.py:137`**（`prepare_prefill`）——检查 `slot_mapping`（扁平的 KV 槽索引 = `block_id * block_size + offset`）、`cu_seqlens_q/k`（变长批处理编码）和 `block_tables`。
- **`model_runner.py:178`**（`prepare_decode`）——1 token decode 情况下的相同思路。这里 vLLM 的每个序列账本管理变得可感知。

### 5. KV 实际写入/读取的时刻
- **`nanovllm/layers/attention.py:158`** → `store_kvcache`（第 9 行）——通过 `slot_mapping` 看到 KV 缓存写入。
- **`attention.py:194`**（`_decode_forward`）→ `_gather_kv_from_cache`（第 35 行）——看到读取：迭代 `block_tables` 从物理块中获取过去的键/值。
- 在这些点检查 `Sequence` 字段（`num_cached_tokens`、`num_scheduled_tokens`）——这就是使切片工作正常的原因。

### 6. 闭合循环
- **`scheduler.py:79`**（`postprocess`）——token 追加，EOS/最大长度完成检查，块释放，`running.remove`。结束于序列在 `Sequence` 中开始的地方（`sequence.py:24`）。

---

在停靠点 2–