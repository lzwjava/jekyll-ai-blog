---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Runs Compact Gemma 4 MoE
translated: false
type: note
---

Question:
Can RTX 4070 run **unsloth/gemma-4-26B-A4B-it-UD-IQ1_M.gguf**?

Answer:

Yes — **RTX 4070 (12GB) can run it**, and **much better than Qwen-27B**, because this is a **MoE (A4B active)** model with **very aggressive IQ1 quantization**.

But there are important details.

---

# 1. Memory requirement (Gemma-4-26B A4B)

Unsloth documentation states:

* **Gemma-4-26B-A4B (4-bit)** needs **~16–18 GB total memory**
* If less memory → CPU offload still works but slower ([Unsloth - Train and Run Models Locally][1])

Your RTX 4070:

* VRAM: **12GB**
* System RAM (likely 32GB+) → OK

So this model **fits using GPU + CPU hybrid**.

---

# 2. IQ1_M version is extremely small

Other quant sizes from the same repo:

* IQ2_XXS → **~9.88 GB**
* IQ2_M → **~9.97 GB**
* IQ3_S → **~11.2 GB**
* IQ4_XS → **~13.4 GB** ([Hugging Face][2])

Your **IQ1_M** is even **smaller than 9–10GB**, meaning:

👉 It **fits fully in 12GB VRAM**
👉 Can run **full-GPU**
👉 Much faster than 27B Q4

---

# 3. Why Gemma-4-26B works on 4070

This model is **MoE (A4B)**:

* total parameters: 26B
* **active per token: ~4B**
* behaves like **4B compute**, but **26B quality**

So it’s **very GPU friendly**.

This is why many users run 26B-A4B on **16GB cards** successfully. ([Reddit][3])

---

# 4. Expected performance on RTX 4070

With IQ1_M:

* ✅ fits in VRAM
* ✅ full GPU inference possible
* ✅ fast tokens/sec
* ⚠️ quality lower (IQ1 aggressive)

Rough estimate:

* speed: ~20–40 tok/s
* VRAM: ~9–11GB
* context: 8k–32k OK

---

# 5. Better choice for RTX 4070

Best balance:

* IQ3_S (11.2GB) → best
* IQ2_M (10GB) → good
* IQ1_M → fastest but lower quality

Avoid:

* IQ4_XS (13.4GB) → may not fit
* Q4_K → too large

---

# Final verdict

RTX 4070 (12GB) + this model:

* ✅ **Yes, runs**
* ✅ **likely full GPU**
* ✅ **better than Qwen3.5-27B**
* ⚠️ IQ1 quality lower
* ⭐ very good for coding agents

This model is actually **one of the best 26B-class choices for 4070**.

If you're using:

* OpenClaw
* llama.cpp
* Ollama
* LM Studio

Tell me — I’ll give **exact launch command**.

[1]: https://unsloth.ai/docs/models/gemma-4?utm_source=chatgpt.com "Gemma 4 - How to Run Locally | Unsloth Documentation"
[2]: https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/blob/main/gemma-4-26B-A4B-it-UD-IQ2_XXS.gguf?utm_source=chatgpt.com "gemma-4-26B-A4B-it-UD-IQ2_XXS.gguf · unsloth/gemma-4-26B-A4B-it-GGUF at main"
[3]: https://www.reddit.com/r/LocalLLaMA/comments/1scw979/gemma_4_for_16_gb_vram/?utm_source=chatgpt.com "Gemma 4 for 16 GB VRAM"