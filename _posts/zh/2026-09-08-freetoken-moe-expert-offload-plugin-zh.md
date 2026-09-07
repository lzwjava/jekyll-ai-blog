---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeToken MoE专家卸载插件
translated: true
type: note
---

这是一个针对 **FreeToken**（一个 LLM serving/inference engine）的 patch plugin。下面介绍该项目的逻辑、其 Triton 用法，以及为什么 GLM-5.3（“glm5_next”）和 DeepSeek-V4-Flash（“deepseek_v4”）会放在同一个仓库中。

## 项目本质

这个仓库要解决的核心难题是：

> 在**一张** 96 GB GPU（RTX PRO 6000 Blackwell）上 serve 前沿规模的 MoE checkpoints，其中仅 *experts* 就有 130–181 GB，且驻留在 host RAM 中。真正的瓶颈是 PCIe Gen5（约 50 GB/s），而不是 compute。

因此，这里的一切都围绕 **MoE expert offload cache**：一个存放“热” expert weights 的 VRAM slot-cache，其余部分固定在 host memory 中，按需通过 PCIe 获取。关键指标是减少 *per-token 移动的 bytes*，并在 bytes 移动时让 GPU 保持忙碌。

FreeToken v0.1.2（baseline）已经通过这种 offload architecture 支持 DeepSeek-V4。本仓库是一组 **53 个 unified-diff patches + 19 个新的 overlay files**，由 `install.sh` 应用到干净的上游树（`python/freetoken/...`）上，以及 `examples/` 中的 launch scripts。仓库特意*不包含上游代码*，只包含 deltas——因此 `README.md` 称其为“patch plugin”。

## 主要逻辑

### 1. GLM-5.3-Flash model port（`overlay/freetoken/models/glm5_next/`）
这是主要交付物（见 README headline）。GLM-5.3-Flash 是一个 45-layer hybrid-attention MoE：
- **34 个 KDA layers**（`attention.py` 中的 `KdaAttention`）——gated-delta linear attention（64 heads × 128 dim，short causal conv，lower-bounded forget gate，delta rule），通过上游 `fla` kernels `chunk_kda` / `fused_recurrent_kda` 计算。
- **11 个 MLA + DSA layers**（`FullAttention = GlmMoeDsaAttention`）——Multi-head Latent Attention 加上带 Lightning indexer + k-pool compressor 的 DeepSeek Sparse Attention。注意这里的 MLA 是 NoPE（`qk_rope_head_dim == 0`）。
- **mHC（manifold-constrained Hyper-Connections）**——每个 decoder layer 保留 *4 条 residual streams*（`hc_mult=4`，sinkhorn iters），并通过 per-sublayer matrices 混合它们（`model.py: hc_pre/hc_post`，`hc_head` = unweighted mean）。这些 knobs 与 DSV4 完全相同，因此它**原样复用 DSV4 的 hyper-connection kernels**——这是两个模型共享此仓库的第一个迹象。
- **NVFP4 MoE**——288 个 routed experts，top-8，sigmoid noaux_tc router，1 个 shared expert，前 3 层 dense。Experts 是 ModelOpt-NVFP4（packed uint8 + FP8 block-16 scales + fp32 global scales），总计 181 GB。

### 2. VRAM/host 拆分——decode path 的核心
`weight.py` 决定每个 expert layer 放在哪里：
- **Non-resident layers**（默认 45 层中的 37 层）→ 它们的 expert banks 是 *host-pinned*，计算时通过将选中的 experts 取入 **VRAM slot-cache**（LRU/LFU eviction），然后运行 grouped Triton GEMM/GEMV。
- **Resident layers**（`experts_resident.py`，由 `FREETOKEN_GLM5_RESIDENT_LAYERS` 控制，例如 `3-6,8-11`）→ 完整 packed banks 永久驻留在 GPU 上；它们的 PCIe 流量为零。根据实测 fetch hotness 选择（miss curve 呈 U 形）。
- 所有必须保持 dense 的非-expert 内容都在 GPU 上运行，可选择重新量化为 FP8（`attention.py`/`mlp.py`，decode 约 +28%）。

