---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mini-Sglang中的MoE流水线
translated: true
type: note
---

以下是 mini-sglang 中 MoE 的工作原理，从模型到内核的端到端追踪。

## 1. 模型层 — router + experts（`models/utils.py`，`models/qwen3_moe.py`）

```python
class MoEMLP(BaseOP):
    def __init__(self, config):
        self.experts = MoELayer(num_experts=..., top_k=..., hidden_size=..., ...)
        self.gate = LinearReplicated(hidden_size, num_experts, has_bias=False)

    def forward(self, hidden_states):
        router_logits = self.gate(hidden_states)          # [num_tokens, num_experts]
        return self.experts(hidden_states, router_logits)  # MoE computation
```

每个解码器层的 MLP 包含一个 **router**（一个复制的线性层，为每个 token 的每个 expert 生成一个 logit）和一个 **MoE layer**。router 是 `LinearReplicated`，意味着每个 TP rank 计算相同的 logits——路由决策是共享的。

## 2. 层级别 — expert 权重（`layers/moe.py`）

`MoELayer` 将 expert 权重保存为原始张量（没有 `nn.Module` 包装——这些权重会被特殊分片/加载）：

- `gate_up_proj`：`[num_experts, 2·intermediate_per_partition, hidden]` — SwiGLU 的 **融合 gate+up projection**
- `down_proj`：`[num_experts, hidden, intermediate_per_partition]`

**张量并行**：`intermediate_size` 通过 `div_even(intermediate_size, tp_size)` 分割，因此每个 rank 持有 **每个 expert** 的一个切片。前向调用可插拔的 `ctx.moe_backend.forward(...)`，然后执行 `all_reduce` 来合并跨 rank 的部分和。（注意：这只是 **TP——没有 expert 并行**；所有 expert 都存在于所有 rank 上。）

## 3. 后端抽象（`moe/`）

`BaseMoeBackend` 是一个 ABC，只有一个 `forward(...)` 方法。引擎通过注册表（`moe/__init__.py`）注册后端，为 MoE 模型自动选择 `"fused"`，并将其存储在全局 ctx 中（`engine/engine.py`）。仅提供 `FusedMoe`——它包装了 SGLang 的 `sgl_kernel` 以及自定义 Triton 内核。

## 4. 融合管道（`moe/fused.py`）— 核心部分

`FusedMoe.forward` = **top-k 路由 → 块对齐调度 → 2个融合 GEMM → sum-reduce**：

**a) `fused_topk`** — 路由：

- `sgl_kernel.topk_softmax` 计算每个 token 在所有 expert 上的 top-k expert 索引和 softmax 归一化权重。
- 如果 `renormalize`，则重新归一化，使得 *所选* k 个权重之和为 1（标准 MoE 实践）。
- 可以掩码填充的 token（`topk_ids = -1`）以支持不规则批次。

**b) `moe_align_block_size`** — 调度布局：

- 将 `topk_ids` 展平（每个 token 出现 `top_k` 次），**按 expert 分组对 token 索引排序**，并将每个 expert 的 token 计数填充到 `BLOCK_SIZE_M` 的倍数（使用 `sgl_kernel.moe_align_block_size` 和 cumsum 缓冲区）。
- 这是经典技巧，允许 Triton GEMM 按 expert 处理一个连续的 `[M_padded, K]` 块——填充使块大小一致。

**c) `fused_experts_impl`** — 计算，分 3 次内核调用：

```
hidden [M, K]
  → fused_moe_kernel(w1=gate_up, mul_routed_weight=True)   # [M, topk, N]  (融合 G+U)
  → silu_and_mul / gelu_and_mul                            # SwiGLU 激活（将 2N 分成两半，逐元素相乘）
  → fused_moe_kernel(w2=down,  mul_routed_weight=False)    # [M, topk, hidden]
  → moe_sum_reduce_triton(sum over topk dim)               # [M, hidden]
```

注意 `apply_router_weight_on_input` 标志在两次内核调用之间 **翻转**（True → False），因此路由权重只乘一次——在 gate-up 输出上——在 top-k 求和之前。

## 5. Triton 内核（`kernel/triton/fused_moe.py`，`kernel/moe_impl.py`）

`fused_moe_kernel` 是一个分组的 GEMM，带有 expert 索引的权重查找：

- 每个程序计算（填充、排序后的）token×expert GEMM 的一个 `[BLOCK_M, BLOCK_N]` 瓦片。
- Token 行来自 `sorted_token_ids[offs_token]`；由于 token 在排序列表中重复 `top_k` 次，`offs_token // top_k` 可恢复输入中的 **原始 token 行**（`a_ptrs`）。使用 `token_mask` 屏蔽填充 token（`offs_token >= num_valid_tokens`）。
- 每个块通过 `expert_ids[pid_m]` 选择 expert 权重切片 → `b_ptr + off_experts * stride_be`。
- K 维度循环以 fp32 累加，如果 `MUL_ROUTED_WEIGHT` 则乘以路由权重，并写入 `[M, topk, N]` 缓存。

`moe_sum_reduce_kernel` 随后对每个 token 的 top-k 贡献求和，得到最终的隐藏状态。

## 总结图

```
router:  hidden [M,K] ──LinearReplicated──▶ logits [M,E]
                                              │ sgl_kernel.topk_softmax
                                              ▼
FusedMoe:  topk_weights [M,k] + topk_ids [M,k]
              │ moe_align_block_size (按 expert 排序并填充)
              ▼
          ┌─ fused_moe_kernel (w1: gate+up, ×weight) ─▶ [M,k,2N] ─ silu_and_mul ─▶ [M,k,N]
          │                                                                        │
          └─ fused_moe_kernel (w2: down, no weight) ◀──────────────────────────────┘
              │ moe_sum_reduce (对 k 求和)
              ▼
          [M, hidden] ── all_reduce (TP) ──▶ final
```

关键设计点：**融合的 gate/up 权重**（一个 GEMM 替代两个）、**分组 GEMM 调度**（使用按 expert 排序的填充块以实现高效的 Triton 矩阵乘法）、**仅 TP 分片**（无 EP）以及 **可插拔后端**，以便可以替换为 SGLang 的本地 `sgl_kernel` MoE 路径。
