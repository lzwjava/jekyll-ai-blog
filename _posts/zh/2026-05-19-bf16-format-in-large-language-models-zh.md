---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型中的BF16格式
translated: true
type: note
---

**问题：** BF16是什么？它在大型语言模型（LLM）中是如何使用的？

**回答：**

## BF16 从基本原理出发

### 位布局

浮点格式由三个字段定义：符号位、指数、尾数。

```
FP32:  [1位符号][8位指数][23位尾数] = 32位
FP16:  [1位符号][5位指数][10位尾数] = 16位
BF16:  [1位符号][8位指数][7位尾数]  = 16位  ← 与FP32指数位数相同
```

BF16 = "Brain Float 16"，由 Google Brain 开发。关键思路：**保留FP32的指数范围，截断尾数**。

```python
import struct

def fp32_bits(x):
    return struct.pack('f', x).hex()

def show_format(x):
    b = struct.unpack('I', struct.pack('f', x))[0]
    sign     = (b >> 31) & 0x1
    exponent = (b >> 23) & 0xFF
    mantissa = b & 0x7FFFFF
    print(f"FP32  {x}: sign={sign} exp={exponent:08b}({exponent-127:+d}) mantissa={mantissa:023b}")
    # BF16 就是 FP32 的高 16 位
    bf16_mantissa = mantissa >> 16  # 只保留高 7 位
    print(f"BF16  {x}: sign={sign} exp={exponent:08b}({exponent-127:+d}) mantissa={bf16_mantissa:07b}")

show_format(3.14)
show_format(0.0001)
show_format(65504.0)  # FP16 最大值
show_format(3.4e38)   # 接近 FP32 最大值 — BF16 能处理，FP16 会溢出
```

### 动态范围比较

| 格式 | 指数位数 | 最大值     | 最小正规数 | 精度（十进制位数） |
|------|----------|------------|------------|-------------------|
| FP32 | 8        | ~3.4e38    | ~1.2e-38   | ~7.2              |
| FP16 | 5        | 65504      | ~6.1e-5    | ~3.3              |
| BF16 | 8        | ~3.4e38    | ~1.2e-38   | ~2.3              |

**BF16 与 FP32 具有相同的范围，但精度只有约2位十进制数。** FP16 精度更好，但范围小得可怜——梯度和权重很容易溢出为 `inf` 或下溢为0。

---

## 这对大型语言模型为何重要

### 1. 训练稳定性

FP16 的经典训练问题：

```
gradient = 1e-6   # 很小但有效
FP16 最小正规数 ≈ 6e-5
→ 梯度下溢为0 → 梯度消失 → 训练发散
```

BF16 可以处理这个问题，因为其指数范围等于 FP32：

```
BF16 最小正规数 ≈ 1.2e-38  ← 梯度 1e-6 完全没问题
```

这就是为什么 BF16 训练通常**不需要损失缩放**（而 FP16 需要 `GradScaler`）。

```python
# FP16 训练 — 需要损失缩放
scaler = torch.cuda.amp.GradScaler()
with torch.autocast(device_type='cuda', dtype=torch.float16):
    loss = model(x)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

# BF16 训练 — 更简单，无需缩放器
with torch.autocast(device_type='cuda', dtype=torch.bfloat16):
    loss = model(x)
loss.backward()
optimizer.step()
```

### 2. 内存节省

```
FP32 7B 参数模型：7e9 * 4 字节 = 28 GB
BF16 7B 参数模型：7e9 * 2 字节 = 14 GB  ← 可放入 2 块 A100 40GB 而非 4 块
```

训练期间仍需优化器状态（Adam：2倍 FP32 参数副本 = 另外 28 GB），但**混合精度**在前向/反向传播中保持 BF16 权重，而 FP32 主副本用于优化器更新。

### 3. 硬件加速

现代 GPU 具有原生 BF16 Tensor Core：

