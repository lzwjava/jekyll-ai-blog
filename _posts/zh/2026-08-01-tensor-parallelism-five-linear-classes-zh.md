---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 张量并行：五个线性类别
translated: true
type: note
---

共有 5 个线性类，它们存在的唯一原因就是**张量并行**——将一个大矩阵乘法拆分到多个 GPU 上。它们之间的区别仅在于：

1. **对哪个权重维度进行分片**（行或列）
2. **完整检查点权重如何加载/重新分片到每个 GPU 的本地切片**（`weight_loader`）
3. **前向传播是否需要 `dist.all_reduce`** 来合并部分结果

以下是详细说明：

---

## `LinearBase` — 共享骨架

持有 `weight`（+ 可选 `bias`），记录 `tp_rank`/`tp_size`，并为每个参数附加一个 `weight_loader` 钩子。它**不执行实际计算**——`forward` 抛出 `NotImplementedError`。其他所有类都继承自它。

## `ReplicatedLinear` — 无分片

最简单的情况：每个 GPU 都拥有**完整的**权重。`weight_loader` 只是复制整个检查点张量；`forward` 就是普通的 `F.linear`。用于嵌入/输出头或不值得拆分的小型投影。

## `ColumnParallelLinear` — 列并行

对**输出**维度进行拆分：每个 GPU 持有 `output_size / tp_size` 列，因此 `weight` 的形状为 `[out/tp, in]`。

- `weight_loader`：从完整检查点权重中取出输出维度上 `rank * shard_size : (rank+1) * shard_size` 的切片。
- `forward`：不需要通信——每个 GPU 计算自己的列，稍后拼接起来。

## `MergedColumnParallelLinear` — 融合的两个列并行

一个“融合”的列并行类，用于 MLP 中的 **gate_up_proj**：一个权重矩阵包含两个逻辑投影（`gate` + `up`，每个大小为 `intermediate_size`），它们被分片*并*合并成一个本地张量。

- `weight_loader(param, loaded_weight, loaded_shard_id)` 接受额外的 `loaded_shard_id`（0 或 1），用于判断这个检查点切片属于合并后本地权重的哪一半，以及 TP 分片偏移量落在其中的位置。

## `QKVParallelLinear` — 特殊的融合类

同样是列并行，但用于**带有 GQA 头分片的 Q/K/V**。本地输出为 `(q_heads + 2*kv_heads) * head_dim`——注意：当 `total_num_kv_heads < total_num_heads`（GQA）时，**Q 头在 GPU 间分片，但 KV 头是复制的**。这之所以成立，是因为要求 `total_num_kv_heads` 能被 `tp_size` 整除。

- `weight_loader(param, loaded_weight, loaded_shard_id)` 中 `loaded_shard_id ∈ {"q", "k", "v"}`：Q、K、V 检查点切片各自映射到单个合并本地权重中的不同偏移量。
- 在前向意义上它也是普通的列并行——不需要 all-reduce。

## `RowParallelLinear` — 行并行

对**输入**维度进行拆分：每个 GPU 持有 `[out, in/tp]`，计算部分输出。

- `weight_loader`：对输入维度（dim 1）进行切片。
- `forward`：**这是唯一需要 `dist.all_reduce(y)`** 来对所有 rank 的部分结果求和的类。另外，偏置只会在 `tp_rank == 0` 时添加（然后 all-reduce 会正确地将其求和）。

---

## 它们在模型中的配合方式

在 `nanovllm/models/qwen3.py` 中，采用了标准的 Megatron 风格 TP 设置：

| 模型组件 | 类 | 原因 |
| --- | --- | --- |
| `qkv_proj` | `QKVParallelLinear` | 一个融合的 Q/K/V 矩阵乘法，头在 GPU 间分片 |
| `o_proj` | `RowParallelLinear` | 注意力输出需要在 GPU 间求和 → 行并行 + all-reduce |
| `gate_up_proj` | `MergedColumnParallelLinear` | 融合的 gate+up 矩阵乘法，列并行 |
| `down_proj` | `RowParallelLinear` | MLP 输出，行并行 + all-reduce |

因此，`ColumnParallel`（无通信）→ `RowParallel`（all-reduce）这一对构成了经典的 Megatron-LM `f`/`g` 配对：列并行产生分片，行并行消费它们，每个行并行层进行一次 all-reduce，从而免费获得通信高效的 TP。`ReplicatedLinear` 是为不需要分片的层提供的逃生出口。

如果你想看看实际运行效果，可以运行 `python3.12 experiments/04_scheduler_watch.py`——不过注意 TP 代码路径只在 `tp_size > 1` 时激活；在单 GPU 上，所有 rank 都是 rank 0，all-reduce 成为空操作。
