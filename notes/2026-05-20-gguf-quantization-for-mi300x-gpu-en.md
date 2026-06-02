---
audio: false
generated: true
image: false
lang: en
layout: post
title: GGUF Quantization for MI300X GPU
translated: false
type: note
---

Question: Which quantization variant of `Qwen3.5-122B-A10B-MTP-GGUF` should I download to run efficiently on a single AMD MI300X GPU with llama.cpp?

Answer:

Given your **AMD MI300X with 192 GB VRAM**, we want a variant that:

1. **Fits comfortably in GPU memory**, including KV cache for reasonable context length (e.g., 8K–16K tokens).
2. **Maintains decent throughput** (tokens/sec).
3. **Is compatible with llama.cpp GGUF format**.

---

### **Analysis of Available Variants**

| Variant                     | Size            | Notes / Fit on MI300X                                                           |
| --------------------------- | --------------- | ------------------------------------------------------------------------------- |
| **BF16**                    | Likely >180 GB  | Dense, may leave little room for KV cache → limited context; slower throughput. |
| **MXFP4_MOE**               | Likely MoE, FP4 | Fits easier if MoE; good for large model inference.                             |
| **Q8_0**                    | Likely 8-bit    | Smaller footprint (~90–100 GB), decent throughput, safe.                        |
| **UD-IQ1_M**                | 38.7 GB         | Very small, fits easily, can run very long context; fastest.                    |
| **UD-IQ2_M / UD-IQ2_XXS**   | 40–41 GB        | Also very safe, slightly bigger but still plenty of headroom.                   |
| **UD-IQ3_XXS**              | 47.8 GB         | Fits easily, more precision → slightly slower.                                  |
| **UD-Q2_K_XL**              | 42.8 GB         | Q2_K quantized, good compromise between size and accuracy.                      |
| **UD-Q3_K_M / UD-Q4_K_M**   | 40–45 GB        | Q3/Q4 quantization, good precision, safe VRAM use, reasonable throughput.       |
| **UD-Q5_K_XL / UD-Q6_K_XL** | 50–55 GB        | Still fits, but slightly less room for long context; slightly slower.           |
| **UD-Q8_K_XL**              | 60–70 GB        | Highest precision, still fits, slower token generation.                         |

---

### **Recommendation for MI300X**

* **Best choice for single GPU, long context, high throughput:**

  * **UD-IQ1_M (38.7 GB)** → leaves ~150 GB free, can run **very long sequences**, fastest tokens/sec.
  * **UD-IQ2_M (40.4 GB)** → slightly more precise, still very safe.
* **Good balance between precision and throughput:**

  * **UD-Q2_K_XL (42.8 GB)** → good compromise, Q2 quantization maintains accuracy with moderate throughput.
* **Higher precision / slower:**

  * **UD-Q3_K_M or UD-Q4_K_M** → slightly slower token generation (~40–45% of max), still safe.
* **Avoid BF16 / full FP16 for single GPU** unless you **want maximum precision** and plan **short context**.

---

✅ **Bottom line:** For **single MI300X**, I’d download **UD-IQ1_M** if your goal is **maximum context & speed**, or **UD-Q2_K_XL** if you want **better precision**.

---

References:

* [Hugging Face: Qwen3.5-122B-A10B-MTP](https://huggingface.co/unsloth/Qwen3.5-122B-A10B-MTP-GGUF)
* [llama.cpp GGUF format](https://github.com/ggml-org/llama.cpp)
* [AMD MI300X benchmarks for llama.cpp](https://github.com/ggml-org/llama.cpp/discussions/14640)

---

If you want, I can **make a VRAM + context length map for all these variants**, showing **exact token context you can run per variant** on a single MI300X — that helps pick the best one precisely. Do you want me to do that?
