---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Qwen Model for RTX 4070
translated: false
type: note
---

Question: **For your RTX 4070 12GB, which uncensored Qwen model should you run locally?**

Answer: **I’d start with Qwen3-8B abliterated, preferably Q8_0.** Your 12 GB VRAM is actually a very comfortable target for 8B.

### My ranking

| Model                    |    Quant |  VRAM-ish | My take                   |
| ------------------------ | -------: | --------: | ------------------------- |
| **Qwen3-8B Abliterated** | **Q8_0** |     ~9 GB | ⭐ Best overall            |
| Qwen3-8B Abliterated     |     Q6_K |     ~7 GB | Great                     |
| Qwen3-8B Abliterated     |   Q4_K_M |     ~5 GB | Fastest / most headroom   |
| Qwen3-14B Uncensored     |   Q4_K_M |     ~9 GB | ⭐ Best quality experiment |
| Qwen3-14B Uncensored     |    Q5/Q6 | 10–12+ GB | Tight on 12 GB            |
| 27B+                     |       Q4 |    >15 GB | Not worth it on one 4070  |

There are currently several Qwen3-8B abliterated variants on HF. ([Hugging Face][1])

### 1. First choice: Qwen3-8B Abliterated Q8

I'd try:

[Rootkit7/Qwen3-8B-abliterated](https://huggingface.co/Rootkit7/Qwen3-8B-abliterated?utm_source=chatgpt.com)

This one is particularly interesting because the author actually tested different quantizations. The Q8_0 is about **8.7 GB**, while Q4_K_M is about **5 GB**. The author reports substantially less refusal with Q8 than Q4. ([Hugging Face][2])

For your 4070:

```bash
# roughly what I'd start with
Qwen3-8B-abliterated-Q8_0.gguf
```

You get enough VRAM left for KV cache and a decent context.

### 2. If you want maximum quality: 14B Q4

There is also:

[mradermacher/Qwen3-14B-Uncensored-GGUF](https://huggingface.co/mradermacher/Qwen3-14B-Uncensored-GGUF?utm_source=chatgpt.com)

It has:

```text
Q4_K_M   9.0 GB
Q5_K_M  10.5 GB
Q6_K    12.1 GB
Q8_0    15.7 GB
```

([Hugging Face][3])

So **Q4_K_M is the sweet spot for your 4070**.

I'd expect:

```text
8B Q8
    ↓
faster
lower memory
good reasoning

14B Q4
    ↓
slower
~9 GB weights
better model capacity
```

For agent/coding workloads, I'd actually benchmark **both**.

### 3. Don't immediately chase the crazy `Heretic / Turbo / Fusion` models

Those names are fun:

```text
Qwen
 → Abliteration
 → Heretic
 → Merge
 → Turbo
 → Fusion
 → NEO
 → GGUF
```

but you're stacking transformations and quantization.

For **research**, I'd rather have a clean baseline:

```text
Qwen3-8B
     ↓
abliteration
     ↓
Q8_0
     ↓
llama.cpp
```

Then compare:

```text
base Qwen3-8B
vs
abliterated Qwen3-8B
vs
Qwen3-14B Q4
```

That gives you an actual controlled experiment.

### 4. On your 4070, I'd run it like this

If you're using llama.cpp:

```bash
./llama-cli \
  -m Qwen3-8B-abliterated-Q8_0.gguf \
  -ngl 99 \
  -c 16384 \
  -t 12
```

For the 14B:

```bash
./llama-cli \
  -m Qwen3-14B-Uncensored.Q4_K_M.gguf \
  -ngl 99 \
  -c 8192 \
  -t 12
```

And benchmark:

```text
tokens/sec
VRAM usage
prompt processing
long-context degradation
coding
tool calling
reasoning
refusal rate
```

**My personal pick for your machine:**

> **Qwen3-8B abliterated Q8_0 → first.**
>
> **Qwen3-14B uncensored Q4_K_M → second.**

The interesting thing is that **8B Q8 may actually be a better local agent than 14B Q4** because you retain much more model precision while staying small enough to run comfortably.

I can also make you a **4070-specific benchmark matrix (8B/14B/30B-A3B × Q4/Q5/Q6/Q8 × llama.cpp/vLLM/SGLang)** so you can decide what to download instead of trial-and-error.

[1]: https://huggingface.co/models?search=Qwen3-8B-abliterated&utm_source=chatgpt.com "Models – Hugging Face"
[2]: https://huggingface.co/Rootkit7/Qwen3-8B-abliterated?utm_source=chatgpt.com "Rootkit7/Qwen3-8B-abliterated · Hugging Face"
[3]: https://huggingface.co/mradermacher/Qwen3-14B-Uncensored-GGUF/tree/main?utm_source=chatgpt.com "mradermacher/Qwen3-14B-Uncensored-GGUF at main"
