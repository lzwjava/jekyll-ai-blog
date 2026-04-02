---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding 1-Bit LLM Compression and Efficiency
translated: false
type: note
---

Question:
Is each neuron using +1/−1 so it’s 1-bit instead of FP16, and that’s why the model becomes about 14× smaller? Also, Microsoft released a 1-bit model before, and recently PrismML also did one — right?

Answer:

Yes — your intuition is basically correct, but there are a few important details.

---

# 1. Why “1-bit” ≈ much smaller than FP16

Traditional LLM weights:

* FP32 → 32 bits per parameter
* FP16 / BF16 → 16 bits per parameter
* 1-bit → **1 bit per parameter** (or ~1.58 bits if ternary)

If everything were pure:

```
FP16 → 16 bits
1-bit → 1 bit
ideal compression ≈ 16× smaller
```

But real models are not perfectly 1-bit everywhere:

They still need:

* scaling factors
* layer norms
* embeddings sometimes higher precision
* activations not fully 1-bit
* metadata / padding

So real-world compression:

```
16× theoretical
→ ~14× practical
```

That’s exactly what PrismML reports.

Their **1-bit Bonsai 8B**:

* same 8B parameters
* FP16 size ≈ 16 GB
* 1-bit size ≈ 1.15 GB
* ≈ **14× smaller**
* ≈ **8× faster**
* ≈ **5× less energy** ([PrismML][1])

So your math intuition is correct.

---

# 2. But it's usually not truly "binary"

Most "1-bit" LLMs are actually **ternary**:

weights ∈ { -1, 0, +1 }

That’s:

```
log2(3) ≈ 1.58 bits
```

So Microsoft calls it:

**1.58-bit LLM**

Microsoft BitNet:

* weights: −1, 0, +1
* similar performance to FP16
* much lower memory + compute cost ([Microsoft][2])

---

# 3. Why 1-bit is powerful

Normal transformer:

```
y = W x
```

needs:

* float multiply
* float add

1-bit transformer:

```
W ∈ {+1, -1}
```

multiply becomes:

```
+1 * x → x
-1 * x → -x
```

So matrix multiply becomes:

* add
* subtract

No floating multiply → huge speed gain.

This is why:

* faster
* lower power
* simpler hardware
* CPU friendly

---

# 4. Timeline (you remembered correctly)

### Microsoft (earlier)

BitNet / BitNet b1.58

* 1-bit (ternary) LLM
* CPU runnable
* similar accuracy
* designed for future hardware ([Microsoft][2])

---

### PrismML (new, 2026)

Bonsai 1-bit

* full network 1-bit
* 14× smaller
* 8× faster
* edge device focused ([PrismML][1])

---

# 5. One subtle but important correction

You said:

> 每个神经元 加一减一

Actually it's:

**each weight** is ±1
not neuron output.

So:

```
neuron output still float
weights are 1-bit
```

Otherwise model would collapse.

---

# 6. Big picture insight (important)

This is why 1-bit LLMs are a big deal:

Instead of:

```
bigger model
more GPU
more VRAM
```

we get:

```
same intelligence
much smaller compute
edge deployment
```

This is similar magnitude shift like:

* int8 quantization
* llama.cpp
* FlashAttention

But potentially **bigger impact**.

---

Your intuition summary:

* 1bit = ±1 ✔
* compared to fp16 ✔
* ~16x theoretical ✔
* ~14x practical ✔
* Microsoft did earlier ✔
* PrismML latest ✔

You got it right.

[1]: https://prismml.com/?utm_source=chatgpt.com "PrismML — Concentrating intelligence"
[2]: https://www.microsoft.com/en-us/research/?p=1039074&utm_source=chatgpt.com "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits - Microsoft Research"