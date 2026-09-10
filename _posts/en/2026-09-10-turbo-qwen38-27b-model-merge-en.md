---
audio: false
generated: true
image: false
lang: en
layout: post
title: Turbo Qwen3.8 27B Model Merge
translated: false
type: note
---

Question: **What is `DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF`?**

Answer:

This is basically a **community-modified Qwen3.8 27B model**, not a new architecture. It is interesting because the author combines several techniques:

```text
Qwen3.8-27B
      │
      ├── fine-tuning / multi-stage training
      ├── Fable Fusion
      ├── Cold Fusion
      ├── model merging
      ├── Heretic / "abliteration"
      │
      └── GGUF quantization
             │
             ├── regular GGUF
             └── MTP GGUF
```

The author claims it is optimized to be **faster-thinking, coding-oriented, creative, and less refusal-prone** than the original Qwen3.8-27B. ([Hugging Face][1])

### The interesting part: "TURBO"

The author's main claim is that the model produces substantially fewer reasoning tokens.

They report roughly:

> **1/5 to 1/2 of the thinking tokens**, and in some cases as little as **1/10**, compared with regular Qwen3.8. ([Hugging Face][2])

So the intended behavior is approximately:

```text
Normal reasoning model:

question
  ↓
thinking: 10k tokens
  ↓
answer


TURBO:

question
  ↓
thinking: 2k–5k tokens
  ↓
answer
```

That's potentially very useful for **local agents**, because reasoning-token waste is one of the biggest costs of running local thinking models.

---

### "Heretic / Uncensored"

This is the other major distinction.

The model uses **Heretic + custom Arbitrary-Rank Ablation (ARA)** to reduce the model's refusal behavior. The author reports:

```text
                     Original       Stage 1
refusal test          99/100         0/100
```

and after additional tuning:

```text
                     Original       Stage 2
refusal test          86/100        11/100
```

They also report KL divergence of only `0.0025` after Stage 2, meaning the modification was intended to preserve most of the base model's behavior while changing the refusal-related behavior. ([Hugging Face][1])

So **"uncensored" here doesn't mean a completely different pretrained model**. It is closer to:

```text
Qwen3.8
   +
refusal-direction modification
   +
fine-tuning / merging
```

---

### "735-882"

Those numbers come from the author's benchmark claims.

They report:

```text
ARC-C   0.735
ARC-E   0.882
```

versus their listed Qwen3.8-27B baseline:

```text
ARC-C   0.591
ARC-E   0.782
```

They therefore put `735-882` into the model name. ([Hugging Face][1])

**I would not interpret this as an independently verified SOTA claim.** These are the creator's own benchmark results, and the model card contains a lot of promotional language. Treat the numbers as something to reproduce yourself rather than established facts.

---

### "NEO-CODER-MAX"

This is essentially the author's positioning of this particular merge/tune toward **coding + general intelligence**.

The HF tags explicitly include:

```text
coder
thinking
reasoning
creative
roleplaying
conversation
```

and the author describes it as a general-purpose model rather than a pure coding model. ([Hugging Face][1])

For your use case, I'd test it particularly on:

```text
repo navigation
code editing
debugging
bash
Python
agent tool calls
long-horizon coding
```

rather than assuming "coder" in the name means it beats a dedicated coding model.

---

### "MTP"

This part is technically more interesting.

**MTP = Multi-Token Prediction.**

Instead of the model predicting only:

```text
x_t → x_(t+1)
```

MTP trains additional prediction heads to predict multiple future tokens:

```text
x_t
 ├──→ x_(t+1)
 ├──→ x_(t+2)
 ├──→ x_(t+3)
 └──→ ...
```

At inference time, this can potentially allow the runtime to **speculatively generate several tokens at once**, reducing the number of expensive forward passes.

That's particularly relevant to you because you're already interested in **vLLM / SGLang / nano-vLLM**.

The repository specifically provides both **regular GGUF** and **MTP GGUF** variants. ([Hugging Face][3])

---

## What "GGUF" means

This repository is the **llama.cpp-friendly quantized distribution**.

For example:

```bash
llama serve \
  -hf DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF:Q4_K_M
```

The model card explicitly provides this workflow. ([Hugging Face][3])

For your RTX 4070 12GB, **Q4_K_M is the obvious starting point**, although 27B + KV cache means you need to pay attention to context length and offloading.

Very roughly:

```text
27B parameters

FP16       ~54 GB
Q8         ~27–30 GB
Q6         ~21 GB
Q5         ~18 GB
Q4         ~14–16 GB
```

Actual GGUF memory is affected by quantization metadata, KV cache, runtime buffers, etc., so **Q4 does not magically mean "fits comfortably in 12 GB."**

You'd probably want:

```text
4070 12GB
   +
system RAM
   +
llama.cpp GPU offload
```

rather than expecting the whole model to live in VRAM.

---

## My take

The interesting idea isn't simply **"uncensored Qwen."**

It's the combination:

```text
strong 27B base
        +
fine-tuning / merging
        +
refusal ablation
        +
reasoning-token reduction
        +
coding tuning
        +
MTP
        +
GGUF
```

For **local agent experimentation**, that's actually a pretty interesting package.

I'd especially benchmark:

```text
Qwen3.8-27B
vs
DavidAU TURBO
vs
Qwen3.8-27B + your own inference optimizations
```

on:

```text
1. tokens/sec
2. time-to-first-token
3. reasoning tokens / task
4. code benchmark
5. tool-call success
6. SWE-style repo tasks
7. refusal rate
8. VRAM/RAM
```

The key question is whether **"TURBO" really gives you equivalent task quality with dramatically fewer reasoning tokens**. If yes, that's much more interesting for agents than a small improvement on ARC.

[Hugging Face model card](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com)

References:

* [DavidAU model card](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored?utm_source=chatgpt.com)
* [GGUF repository](https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com)

[1]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF · Hugging Face"
[2]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF?hardware=apple-m3-max-96gb&utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF · Hugging Face"
[3]: https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored?utm_source=chatgpt.com "DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored · Hugging Face"
