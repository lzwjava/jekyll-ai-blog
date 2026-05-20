---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Qwen3.5-122B on MI300X
translated: false
type: note
---

Question: Can the model `unsloth/Qwen3.5-122B-A10B-MTP-GGUF` run on an AMD MI300X GPU with llama.cpp?

Answer:

Let’s break this down carefully with numbers:

---

### **1. Model Specs**

* **Qwen3.5-122B** → 122 billion parameters
* **A10B-MTP** → Likely means a mixed precision quantization (possibly 10-bit or custom) + MTP (multi-task pretraining)
* **GGUF format** → Compatible with `llama.cpp`

**Estimated memory footprint:**

* Dense FP16: 122B × 2 bytes ≈ 244 GB
* With **Q4_K / 4-bit quantization**: ~30–35% of FP16 → ~73–85 GB
* With **A10B-MTP (10-bit + compression)**: might reduce to **~90–95 GB** or slightly higher depending on KV cache and context length

> The MI300X has **192 GB VRAM**, so **in theory it can fit this model** in GPU memory with a single instance.

---

### **2. Token Context Considerations**

* `llama.cpp` requires additional VRAM for:

  * **KV cache** → grows with `context length × hidden size × #layers`
  * **Intermediate activations / working memory**
* With **typical 4K–8K context**, you probably need **~30–50 GB extra VRAM**.

**Estimated total VRAM usage:**

```
Model weights (~90–95 GB) + KV cache & buffers (~50 GB) ≈ 140–145 GB
```

* Leaves ~50 GB headroom → fine for 8K–16K context
* For **very long contexts (>50K tokens)**, you’ll hit memory limits

---

### **3. Throughput (tg128) Expectations**

* MI300X token generation is **memory bandwidth-limited**
* Rough estimate based on 70B-class benchmarks (40–45 GB weights → 45 t/s):

  * Model is ~2× size → throughput roughly halves → **20–25 tokens/sec**
* So, **realistic throughput for Qwen3.5-122B-A10B-MTP** on MI300X: **20–25 t/s per single GPU instance**

---

### **4. Practical Recommendations**

1. **Use Q4_K or A10B-MTP quantization** → reduces VRAM footprint
2. **Keep context length reasonable** (≤16K tokens) for smooth operation
3. **Enable flash attention** in llama.cpp → reduces memory pressure, improves speed
4. **Multi-instance / batching** → MI300X has enough VRAM to run 2–3 concurrent smaller sequences for throughput

> ✅ Conclusion: **Yes, it is feasible to run unsloth/Qwen3.5-122B-A10B-MTP-GGUF on a single MI300X with llama.cpp**, but expect **moderate throughput (~20–25 t/s)** and plan context length accordingly.

---

References:

* [llama.cpp GGUF format](https://github.com/ggml-org/llama.cpp)
* [AMD ROCm MI300X llama.cpp benchmarks](https://github.com/ggml-org/llama.cpp/discussions/14640)
* [Hugging Face: Qwen3.5-122B-A10B-MTP](https://huggingface.co/unsloth/Qwen3.5-122B-A10B-MTP-GGUF)

---

If you want, I can make a **VRAM map + token throughput estimate table for different context lengths** specifically for this 122B GGUF model on MI300X, so you can plan usage precisely. Do you want me to do that?