---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton行Argmax内核
translated: true
type: note
---

## `kernels/decode_fuse/argmax.py` 是什么

一个用于 **MTP draft head** 的 **Triton row-argmax kernel** — 在推测性草稿步骤结束时，这个核函数负责选取 `argmax(logits)`，取代了 PyTorch 的 `logits.max(dim=-1).indices`。

### 它解决的问题

现有的 `logits.max(dim=-1)` 是一个 **每行一个 CTA 的归约操作**。在这个模型的词表（98,304 列）上，速度很慢 — 头部引用了 PRO 5000 上朴素路径约 23 µs 的数据。替代方案是一个 **2 阶段拆分归约：阶段 1 为 4096 宽的块，阶段 2 为一个小的合并核函数**，它将归约并行化到比行数多得多的 CTA 上。

### 核函数结构

**阶段 1** `_argmax_stage1` — 网格 `(M, nchunk)`，每个（行，块）一个 CTA：
- 将其 4096 元素的块（行末尾之后的部分用 `-inf` 掩蔽）加载到 fp32。
- 计算块的第一个最大索引 *以及* 块是否包含 NaN：
  - `first_nan = min(offs where isnan)` — NaN 位置
  - `m = max(vf)`，其中 NaN 已被替换为 `-inf`，因此它们不会污染最大值
  - `i = min(offs where vf == m)` — 块最大值的 **第一个** 索引（平局 → 最小索引）
- 存储每个块的 `(value, index)` — 或者如果发现了 NaN 则存储 `(NaN, first_nan)`。

**阶段 2** `_argmax_stage2` — 网格 `(M,)`，每行一个 warp：
- 加载所有 nchunk 个 `(value, index)` 对。
- 包含 NaN 的块胜过一切（`nan_ix = min` 携带 NaN 的块索引 → 最早的块获胜，与 torch 一致，其中第一个 NaN 被视为最大值）。
- 否则 `m = max(vals)`，`i = min(idx where vals == m)` — 由于块按索引顺序排列，**最低的全局索引赢得平局**，完全像 `torch.max().indices`。
- 写入 `int64` 全局列索引。

### 为什么 NaN 处理很重要

CUDA 图填充行可能包含 **NaN logits**，而 `torch.max` 的语义是 *NaN 计为最大值* 且 *第一个* NaN 获胜。因此这不仅仅是“找到最大值” — 它必须再现 torch 的确切平局/NaN 行为（文档字符串声称“与 `torch.max(dim=-1).indices` 结果相同”，并且它被用作直接替代）。

### 集成方式

`vllm/model_executor/layers/logits_processor.py`：
1. 由 `QWEN38_ARGMAX=1` 控制（在 `scripts/duo.sh` 中为 SPEC 布局设置，同时设置了 `DRAFT_VOCAB`）。
2. 该函数通过 `direct_register_custom_op("qwen38_row_argmax", ...)` 注册，并带有一个 `fake_impl`，它返回一个空的 `int64[M]` 张量用于 torch.compile。
3. 仅在 `tp_size == 1` 且 logits 为 2-D 连续（`line 247`）时使用 — 否则使用现有的 `logits.max(dim=-1)`。局部索引通过 `org_vocab_start_index` 偏移以获取全局词表索引。

一个很好的特性：它位于 `kernels/decode_fuse/` 目录下（一个纯 Python 的 Triton 负载，没有 `.cu` 文件），并通过 `sys.path` 和 `QWEN27B_KERNELS` 环境变量加载，与其他 JIT 核函数相同的约定 — 但使用 Triton 而非 CUDA 扩展。