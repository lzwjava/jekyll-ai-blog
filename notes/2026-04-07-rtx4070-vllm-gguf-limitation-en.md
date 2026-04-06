---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 vLLM GGUF Limitation
translated: false
type: note
---

Question: Can `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` be served by vLLM on a local RTX 4070 server?

Answer:

Short answer: **No.**
You cannot serve `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` with **vLLM** on an **RTX 4070 (12GB)**.

There are **two separate blockers**:

---

# 1. vLLM does NOT support GGUF models

Your model:

```
gemma-4-26B-A4B-it-UD-IQ3_S.gguf
```

is:

* GGUF format
* llama.cpp quantization (IQ3_S)
* Unsloth / llama.cpp ecosystem

But **vLLM only supports:**

* HuggingFace FP16/BF16
* AWQ
* GPTQ
* some tensor-parallel sharded weights

vLLM **cannot load GGUF** at all.

So even before VRAM — it simply won't run.

You must use one of:

* llama.cpp
* llama-cpp-python
* Ollama
* OpenWebUI + llama.cpp backend
* OpenClaw (if using llama backend)

---

# 2. RTX 4070 VRAM is too small anyway

RTX 4070:

```
12GB VRAM
```

Your model:

```
Gemma 4 26B IQ3_S
```

Approx VRAM usage:

| Quant  | VRAM needed |
| ------ | ----------- |
| IQ3_S  | ~13–15GB    |
| IQ2    | ~10–11GB    |
| Q4_K_M | ~18–20GB    |

So:

* **IQ3_S → too big for 4070**
* might work **CPU offload**, but slow
* vLLM cannot do GGUF CPU offload anyway

---

# What WILL work on RTX 4070

Best choices:

### Option 1 (recommended)

Use llama.cpp:

```
llama-server \
-m gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
--n-gpu-layers 30
```

This:

* partially loads GPU
* rest CPU
* usable speed

---

### Option 2 (better fit)

Use smaller quant:

```
IQ2_XS
IQ2_S
```

These fit fully in 4070.

---

### Option 3 (best for vLLM)

Use **non-GGUF** model:

Example:

```
gemma-2-27b-it AWQ
gemma-2-9b-it
qwen3-14b-awq
```

These can run in vLLM.

---

# Final Verdict

| Question             | Answer                   |
| -------------------- | ------------------------ |
| vLLM support GGUF    | ❌ No                     |
| RTX 4070 fits IQ3_S  | ❌ No                     |
| llama.cpp works      | ✅ Yes                    |
| CPU offload possible | ✅ Yes (slow)             |
| Best choice          | smaller IQ2 or 14B model |

If you tell me:

* vLLM only?
* OpenClaw?
* Ollama?
* llama.cpp?

I’ll give the **best model for RTX 4070**.