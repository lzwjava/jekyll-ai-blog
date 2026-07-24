---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GQA中的KV头扩展
translated: true
type: note
---

问题：在GQA/MQA注意力机制中，`k_i = k_i.repeat_interleave(num_repeats, dim=2)` 的作用是什么？已知注释为 `(1, kv_len, 16, 128)`。

回答：

这是在**分组查询注意力（GQA）**中将KV头扩展为与Q头数量匹配的操作。张量的形状说明了逻辑：`(batch, seq_len, num_heads, head_dim)`。

**问题背景：** 为了节省KV缓存内存，训练/推理时使用的KV头数量少于Q头。例如，有16个查询头但只有4个KV头（`num_repeats = 16/4 = 4`）。每个KV头被一组4个Q头共享。

**在repeat_interleave之前**，`k_i`的形状为 `(1, kv_len, 4, 128)`——4个KV头。

**repeat_interleave(4, dim=2)** 将每个KV头复制为4个相同的副本，并保持连续排列：

```python
import torch

kv_heads = 4
num_repeats = 4
k_i = torch.arange(kv_heads).view(1, 1, kv_heads, 1)  # 模拟KV头索引
print(k_i.squeeze())
# tensor([0, 1, 2, 3])

out = k_i.repeat_interleave(num_repeats, dim=2)
print(out.squeeze())
# tensor([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3])
```

因此，KV头0被复制到Q头槽位[0,1,2,3]，KV头1复制到[4,5,6,7]，以此类推。这与Q头的布局方式匹配（非交错排列）——Q头索引`h`对应使用KV头索引`h // num_repeats`。

**为何不直接用`.repeat()`：** `repeat`会整体平铺序列`[0,1,2,3,0,1,2,3,...]`——导致错误的分组。`repeat_interleave`生成`[0,0,0,0,1,1,1,1,...]`——这是正确的，因为每个Q头组需要*相同*的KV头重复出现，而非整个KV头序列重新平铺。

**操作之后：** `k_i`的形状变为`(1, kv_len, 16, 128)`——此时每个Q头都对应一个（已复制的）K/V头，因此可以直接使用普通的多头注意力机制（逐头计算Q·Kᵀ矩阵乘法），无需特殊的GQA感知内核。

**代价：** 此操作会显式占用内存——产生`num_repeats`份副本。实际推理引擎（如vLLM、FlashAttention-2的GQA内核）会通过在内核内部虚拟广播KV头来避免这种物理扩展。这里的`repeat_interleave`是朴素/参考实现——适用于正确性验证，但不适用于高性能服务场景。

**无需额外内存的替代方案**（通过视图+扩展实现广播，在矩阵乘法之前不实际复制数据）：
```python
k_i = k_i.unsqueeze(3).expand(1, kv_len, kv_heads, num_repeats, 128).reshape(1, kv_len, 16, 128)
```
对于非连续情况，仍会在`.reshape()`时产生实际内存分配，但至少意图（广播而非复制）是明确的，且某些自动求导/内核路径可以将其融合。

如果是为训练（而非服务）编写代码，`repeat_interleave`完全可用——它只是为后续在Eager模式/GQA朴素模式下调用标准`scaled_dot_product_attention`做准备。