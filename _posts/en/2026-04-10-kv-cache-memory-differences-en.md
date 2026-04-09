---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache Explains Memory Differences
translated: false
type: note
---

Question:
Why does Gemma-4 **E2B** use less memory than **A26B MoE** at the same context length and same quantization, and what context length can run on mobile (32k vs 65k)?

Answer:

This confusion usually comes from **MoE vs dense model** memory behavior and **KV cache scaling**.
Even if quantization bits are the same, **runtime memory is dominated by KV cache**, not just weights.

The key relationship:

\text{KV cache memory} \approx 2 \times L \times H \times T \times \text{bytes per element}

Where:

* (L) = number of layers
* (H) = hidden size
* (T) = context length (32k, 65k, etc.)
* factor **2** = K + V cache
* bytes = depends on fp16 / q8 / q4 etc.

---

# 1. Why Gemma-4 E2B uses LESS memory than A26B MoE

Even though **A26B is MoE**, KV cache is **NOT sparse**.

Important:

* MoE reduces **compute**
* MoE does **NOT reduce KV cache**
* KV cache depends on **hidden size**, not number of active experts

So if:

* A26B has **larger hidden dimension**
* more heads
* more layers

then its KV cache becomes **much larger**.

This is why:

* same quantization
* same context length
* A26B MoE still uses **more RAM**

because:

MoE sparsity only applies to **FFN weights**,
but KV cache stores **full attention states**.

---

# 2. Why E2B is especially memory efficient

Gemma-4 **E2B** likely has:

* smaller hidden size
* fewer layers
* smaller head dimension

So KV cache is much smaller.

Example intuition:

| model    | hidden size | layers | KV memory |
| -------- | ----------- | ------ | --------- |
| E2B      | smaller     | fewer  | small     |
| A26B MoE | bigger      | more   | large     |

Even if A26B activates only 2 experts:

KV cache still full size.

---

# 3. Context length on mobile (32k vs 65k)

Context length scales **linearly**:

32k → baseline
65k → ~2× memory

So if:

32k fits → 65k likely **OOM**

Typical mobile / small RAM:

* 7B / E2B → 32k OK
* 65k → borderline / OOM
* A26B → even 32k heavy

Because:

KV cache dominates after ~16k.

---

# 4. Why quantization doesn't help much here

Quantization reduces:

* model weights

But **KV cache usually stays fp16 / fp8**

So memory ≈ dominated by KV cache

Therefore:

same quantization
but different hidden size
→ big memory difference

---

# 5. Simple mental model

Dense model memory:

weights + KV cache

MoE model memory:

weights (smaller active) + **same KV cache**

So:

MoE saves compute
NOT context memory

---

# Final intuition

E2B smaller attention dimension
→ smaller KV cache
→ longer context fits

A26B MoE larger attention dimension
→ huge KV cache
→ memory explodes

So E2B can run:

* 32k easier
* maybe 65k

while A26B struggles even at 32k.