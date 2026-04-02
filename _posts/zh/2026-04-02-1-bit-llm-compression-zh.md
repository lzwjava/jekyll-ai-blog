---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 1 位大语言模型压缩与效率
translated: true
type: note
---

Question:
每个神经元都使用 +1/−1 所以是 1-bit 而不是 FP16，这就是为什么模型变得大约 14× 更小？另外，Microsoft 之前发布过一个 1-bit 模型，最近 PrismML 也做了一个——对吧？

Answer:

是的——你的直觉基本正确，但有一些重要细节。

---

# 1. 为什么 “1-bit” ≈ 比 FP16 小得多

传统的 LLM weights：

* FP32 → 32 bits per parameter
* FP16 / BF16 → 16 bits per parameter
* 1-bit → **1 bit per parameter** (or ~1.58 bits if ternary)

如果一切都是纯的：

```
FP16 → 16 bits
1-bit → 1 bit
ideal compression ≈ 16× smaller
```

但真实模型并非处处完美 1-bit：

它们仍然需要：

* scaling factors
* layer norms
* embeddings sometimes higher precision
* activations not fully 1-bit
* metadata / padding

所以真实世界的压缩：

```
16× theoretical
→ ~14× practical
```

这正是 PrismML 报告的。

他们的 **1-bit Bonsai 8B**：

* same 8B parameters
* FP16 size ≈ 16 GB
* 1-bit size ≈ 1.15 GB
* ≈ **14× smaller**
* ≈ **8× faster**
* ≈ **5× less energy** ([PrismML][1])

所以你的数学直觉是正确的。

---

# 2. 但通常不是真正的 “binary”

大多数 “1-bit” LLMs 实际上是 **ternary**：

weights ∈ { -1, 0, +1 }

那是：

```
log2(3) ≈ 1.58 bits
```

所以 Microsoft 称之为：

**1.58-bit LLM**

Microsoft BitNet：

* weights: −1, 0, +1
* similar performance to FP16
* much lower memory + compute cost ([Microsoft][2])

---

# 3. 为什么 1-bit 很强大

正常的 transformer：

```
y = W x
```

需要：

* float multiply
* float add

1-bit transformer：

```
W ∈ {+1, -1}
```

multiply 变成：

```
+1 * x → x
-1 * x → -x
```

所以 matrix multiply 变成：

* add
* subtract

没有 floating multiply → 巨大的速度提升。

这也是为什么：

* faster
* lower power
* simpler hardware
* CPU friendly

---

# 4. 时间线（你记得正确）

### Microsoft（较早）

BitNet / BitNet b1.58

* 1-bit (ternary) LLM
* CPU runnable
* similar accuracy
* designed for future hardware ([Microsoft][2])

---

### PrismML（新，2026）

Bonsai 1-bit

* full network 1-bit
* 14× smaller
* 8× faster
* edge device focused ([PrismML][1])

---

# 5. 一个细微但重要的更正

你说：

> 每个神经元 加一减一

实际上是：

**每个 weight** 是 ±1
不是 neuron output。

所以：

```
neuron output still float
weights are 1-bit
```

否则模型会崩溃。

---

# 6. 大局观洞见（重要）

这就是为什么 1-bit LLMs 是大事：

不再是：

```
bigger model
more GPU
more VRAM
```

而是：

```
same intelligence
much smaller compute
edge deployment
```

这类似于以下的重大转变：

* int8 quantization
* llama.cpp
* FlashAttention

但潜在 **更大影响**。

---

你的直觉总结：

* 1bit = ±1 ✔
* compared to fp16 ✔
* ~16x theoretical ✔
* ~14x practical ✔
* Microsoft did earlier ✔
* PrismML latest ✔

你完全正确。

[1]: https://prismml.com/?utm_source=chatgpt.com "PrismML — Concentrating intelligence"
[2]: https://www.microsoft.com/en-us/research/?p=1039074&utm_source=chatgpt.com "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits - Microsoft Research"