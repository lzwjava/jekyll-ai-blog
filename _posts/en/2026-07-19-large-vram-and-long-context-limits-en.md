---
audio: false
generated: true
image: false
lang: en
layout: post
title: Large VRAM and Long Context Limits
translated: false
type: note
---

Question: Does a 48GB VRAM setup (2×RTX 3090) still fit large context windows like 32k or 100k tokens?

Answer:

The short answer: **model weights fit, but long context is where VRAM gets eaten by KV cache.** For 32k it is usually fine; 100k depends heavily on model architecture and quantization.

The inference memory is:

```
Total VRAM =
  model weights
+ KV cache
+ CUDA/runtime overhead
```

Most people only calculate weights and forget KV cache.

---

## Example: Qwen2.5-Coder-32B / Qwen3-32B

Assume:

* 32B model
* 4-bit weights
* 48GB VRAM

Weights:

```
32B × 4 bits
= 16GB
```

Runtime:

```
~3-5GB
```

Leaves:

```
48 - 20 ≈ 28GB
```

for KV cache.

---

## KV cache calculation

For a transformer:

```
KV cache =
2 × layers × sequence_length × KV_heads × head_dim × bytes
```

The important variables:

* number of layers
* KV heads (GQA helps a lot)
* context length
* KV cache precision

Modern models use GQA:

Example Qwen2.5-32B:

```
layers = 64
KV heads = 8
head_dim = 128
```

FP16 KV:

```
2 × 64 × 32768 × 8 × 128 × 2 bytes

≈ 8.6 GB
```

So:

### 32k context

```
weights      ~16GB
runtime      ~4GB
KV cache     ~9GB

total        ~29GB
```

Easy on 48GB.

---

## 100k context

Scale linearly:

```
100k / 32k = 3.125
```

KV:

```
9GB × 3.125
≈ 28GB
```

Total:

```
weights      16GB
runtime       4GB
KV           28GB

≈48GB
```

So Qwen2.5-32B 4-bit at 100k is right at the edge.

You would probably need:

* KV cache quantization
* lower batch size
* llama.cpp
* vLLM paged attention

---

## For 70B models

Example:

Llama 3.1 70B Q4:

Weights:

```
~40GB
```

Runtime:

```
5GB
```

Remaining:

```
3GB
```

KV cache:

not much room.

So:

```
70B @ 32k
```

is difficult on 48GB.

You need:

* KV cache quantization
* CPU offload
* more GPUs

---

## KV cache quantization changes everything

Instead of FP16 KV:

```
K,V = 16-bit
```

use:

```
INT8 KV
```

or:

```
FP8 KV
```

Memory roughly halves.

Example:

100k context:

```
FP16 KV:
28GB

FP8 KV:
14GB
```

Then:

```
32B Q4:
16GB weights
5GB runtime
14GB KV

≈35GB
```

Very comfortable.

---

## Practical 2×3090 targets

| Model                   | 32k ctx | 100k ctx         |
| ----------------------- | ------- | ---------------- |
| Qwen3 8B                | ✅ easy  | ✅ easy           |
| Qwen3 14B               | ✅ easy  | ✅                |
| Qwen3 32B Q4            | ✅       | ⚠️ with KV quant |
| Qwen2.5-Coder 32B Q4    | ✅       | ⚠️               |
| Llama 3.1 70B Q4        | ⚠️      | ❌                |
| DeepSeek-R1-Distill-32B | ✅       | ⚠️               |

---

For your workload (agents + coding + long documents), I would actually prioritize:

```
2 × RTX3090 48GB
+
llama.cpp / vLLM
+
Qwen3-32B
+
FP8/INT8 KV cache
```

This gives you a local model with something close to **100k context capability**, which is much more useful than squeezing a larger 70B model with only 8k context.