每个 decode step 的流程是：router scores → top-8 expert ids → 一个 **slot-cache “ensure” kernel**（见下文）决定 hits 与 misses 并选择 eviction victims → 缺失 experts 的 H2D copies 在 **side CUDA stream** 上运行 → expert GEMMs 等待 copy event（`spec_prefetch.py` 将 copy 隐藏在下层工作之后）。整个 decode step 是 **CUDA-graph captured**，因此每个自定义 kernel 都必须遵守 graph discipline：固定 shapes、无 host sync、hot path 中无 host-side branches。

### 3. Speculative expert prefetch（`overlay/freetoken/moe/spec_prefetch.py`）
由于 routing 在一定程度上可预测，layer *L* 会在自己的 hidden state 上运行 layer *L+hop* 的真实 gate，预测 top-P experts，并提前预热 slot-cache——类似 Mixtral-offloading 风格。已扫描到 P=4/hop-1。对于 GLM，routing 是“flat”的（tokens 之间的 experts 重叠度低），这解释了 concurrency ceiling：concurrent streams 只会增加 PCIe bytes。

### 4. Serving-level 特性
- **Radix/prefix KV cache**，对 image spans 使用 content-hash keys（media prefix reuse），以及一个 **KDA track-snapshot writer**，使缓存的 mid-prefill reuse points 携带真实的 recurrent state（一个被发现并修复的 correctness bug，记录在 README 中）。
- **On-demand prefill** 用于短 prompts（`FREETOKEN_PREFILL_ONDEMAND_TOKENS`）：不是逐层 streaming 整个 prompt，而是作为一次 decode-style pass 运行 → 对于 10 tokens，TTFT 从 2.1 s 降至 0.59 s。
- **Vision** tower port（0.6B ViT）+ vendored 的与 HF-identical 的 image preprocessing，默认通过 env 开关关闭。
- 为 DSV4 实现 long-context stabilization（prefill chunk cap、sliced indexer top-k、staging slab），使 236K-token cold prefills 不会 OOM。

### 5. DSV4 线是同一套打法，第二个 model
`MANIFEST.md` 中的“DeepSeek-V4-Flash (DSV4) line”：native FP8/MXFP4 experts，43 layers，DSA compressor/indexer + mHC，约 6000 个 experts 常驻，约 75 GB。在同一张单 GPU 上用相同的 offload logic 服务它，通过相同的技术（fused route、FP8 GEMVs、fused compressor decode step、rms-in-mix fusion）从 51 tok/s 提升到 64 tok/s。两个 model 无法同时运行（serve scripts 会停止彼此的 systemd service），因此 DSV4 和 GLM5 是**同一台机器上的两个可互换 workloads**。

## Triton 的使用方式

Triton 恰好扮演两个角色：**(a) 用单个 fused kernel 替代 multi-kernel eager chains**（以削减 launch overhead 和 intermediate memory traffic），以及 **(b) 实现上游仅以 eager form 或 cuBLAS 形式存在的 cache/control-plane kernels**。全部位于 `overlay/freetoken/kernel/triton/`：

| Kernel | 它融合/替代了什么 |
|---|---|
| `fused_route.py` | Router epilogue：sigmoid（或 sqrt-softplus）+bias+**top-k+renorm+scale**（约 8 次 launches × 约 40 个 MoE layers/step → 1 个 kernel）。迭代式 `tl.argmax`，带 first-index tie-break，以精确匹配 `torch.topk` semantics。 |
| `kda_gate.py` | KDA forget/input gate math（5 个 GEMVs + 约 7 个 elementwise → 2 个 GEMVs + 1 个 fused elementwise kernel）。 |
| `dsv4/hc_norm.py` | mHC pre-norm：在一个 CTA-per-token kernel 中完成 fp32 cast + sum-of-squares + rsqrt，并将 rsqrt 折叠进 mix GEMV 的 epilogue（无 atomics → deterministic）。 |
| `dsv4/comp_step.py` | DSV4 的 fused compressor decode step——每个 tier instance 一次 launch 内完成 read/scatter/pool/promote/write 的 register roll，tile-loaded pool rows（原先是一条 52 µs 的 serial load chain）。 |
| `dsv4/hc_fused.py` | 将 mHC pre-mix rms 折叠进 mix GEMV。 |
| `kda_gate.py`, `fused_route.py` (ACT constexpr) | 在两个 model 之间共享，只要 math 匹配。 |