| GPU | BF16 TFLOPS | FP32 TFLOPS | 加速比 |
|-----|-------------|-------------|--------|
| A100 80GB | 312 | 19.5 | 16x |
| H100 SXM | 989 | 67 | ~15x |
| RTX 4090 | 165 | 82.6 | 2x |

A100/H100 具有巨大的 BF16 加速能力。这是 BF16 成为 LLM 训练标准的主要原因——与 FP32 相比，可免费获得 10-16 倍的吞吐量提升。

---

## 混合精度训练：全貌

```
┌─────────────────────────────────────────────────────────┐
│  前向传播                                               │
│  权重 (BF16) → 激活值 (BF16)                            │
│                           ↓                            │
│  损失 (矩阵乘法输出中 FP32 累加)                        │
│                           ↓                            │
│  反向传播                                               │
│  梯度以 BF16 计算                                       │
│                           ↓                            │
│  优化器步骤                                             │
│  FP32 主权重 ← BF16 梯度转换为 FP32                     │
│  Adam m, v 以 FP32 存储                                 │
│  更新后的 FP32 权重 → 转换回 BF16                       │
└─────────────────────────────────────────────────────────┘
```

以 nanoGPT 风格实现：

```python
import torch
import torch.nn as nn

model = GPT(config).cuda()

# 优化器自动处理 FP32 主权重
# 使用 AMP 时 — PyTorch 内部管理主副本
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

# torch.compile + BF16 = A100/H100 上的最大吞吐量
model = torch.compile(model)

ctx = torch.autocast(device_type='cuda', dtype=torch.bfloat16)

for x, y in dataloader:
    with ctx:
        logits, loss = model(x, y)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

这正是 Karpathy 在 nanoGPT 中使用的内容——`dtype=torch.bfloat16` + A100。

---

## 推理：超越 BF16 的量化

在推理时，可以更进一步：

```
训练：     BF16 权重 + BF16 激活值（混合 FP32 累加器）
推理：     INT8 / INT4 权重 + BF16 激活值（GPTQ, AWQ, bitsandbytes）
```

```python
# bitsandbytes 4位推理
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,  # 激活值为 BF16
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"               # NormalFloat4
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
```

权重以 INT4 存储（7B 模型约 3.5 GB），在矩阵乘法时动态反量化为 BF16。

---

## BF16 vs FP16：何时使用哪种

| 场景 | 建议 |
|------|------|
| 在 A100/H100 上训练 | **BF16** — 始终使用 |
| 在较旧 GPU (V100) 上训练 | FP16 + GradScaler（V100 没有 BF16 Tensor Core） |
| 在消费级 GPU 上推理 | 如果支持则用 BF16，否则 FP16 |
| Apple Silicon (MPS) | M2+ 支持 BF16 |
| TPU | 原生 BF16（Google 为 TPU 设计） |

检查支持情况：

```python
print(torch.cuda.is_bf16_supported())  # A100, H100, RTX 30xx+ 上为 True
```

---

## 实际中的精度损失

BF16 只有 7 位尾数 → 相邻可表示值之间的分辨率约为 0.8%。这会带来问题吗？

实证表明：**不会，对于 LLM 权重来说**。神经网络权重对这种级别的噪声具有鲁棒性——它本质上是免费的正则化。超过约 10 亿参数后，BF16 与 FP32 训练的损失曲线几乎无法区分。

可能**会**出现问题的地方：需要高数值精度的操作——softmax（大数的指数）、层归一化、损失计算。即使在 BF16 自动混合精度期间，这些操作也会在矩阵乘法累加器中以 FP32 内部保留。

---

## 总结

```
BF16 = FP32 的指数 + 7 位尾数
     = 相同范围，更低精度
     = 没有困扰 FP16 的溢出/下溢问题
     = 相比 FP32 节省 2 倍内存
     = A100/H100 Tensor Core 上实现 10-16 倍吞吐量
     = 现代 LLM 训练的标准
```

如果你在 H100（你正在使用）上训练，BF16 + `torch.compile` 是默认技术栈——无需 GradScaler，没有因溢出导致的损失尖峰，最大 FLOP 利用率。
