---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V4 与 nanoGPT 的区别
translated: true
type: note
---

问题：在DeepSeek V4官方推理代码中，`scale_fmt`、`n_routed_experts`以及`ue8m0`格式是什么——这些与nanoGPT不同的地方？

答案：

直接研究官方推理代码是很好的直觉。下面我从基本原理逐一解释。

---

## `n_routed_experts` — MoE路由

nanoGPT的每一层只有一个稠密FFN：

```python
# nanoGPT FFN — 每个token都经过相同的权重
x = self.c_fc(x)    # [B, T, 4*n_embd]
x = self.gelu(x)
x = self.c_proj(x)  # [B, T, n_embd]
```

DeepSeek V4将其替换为**混合专家（MoE）** FFN：

```python
# MoE：存在N个专家，但每个token仅激活top-K个
n_routed_experts = 256   # 专家总数
n_activated_experts = 8  # 每个token选择的top-K（稀疏激活）
```

路由器是一个小型线性层，对全部256个专家进行评分并选出8个：

```python
# 简化的MoE前向
router_logits = x @ router_weight.T        # [B*T, n_routed_experts]
topk_ids = router_logits.topk(k=8).indices # 选出8个专家
output = sum(expert[i](x) for i in topk_ids)  # 仅8个FFN被激活
```

**为什么重要：** 256个专家 × FFN参数量 = 庞大的总参数量，但每个token仅激活8个专家 → 计算量保持可控。DeepSeek-V3/V4总参数量约671B，但每次前向仅激活约37B。这就是MoE的权衡。

此外还有**共享专家**（始终激活，类似稠密残差）和路由专家。DeepSeek将此架构称为**DeepSeekMoE**。

---

## `scale_fmt` — 量化缩放格式

这涉及**如何存储量化权重的缩放因子**。

当你量化一个权重矩阵（例如FP16 → INT8）时，需要按块存储缩放因子：

```
W_quantized = round(W / scale)
W_reconstructed = W_quantized * scale
```

`scale_fmt` 指定了**该缩放张量的数据类型**。在DeepSeek V4的推理代码中，你会看到如下选项：

```python
scale_fmt = "e4m3"   # FP8缩放
scale_fmt = "e5m2"   # FP8缩放（不同的范围/精度）
scale_fmt = "fp16"   # 半精度缩放
```

这对于**FP8量化**至关重要——DeepSeek V3/V4原生采用FP8进行训练和推理（这是一项重要的工程贡献）。缩放格式决定了反量化步骤的精度。

---

## `ue8m0` — 无符号指数8位，尾数0位

这是一种**非标准浮点格式**，也是三者中最特殊的。

标准浮点结构：`符号 | 指数 | 尾数`

| 格式 | 符号 | 指数 | 尾数 | 范围 |
|--------|------|----------|----------|-------|
| FP32 | 1 | 8 | 23 | ~1e-38 到 3e38 |
| FP16 | 1 | 5 | 10 | ~6e-5 到 65504 |
| E4M3 (FP8) | 1 | 4 | 3 | ~1e-9 到 448 |
| **UE8M0** | **0** | **8** | **0** | 仅2的幂 |

`ue8m0` **只能表示2的幂**：`2^-127` 到 `2^128`。没有小数尾数，没有符号。

**为什么用它来存储缩放因子？** 量化缩放因子在实践中几乎总是2的幂（为了硬件效率，你会四舍五入到最近的2的幂）。将它们存储为`ue8m0`意味着：

- 反量化变成**位移位**而不是乘法——在硬件上极其快速
- 每个缩放因子只需8位而不是16位（FP16）→ 缩放张量内存减半
- 完美适配大规模块状FP8量化

这是**MXFP8 / 微缩放格式**，正成为前沿模型推理的标准。NVIDIA H100、AMD MI300X都在硬件层面支持。

---

## 它们如何关联

```
DeepSeek V4推理管道：

Token → 注意力（MLA，也具独特性） → MoE FFN
                                           ↓
                              路由器对256个专家评分（n_routed_experts）
                                           ↓
                              激活top-8个专家（稀疏，低成本）
                                           ↓
                              每个专家权重为FP8量化
                              缩放因子以ue8m0存储（2的幂，8位）
                              scale_fmt控制此数据类型
```

---

## 在Hermes分析中关注什么

当你通过Hermes运行代码时，重点关注：

1. **`MoEGate` / 路由器模块** — 辅助损失（负载均衡）如何计算
2. **`fp8_gemm` 调用** — 矩阵乘法中实际使用`scale_fmt`和`ue8m0`的地方
3. **`shared_experts` 与 `routed_experts`** — DeepSeek的混合稠密+稀疏设计
4. **`ep_size`（专家并行度）** — 专家如何在GPU间分片

官方推理代码是MXFP8 + MoE如何在生产环境中实际工作的最清晰文档。比任何论文都强。

参考文献：

- [DeepSeek-V4-Pro推理代码](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/tree/main/inference)
- [DeepSeek-V3技术报告](https://arxiv.org/abs/2412.19437)
- [MXFP8 / 微缩放格式 — OCP规范](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf)
