---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang中的上下文并行与KV缓存重分片
translated: true
type: note
---

**问题：** 在 SGLang 的上下文中，这种带有 KV 缓存重分片的 CP（上下文并行）设计意味着什么？

**答案：**

让我将其与 SGLang 的实际代码库和架构联系起来。

## 描述的内容

这描述的是 **上下文并行（Context Parallelism, CP）**——一种用于 **长上下文推理** 的并行策略，其中单个序列沿着序列维度被分割到多个 GPU 上，这与 TP（分割权重矩阵）或 DP（分割批次）不同。

---

## SGLang 的当前状态（截至 2025 年中）

SGLang 一直在积极添加 CP 支持。该讲座描述了 **三个阶段**：

### 阶段 1：纯 TP（基准）

```
GPU0: 完整 KV, heads 0..H/8
GPU1: 完整 KV, heads H/8..H/4
...
# 注意力之后对隐藏层进行 All-reduce
```

### 阶段 2：CP=8 且使用 All-gather（当前 SGLang 模式）

```python
# 概念上 SGLang 当前的做法：
# 序列分割：rank0 拥有 tokens [0, seq_len//8)
#             rank1 拥有 tokens [seq_len//8, 2*seq_len//8) ...

# 注意力之前：
kv_cache = all_gather(local_kv, group=cp_group)  # 从所有 rank 收集完整 KV
q = all_gather(local_q, group=cp_group)           # 每个 rank 需要完整上下文

# 注意力（每个 rank 计算完整 KV 上的注意力，但仅针对其 Q 切片）
out = flash_attn(local_q, kv_cache.k, kv_cache.v)

# 注意力之后：reduce
out = reduce_scatter(out, group=cp_group)
```

问题：**KV 缓存被完全复制了 N 次**（每个 CP rank 一次）。对于 CP=8，那就是 8 倍的 KV 内存开销。

### 阶段 3：CP=8 且使用自动调度 + 重分片（优化）

```
# 热 tokens（例如系统提示前缀、前 2 个 tokens）：
#   在所有 rank 上复制（避免在每个解码步骤中获取）

# 冷 tokens：
#   在 rank 之间分片 — rank i 持有 pages [i::CP_SIZE]
#   CP=4 → 每个 rank 存储 1/4 的冷 KV pages

# 在注意力层 L 之前：
# 与层 L-1 的计算重叠：
remote_kv = async_all_gather(sharded_kv_pages, group=cp_group)
compute(layer_L_minus_1)          # 与上述并行运行
sync(remote_kv)                   # 此时，预取已完成
compute_attention(layer_L, remote_kv)
```

---

## 在 SGLang 源码中的位置

```bash
# 关键文件：
python/sglang/srt/layers/attention/
├── triton_attention_backend.py
├── flashinfer_attention_backend.py

python/sglang/srt/model_executor/
├── model_runner.py          # CP 组初始化
├── forward_batch_info.py    # 序列分割逻辑

python/sglang/srt/distributed/
├── parallel_state.py        # CP 进程组管理
```

SGLang 中的 CP 组初始化遵循 Megatron 风格：

```python
# parallel_state.py
def initialize_model_parallel(
    tensor_model_parallel_size=1,
    context_parallel_size=1,   # <-- 这就是 CP
    ...
):
    # CP 组：共享一个序列的 ranks
    for i in range(num_cp_groups):
        ranks = range(i * cp_size, (i+1) * cp_size)
        group = torch.distributed.new_group(ranks)
```

---

## KV 重分片实践

```python
# 概念性的重分片逻辑（讲座中描述的阶段 3）：

class CPKVCache:
    def __init__(self, cp_rank, cp_size, num_hot_tokens=2):
        self.cp_rank = cp_rank
        self.cp_size = cp_size
        self.num_hot_tokens = num_hot_tokens

    def should_replicate(self, page_idx):
        # 热 pages 在所有地方复制
        return page_idx < self.num_hot_tokens // PAGE_SIZE

    def owner_rank(self, page_idx):
        # 冷 pages 按轮询方式分片
        return page_idx % self.cp_size

    def local_pages(self, all_pages):
        return [p for p in all_pages
                if self.should_replicate(p) or self.owner_rank(p) == self.cp_rank]

    async def prefetch_for_attention(self, needed_pages):
        remote = [p for p in needed_pages
                  if not self.should_replicate(p)
                  and self.owner_rank(p) != self.cp_rank]
        return await async_all_gather(remote, group=cp_group)
```

---

## 通信数学（来自讲座）

对于一个 330B 模型，seq_len=K，TP=8：

| 配置 | 通信量 |
|------|--------|
| 纯 TP=8 | `100 * 2` 单位（注意力前后 all-reduce） |
| CP=8，all-gather（当前） | 类似，但增加了 KV all-gather 开销 |
| CP=8，自动调度优化 | ~`102 MB` 总计 — **减少约 50%** |

关键洞察：**自动调度将注意力两侧的两个显式 all-gather/reduce-scatter 调用转换为单个融合的异步操作**，通过 `osm`（单侧消息 / NVSHMEM 风格）通信内核与前一层的计算重叠。

---

## 这对你的意义

如果你在配有 RTX 4070 的工作站上运行长上下文的 SGLang，或者在 MI300X 上运行 330B+ 模型：

```bash
# 使用 CP 启动 SGLang（当前 all-gather 模式）：
python -m sglang.launch_server \
  --model deepseek-v4 \
  --tp 8 \
  --context-parallel-size 8 \   # <-- 此标志
  --max-model-len 128000

# 重分片优化（阶段 3）将让你：
# - 以相同的 KV 缓存内存运行 8 倍更长的序列
# - 在注意力层上减少约 50% 的 GPU 间带宽
```

重分片的 PR 可能正在 SGLang 中进行中——值得关注：

- [github.com/sgl-project/sglang](https://github.com/sgl-project/sglang) — 在最近的 PR 中搜索 `context_parallel` 或 `cp_size`

---

**总结：** 讲座描述了 SGLang 从朴素 CP（KV 复制 N 次 = N× 内存浪费）到智能 CP（KV 分片，热页复制，冷页与计算重叠异步预取）的路线图。`~102MB` 的目标是优化后的稳态跨节点带宽，而未经优化时大约是它的两倍。
