---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM预填充基准测试解释
translated: true
type: note
---

**问题：** 在 LLM 推理基准测试中，“prefill”是什么意思？比如“LLM prefill (8192x8192): 1,632 TFLOPS”这样的表述。

**回答：**

Prefill 是自回归推理的第一阶段——在生成开始之前，一次性对整个输入 prompt 进行前向传播。它不同于 **decode**（在 prefill 之后逐个生成 token）。

### 为什么是 8192x8192 这个具体数值

这是 `seq_len x seq_len`——一个 8192 token 的 prompt，因此注意力矩阵的大小是 8192×8192。该基准测试衡量的是对长度为 8192 的序列进行一次前向传播的吞吐量。

### Prefill vs Decode——你已经关心的关键区别（KV cache 的工作）

```
Prefill:
  - 输入：一次性输入所有 N 个 prompt token
  - 计算：并行处理 N 个 token（一次 matmul 传递）
  - 瓶颈：受计算能力限制（大型 matmul，高算术强度）
  - 输出：所有 N 个 token 的 KV cache + 第一个生成的 token
  - 因此以 TFLOPS 来衡量——你受计算能力限制，
    所以 FLOPS/sec 是合适的指标

Decode:
  - 输入：每次输入 1 个新 token（使用 prefill 阶段缓存的 K、V）
  - 计算：batch=1（或小 batch）的 matvec，而非 matmul
  - 瓶颈：受内存带宽限制（加载权重 + KV cache
    占主导，算术强度低）
  - 因此 decode 通常以 tokens/sec 而非 TFLOPS 来衡量
```

### 为什么这个区别在实际中很重要

对于长度为 N 的 prompt，自注意力成本为 O(N²·d)（用于 QK^T 和 softmax·V）。这就是为什么 prefill 的计算量随 prompt 长度呈二次方增长，并且此时你才能真正饱和 GPU 的计算能力（MI300X 的 1,307 TFLOPS BF16 密集计算——你看到的 1,632 TFLOPS 意味着 MFU >100%……这有点可疑，除非它计算的是稀疏/结构化 FLOPS，或者是厂商的峰值营销数字，值得查一下来源）。

对一个具有 `d_model` 和 `n_layers` 的模型，进行长度为 8192 的序列的 prefill 的粗略 FLOPS 估算：

```python
def prefill_flops(seq_len, d_model, n_layers, d_ff_mult=4):
    # 每层：QKV 投影 + 注意力 + O 投影 + FFN
    attn_proj = 4 * seq_len * d_model**2       # Q,K,V,O 投影
    attn_scores = 2 * seq_len**2 * d_model     # QK^T 和 softmax*V
    ffn = 2 * seq_len * d_model * (d_ff_mult * d_model) * 2  # 上+下投影
    per_layer = attn_proj + attn_scores + ffn
    return per_layer * n_layers * 2  # 乘以2是因为乘加操作

# 例如，一个 7B 左右的模型，seq_len=8192
flops = prefill_flops(seq_len=8192, d_model=4096, n_layers=32)
print(f"{flops/1e12:.1f} TFLOPs total for one prefill pass")
```

给定 GPU 的峰值 TFLOPS/sec，`flops / peak_tflops` 可以得到理论上的 prefill 延迟——当你对自己的 GPT-2 760M 或更大的训练/推理运行进行基准测试时，可以用这个来推理你的 MI300X 的预期首 token 生成时间。

你引用的 `1,632 TFLOPS` 数值是一个**测得的吞吐量**，而不是固定成本——它告诉你在那个特定的 8192×8192 prefill 工作负载下，硬件接近峰值的程度，这是厂商报告受计算能力限制的推理性能的标准方式。

参考资料：

- [MI300X 规格 - AMD](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
