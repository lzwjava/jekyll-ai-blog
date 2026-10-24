---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 延迟GDN状态物化
translated: true
type: note
---

## 什么是 `kernels/gdn_defer/gdn_defer.cu`

一个用于 Qwen3.8-27B GDN（Gated DeltaNet）speculative-decode 路径的 **自定义 CUDA 内核对**，衍生自 vLLM v0.30.0 的 `fused_gdn_decode_kernel.cu`。它是该异构推理项目中的一个优化实验。

### 它要解决的问题

在 stock vLLM 中，GDN MTP（multi-token prediction）解码内核在 **每个** speculative token 后写入完整的 fp32 循环状态 —— 每个序列每层有 `k+1` 个槽位，每个 3 MiB —— 但只有 `accepted-1` 槽位会在下一步被读取。性能分析显示，这些存储操作在 **down GEMM** 上（c=4 时为 37→52 µs）成为了浪费的 DRAM 写入流量。

### 修复方案：延迟状态存储

**Kernel A — `gdn_mtp`**（每层，在 forward 中）：执行与 stock 版本完全相同的计算，但不是存储 k+1 个状态槽，而是保存稍后重放所需的 *ingredients*：

- 每个 token 的归一化 `k` (fp32)、`v` (bf16)、decay 和 beta（k+1 个槽位 × 16 KiB 对比 3 MiB）
- `meta`：epoch stamp、source slot、token count、destination slots
- 这些缓冲区具有固定地址，因此 forward 过程在 **CUDA 图中保持可捕获**（epoch 从设备内存读取）。

**Kernel B — `gdn_materialize`**（每步一次，所有层，*在* 接受计数已知且 vLLM 的 mamba 后处理之前）：重新加载源状态，仅使用相同的每 token 更新代码重放已接受的 token，并仅存储最终的槽位 —— `slot[accepted-1]`，以及在 align-mode 后处理复制块边界状态情况下的 `slot[bias]`。

### 关键细节

- `token_update<>` 是模板化的，被两个内核共享，因此状态运算（FMA contraction，shuffle order）是 *相同的指令序列* —— 与 stock 版本比特一致。
- `kDefer=false` 编译未更改的 stock 内核，用作单元测试的参考（比特完全相同的输出；JIT 脚本强制使用 `--use_fast_math` 以匹配 vLLM 的构建）。
- 支持两种运行变体：V1（per-batch-row counts）和 V2（`idx_map` → request slot，`precomputed` counts）。
- 在不可能的接受计数上使用 `__trap()` —— 拒绝无声地写入错误状态。

### 连接方式（in `registry.py`）

仅在 `QWEN38_GDN_DEFER=1` + spec decode + TP=1/PP=1 时激活：

- `GdnDefer.__init__` 分配所有固定地址缓冲区
- `begin_step` 增加 device epoch 并写入 spec-row → batch-row 映射
- `decode(...)` 每层运行 kernel A
- `materialize(...)` 在接受计数已知后运行 kernel B

要点：**“不要存储所有 speculative token 的 3 MiB 循环状态 —— 保存 16 KiB 的重放 ingredients，然后只实例化那些实际会被读取的状态。”**
