---
audio: false
generated: true
image: false
lang: en
layout: post
title: Technical Understanding of Qwen3.8-27B-Uncensored-FP8
translated: false
type: note
---

Question: **What is `orcarouter/Qwen3.8-27B-Uncensored-FP8`, and how should you understand it technically?**

Answer:

[Qwen3.8-27B-Uncensored-FP8 on Hugging Face](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8?utm_source=chatgpt.com) is basically:

> **Qwen3.8-27B + refusal-removal ("abliteration") + FP8 quantization**

It is **not a new model architecture trained from scratch**.

### 1. Start with the base model

The underlying model is **Qwen3.8-27B**, a 27B dense multimodal model. The architecture listed by the uploader is:

```text
64 layers
hidden_size = 5120

48 × Gated DeltaNet / linear-attention layers
16 × full-attention layers

+ vision encoder
+ MTP speculative-decoding head
```

So it's quite interesting architecturally: it isn't a conventional Transformer where every layer is standard softmax attention. It uses **hybrid attention**:

```text
input
  │
  ├── Gated DeltaNet      ← cheap linear recurrence
  ├── Gated DeltaNet
  ├── Gated DeltaNet
  ├── Full Attention      ← every 4th layer
  ├── Gated DeltaNet
  ├── ...
  └── Full Attention
```

The model supports **vision + text**, reasoning/thinking control, tool calling, and MTP speculative decoding. It has a **262,144-token context window** according to this model card. ([Hugging Face][1])

---

### 2. What does "Uncensored" actually mean?

The interesting part is **abliteration**.

The uploader says they performed:

```text
Qwen3.8-27B
      │
      ▼
find refusal direction
      │
      ▼
orthogonalize/remove refusal direction
      │
      ▼
modified weights
      │
      ▼
FP8 quantization
      │
      ▼
Qwen3.8-27B-Uncensored-FP8
```

The goal isn't to retrain the entire model.

Instead, the idea is that refusal behavior corresponds partly to particular directions in the model's residual representations. You identify a "refusal direction" and modify the model so that direction is removed.

The model card explicitly describes this as **"orthogonalizing the refusal direction out of the residual stream."** ([Hugging Face][1])

Conceptually:

```python
# x = residual representation

r = refusal_direction

# remove component of x along r
x_uncensored = x - projection(x, r)

# projection:
projection(x, r) = (x @ r) / (r @ r) * r
```

So:

```text
x
│
│       ↗ refusal direction r
│      /
│     /
│    ●
│   /
│  /
└──────────────

       ↓

remove the component parallel to r

       ●
      /
     /
────●──────────
```

That's why **abliteration is much cheaper than retraining**.

---

### 3. Then why FP8?

The resulting model is quantized to **block FP8 E4M3**.

The model card says:

```text
weight_block_size = [128, 128]
activation = dynamic
weights = FP8 E4M3
```

while some components remain BF16:

```text
FP8:
    linear weights

BF16:
    vision tower
    norms
    router
    embeddings
    lm_head
```

The resulting files are about **30.9 GB**, split into 7 safetensors shards. ([Hugging Face][1])

So don't think:

```text
27B × 1 byte = 27 GB
```

exactly.

There is FP8 metadata/scales plus BF16 components, etc., giving roughly **31 GB on disk**.

---

### 4. Why this model is interesting for you

I'd actually put this model into a very useful learning category:

```text
                 Qwen3.8
                    │
          ┌─────────┴─────────┐
          │                   │
     architecture         post-training
          │                   │
    hybrid attention       alignment
    DeltaNet               refusal
    full attention         safety
    vision                 RL/SFT
    MTP                    abliteration
          │                   │
          └─────────┬─────────┘
                    │
                 quantization
                    │
                  FP8
```

You can study **three different pieces of modern LLM engineering from one checkpoint**:

1. **Hybrid architecture**

   * Gated DeltaNet
   * full attention
   * multimodal tower
   * MTP

2. **Model modification**

   * refusal-direction discovery
   * activation-space manipulation
   * abliteration

3. **Inference optimization**

   * block FP8
   * vLLM
   * MTP speculative decoding
   * 262K context

That's substantially more educational than just downloading a random GGUF.

---

### 5. Can you run it on your 24 GB GPU?

**Not comfortably as a single GPU.**

The checkpoint itself is ~31 GB, and that's before considering:

```text
weights
+ KV cache
+ activations
+ CUDA workspace
+ vision model
```

So 24 GB VRAM isn't enough for the straightforward FP8 deployment.

The official model card specifically provides vLLM and SGLang serving instructions. ([Hugging Face][1])

For example:

```bash
pip install vllm

vllm serve \
  orcarouter/Qwen3.8-27B-Uncensored-FP8
```

But you'd want **more than 24 GB VRAM**, or multi-GPU/offloading/another quantization format.

---

### 6. One important distinction

"Uncensored" does **not** mean:

```text
better intelligence
```

It primarily means:

```text
less refusal / fewer safety-alignment constraints
```

The uploader explicitly warns that abliteration can affect behavior beyond simply removing refusals, and the model is intended for research/red-teaming rather than directly exposing it to end users. ([Hugging Face][1])

So scientifically, the interesting question is actually:

> **How much capability survives after modifying the representation responsible for refusal behavior?**

That's much more interesting than "can it generate uncensored content?"

The model card includes separate evaluations for **harmful-prompt refusal, over-refusal, capability retention, reasoning, and vision**, which is exactly the kind of experiment you'd want to inspect if you're studying model surgery. ([Hugging Face][1])

### My recommendation

Given that you're learning **model training + inference**, I'd study this in this order:

```text
Qwen3.8 architecture
       ↓
Gated DeltaNet
       ↓
Qwen multimodal forward pass
       ↓
MTP
       ↓
FP8 block quantization
       ↓
abliteration
       ↓
vLLM implementation
```

The **abliteration + FP8 combination is particularly worth reproducing yourself**: take a small open model, identify a refusal direction, remove it, evaluate before/after, then quantize it. That gives you a concrete end-to-end **"model surgery → quantization → inference"** project rather than merely learning how to call an LLM API. ([Hugging Face][1])

References:

* [Qwen3.8-27B-Uncensored-FP8 model card](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8?utm_source=chatgpt.com)
* [Qwen official models](https://huggingface.co/Qwen/models?utm_source=chatgpt.com)

[1]: https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8 "orcarouter/Qwen3.8-27B-Uncensored-FP8 · Hugging Face"