此外，patch set 还添加了 GPU-side cache-control kernels，例如 LFU admission kernel（`lfu_ensure.py`——saturating 3-bit frequency counters + `(freq<<48)|usage` composite keys，single-CTA register-resident scan 约 3000 个 slots，并定期进行 halving decay sweep），以及对上游 `lru_ensure`/`fast_index_copy` 的 tweaks（device-side H2D slot copy plans）。

在每个 kernel docstring 中反复出现的设计约束：
- **Deterministic**：尽可能不使用 atomics（与它所替代的 cuBLAS chain 相比，run-to-run 可重现）；
- **Numerics-bit-compatible**：sigmoid/topk rounding 必须在 ≤1 ulp 内匹配 ATen——本仓库的质量标准是与 HuggingFace reference 实现*逐 token*相等（48/48 steps），因此 kernels 会对照 eager path 的 rounding order 进行验证；
- **CUDA-graph-safe**：固定 shapes、无 host sync、capture 期间无 unpinned host→device copies；每次 replay 时 *刷新* 的 device buffers（例如用于所有 34 个 KDA layers 共享的 `idx.long()` cast 的 `decode_memo`）；
- **Auto-fallback**：例如，b12x (cuBLAS) MoE path 因 epilogue 缺少 swiglu clamp 而被 GLM 拒绝；engine 会自动解析到 Triton path。

## 为什么两个 model 放在同一个仓库？

1. **DSV4 是 template。** FreeToken upstream 发布的 DeepSeek-V4-Flash 正好具备 GLM-5.3 所需的机制：mHC hyper-connections、MLA + DSA sparse attention、linear-attention state pool、quantized-expert offload banks。GLM-5.3-Flash 在结构上几乎相同（mHC 使用*相同*的 `hc_mult=4`/sinkhorn knobs，hybrid KDA/MLA-DSA attention，dense head layers + MoE tail，FP8-class expert quantization）。overlay 中充满了“reuse map”注释：GLM-5.3 复用 DSV4 的 hc kernels，GLM 的 full-attention layers *就是* 上游的 `glm_moe_dsa` attention 原样，DSA/MLA KV pool 也原样服务于 GLM。因此，porting GLM 主要意味着编写 weight-loader + glue，而不是 engine code。

2. **相同的 hardware problem，同一台机器。** 两者都是“在一张 96 GB 卡上运行数百 GB experts，并采用 host offload”的 workloads。所有核心优化（fused route、resident-layer split、speculative prefetch、FP8 decode、radix/prefix cache、chunked prefill）都适用于两者，而且许多 kernels 确实是字面共享的（`fused_route.py` 通过 constexpr `ACT` 同时处理 GLM 的 sigmoid flavor 和 DSV4 的 sqrt-softplus）。这台机器运行两者——`serve_full.sh`（glm5-flash）和 `serve_dsv4.sh`（dsv4-flash）是同一 GPU 上的两个互斥 systemd services。

3. **不同的 optimization maturity，同一个 artifact。** README/MANIFEST 的 headline 是 GLM-5.3 adaptation（git history 只从 DSV4 round 3 开始，所以 GLM 工作早于 repo snapshot）；DSV4 line 随后成为第二条、迭代更快的 optimization track（55 → 64 tok/s，然后是 deep-context stabilization）。将两个 model 都保留在 patch set 中，意味着作者可以服务请求所针对的任一 model，而无需重构树，并且一条线上的每个 kernel improvement 都会在另一条线上衡量。

总结：**DSV4 为项目提供了一个经过验证、注重 byte-billing 的 offload architecture 供复制；GLM-5.3 是行使该架构的 flagship port；仓库同时发布两者，因为它们共享约 80% 的机制以及相同的 single-GPU hardware reality。**