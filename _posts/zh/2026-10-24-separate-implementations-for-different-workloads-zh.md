---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 针对不同工作负载的独立实现
translated: true
type: note
---

## 这两个内核是互不相关的实现，用于*不同*的工作负载

它们并非同一操作（op）的竞争性替代方案——每一个都替换了 vLLM 标准路径中针对特定 shape/regime 的不同部分。这就是为什么彼此之间**没有单一的 if/else 在它们之间做选择**；每个都有自己的 env-gated dispatch 及 fallback。

### `kernels/fp4_gemv/` — W4A4 NVFP4 **GEMV**（MLP linears）
- 计算 `out[t,n] = Σ_g sa·sw · Σ_{i<16} qa[t,16g+i]·qw[n,16g+i]` —— 一个 *linear-layer* 数学核（少量 token `M≤8` × 隐藏维度 `K` × 输出维度 `N`）。
- 替换了 FlashInfer 的 `mm_fp4`（b12x 后端），用于 Qwen3.8-27B 的 **MLP** 在较小 M 时的 down（`N=5120,K=17408`, M≤5）和 gate_up（`N=34816,K=5120`, M≤4）。
- 这是 **decode/MTP-verify** 工作负载——在极少的 token 数量上运行的 GQKV/MLP linears。

### `kernels/fp8attn/` — paged FP8 tensor-core **attention**（KV-cache reads）
- 一个全 flash-attention 风格的内核：FP8 E4M3 QK/PV 在 `mma.sync.m16n8k32.f8f6f4` 上计算，online softmax，paged KV。两个构建版本：8-warp prefill（`ext()`）和 4-warp spec-verify decode（`ext_verify()`，`FP8_NW=4`）。
- 替换了 b12x 的 paged *extend attention* 和 trtllm 的 *xqa decode*，用于 Qwen3.8-27B 的 **full-attention layers**（HQ 24, HK 4, D 256, page 64），去重复 cache reads/repacks。

所以：**fp4_gemv = the linear/MLP phase；fp8attn = the attention phase**。它们属于同一个"heterogeneous-inference"内核套件（都是 sm_120a，都是固定形状的手写 CUDA，带有 JIT loader，都由 `QWEN38_*` 标志激活），但永远不会看到彼此的输入。

### 调度分支

**fp4_gemv** — `vllm/model_executor/kernels/linear/nvfp4/flashinfer.py`：
1. 导入门（第61-66行）：`_QWEN38_GEMV_ON = os.environ.get("QWEN38_FP4_GEMV","0")=="1"` → JIT-loads the extension。
2. `apply_weights`（第474行）：
   ```python
   max_m = _QWEN38_GEMV_MAX_M.get((layer.weight.shape[0], x_fp4.shape[-1]*2), 0)  # (N,K)->M cap
   if (_QWEN38_GEMV_ON and max_m and output_dtype==torch.bfloat16 and x_fp4.dim()==2
           and not nvfp4_weight_padding_bytes(layer)):
       out = torch.ops.vllm.qwen38_fp4_mm(...)
   else:
       out = flashinfer_scaled_fp4_mm(..., backend="b12x")
   ```
3. M 与 b12x 之间的阈值位于自定义 op `_qwen38_fp4_mm` 中（`if 1 <= M <= max_m: gemv else b12x`）——有意放在自定义 op 内，这样 `torch.compile` 就不会专门针对 `M` 进行优化，因为 `M` 每步都在变化。

**fp8attn** — `vllm/v1/attention/backends/flashinfer.py`：
1. 整个 b12x-prefill 路径在 metadata-build time 进行门控（第1903行）：`prefill.b12x = ... if _B12X_PF and not use_dcp and causal else None`。
2. Prefill forward（`_qwen38_b12x_prefill`，第276行）：首先进行 `_FP8EMU` emulation（evaluation），然后 `if _FP8ATTN and page==64 and head_size==256 and num_heads==24 and num_kv_heads==4 and contiguous` → `fp8_extend_batch`；否则使用 b12x plan。
3. Spec-verify decode（第2729行）：`if _FP8DEC and _qwen38_fp8_verify(...)` → 使用 `FP8_NW=4` 构建；`_qwen38_fp8_verify` 对于不适用批次（non-causal, wrong configs, non-contiguous）返回 False，所以它会**自动回退到 `flashinfer_xqa_batch_decode_with_kv_cache`**。

总之：fp4_gemv 和 fp8attn 属于*不同的 pipeline stages*（linear vs attention）；它们之间唯一的联系是相同的 env-flag/KN kernel-suite convention，以及将 b12x/trtllm 作为共享 fallback。