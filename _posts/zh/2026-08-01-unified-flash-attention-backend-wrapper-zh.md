---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 统一闪存注意力后端封装器
translated: true
type: note
---

`nanochat/flash_attention.py` 是这个 GPT 风格训练/推理代码库中一个**围绕三种注意力后端的统一封装器**。其目标是：提供与 FlashAttention-3 接口完全匹配的单一 API，并自动选择最佳可用内核。

## 功能说明

**后端自动检测（在导入时）：**

1. **FA3** (`_load_flash_attention_3`) — 尝试加载内核包。在 Hopper 架构（sm90，`major == 9`）上优先使用 `varunneal/flash-attention-3` 的 HF 内核；在其他架构上尝试 `kernels-community/flash-attn3`。若遇任何失败（无 CUDA、导入错误等）则返回 `None`。
2. **FA2** (`_load_flash_attention_2`) — 导入 `flash-attn` pip 包。同时支持 NVIDIA CUDA 和 AMD ROCm。
3. **SDPA 后备方案** — 纯 PyTorch 的 `scaled_dot_product_attention`，通用性最强。

**选择逻辑** (`_resolve_impl`)：

- 环境变量 `NANOCHAT_FORCE_SDPA=1` 强制使用后备方案。
- 测试覆盖变量 `_override_impl` 可强制指定 `'fa3'`/`'fa2'`/`'sdpa'`（会断言后端实际存在）。
- 自动模式：仅在 Hopper 架构且计算数据类型为 bf16 时优先使用 FA3，否则使用 FA2，再否则使用 SDPA。
- 会在导入时打印当前激活的后端：`✓ 使用 Flash Attention 3（Hopper GPU）`等。

**公共 API**（以 `flash_attn` 形式导出，为 `SimpleNamespace` 对象）：

- **`flash_attn_func(q, k, v, causal, window_size)`** — 训练路径，无 KV 缓存。对于 SDPA，会将输入从 `(B,T,H,D)` 转置为 `(B,H,T,D)` 并委托给 `_sdpa_attention`。
- **`flash_attn_with_kvcache(q, k_cache, v_cache, k, v, cache_seqlens, causal, window_size)`** — 使用预分配缓存的推理路径。FA3/FA2 会将 `k, v` 原地写入缓存；SDPA 后备方案则手动模拟此过程（`k_cache[:, pos:pos+T_new] = k`），然后截取缓存至 `end_pos` 长度并执行注意力计算。

**`_sdpa_attention`** 是其中的关键部分——它模拟了 SDPA 原生不支持的一些 FA 语义：

- 在全上下文因果场景下，且当窗口覆盖全部内容且 `Tq == Tk` 时，直接使用标准因果注意力。
- 单 token 生成时：截取 KV 窗口尾部而非构建掩码。
- 其他情况：为**分块推理**（`Tq != Tk`，即 `is_causal` 无法与缓存位置对齐）构建显式布尔掩码，并结合左侧滑动窗口约束 `row_idx - col_idx <= window`。

**`_fa2_window_size`** — 将 FA3 的 `(-1, -1)` 约定转换为 FA2 期望的格式。

## 使用位置

`nanochat/gpt.py` 会导入 `flash_attn` 并调用 `flash_attn.flash_attn_func(...)`（第 110 行，训练）或 `flash_attn.flash_attn_with_kvcache(...)`（第 114 行，生成），因此模型其余代码无需关心具体使用哪个后端。

## 值得注意的潜在问题

- `_load_flash_attention_2` 导入了 `flash_attn_varlen_func` 但从未使用（死代码导入）。
- SDPA 的 KV 缓存路径假设批次中所有 `cache_seqlens` 一致（使用 `cache_seqlens[0].item()`），这在批次解码中存在不同序列长度时会产生错误。
- FA3 的 Hopper 分支仅对 bf16 生效——即使 FA3 支持 fp16，Hopper 上的 fp16 用户会静默地回退到 FA2/SDPA。
