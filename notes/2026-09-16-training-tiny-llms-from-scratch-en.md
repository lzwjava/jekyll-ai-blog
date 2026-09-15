---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Tiny LLMs from Scratch
translated: false
type: note
---

Question: **Intro to Hugging Face’s SmolLM2-135M**

Answer:

[SmolLM2-135M on Hugging Face](https://huggingface.co/HuggingFaceTB/SmolLM2-135M?utm_source=chatgpt.com) is a very small **decoder-only Transformer language model** from Hugging Face's SmolLM2 family.

The interesting part isn't really "135M parameters." It's that this is a relatively complete, open example of **how to train a useful tiny LLM from scratch**.

### 1. What is it?

SmolLM2 comes in:

```text
SmolLM2-135M
SmolLM2-360M
SmolLM2-1.7B
```

The model you're looking at is the smallest one:

```text
~135M parameters
2T pretraining tokens
BF16
64 × H100 GPUs
Transformer decoder
Apache 2.0
English-focused
```

([Hugging Face][1])

Think of it as:

```text
                    SmolLM2-135M
                         │
              ┌──────────┴──────────┐
              │                     │
         Pretraining             Instruct
              │                     │
        2T tokens                 SFT
              │                     │
     next-token prediction        DPO
                                    │
                              UltraFeedback
```

The base model is **not a chatbot**. It learns:

> given tokens `x₁ ... xₜ`, predict `xₜ₊₁`

i.e.

$$
\mathcal L =
-\sum_t \log P_\theta(x_t \mid x_{<t})
$$

That's the whole fundamental objective.

---

### 2. Why is 135M interesting?

135M is tiny by modern LLM standards.

A rough comparison:

```text
GPT-2 small       124M
SmolLM2           135M
Llama 3.2         1B+
Qwen 2.5          0.5B+
```

Yet SmolLM2-135M was trained on **2 trillion tokens**. That's roughly:

$$
\frac{2T}{135M} \approx 14,800
$$

training tokens per parameter.

That's an enormous data/parameter ratio.

So this is a nice model for studying the question:

> **What happens when you make the model extremely small but train it extremely hard?**

Hugging Face explicitly describes SmolLM2 as a data-centric effort, and the 135M model uses FineWeb-Edu, DCLM, The Stack, and additional filtered datasets. ([Hugging Face][1])

---

### 3. Base model vs Instruct model

There are two concepts you should keep separate.

**Base:**

```text
SmolLM2-135M
```

It is basically:

```python
input_ids
    ↓
Transformer
    ↓
logits
    ↓
next token
```

For example:

```text
"The capital of France is"
                         ↓
                       " Paris"
```

It has learned language statistics, knowledge, code, etc., but isn't specifically optimized to follow instructions.

Then:

```text
SmolLM2-135M-Instruct
```

takes the pretrained checkpoint and applies:

```text
base model
    ↓
SFT
    ↓
DPO
    ↓
instruction model
```

The SFT data includes public datasets plus Hugging Face's Smol-SmolTalk dataset, and DPO uses UltraFeedback. ([Hugging Face][1])

So if you're trying to understand **pretraining**, start with `SmolLM2-135M`.

If you're trying to build a tiny agent/chatbot, look at `SmolLM2-135M-Instruct`.

---

### 4. What does the actual Transformer look like?

Conceptually:

```text
tokens
  │
  ▼
Embedding
  │
  ▼
┌─────────────────────┐
│ Transformer Block   │
│                     │
│ RMSNorm             │
│   ↓                 │
│ GQA / Attention     │
│   ↓                 │
│ residual             │
│   ↓                 │
│ RMSNorm             │
│   ↓                 │
│ SwiGLU MLP          │
│   ↓                 │
│ residual             │
└─────────────────────┘
          × N
  │
  ▼
LM Head
  │
  ▼
logits [vocab_size]
```

It's a conventional decoder Transformer rather than some fundamentally new architecture. The model card identifies it as a Transformer decoder. ([Hugging Face][1])

The interesting engineering is therefore less:

> "What novel attention mechanism did they invent?"

and more:

> **How do you make a tiny Transformer surprisingly capable through architecture + data + training?**

---

### 5. The training scale is the crazy part

Hugging Face reports:

```text
Parameters:       135M
Tokens:           2T
Hardware:         64 × H100
Precision:        BF16
Framework:        nanotron
```

([Hugging Face][1])

The rough training FLOPs estimate for a dense autoregressive Transformer is:

$$
C \approx 6NT
$$

where:

* \\(N = 135M\\)
* \\(T = 2T\\)

So:

$$
C \approx 6(1.35\times10^8)(2\times10^{12})
$$

$$
\approx 1.62\times10^{21}
$$

FLOPs.

That's a useful number to keep in mind: **tiny model, enormous token budget**.

---

### 6. What can it actually do?

The base model's benchmark numbers are modest but respectable for its size:

| Benchmark  | SmolLM2-135M |
| ---------- | -----------: |
| HellaSwag  |         42.1 |
| ARC        |         43.9 |
| PIQA       |         68.4 |
| MMLU       |         31.5 |
| Winogrande |         51.3 |
| GSM8K      |          1.4 |

The instruct version improves instruction-following substantially; for example, IFEval goes to 29.9 versus 17.2 for the previous SmolLM-135M-Instruct. ([Hugging Face][1])

But don't interpret 135M as a miniature GPT-4.

At this scale, it is much better thought of as:

```text
excellent research / experimentation model
              +
cheap local model
              +
toy-to-production training substrate
```

rather than a strong general-purpose assistant.

---

### 7. You can run it in ~10 lines

```bash
pip install transformers torch
```

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

name = "HuggingFaceTB/SmolLM2-135M"

tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(
    name,
    torch_dtype=torch.bfloat16,
).cuda()

x = tokenizer("The future of AI is", return_tensors="pt").to("cuda")

y = model.generate(
    **x,
    max_new_tokens=100,
    temperature=0.7,
)

print(tokenizer.decode(y[0]))
```

The official model card provides essentially this loading/generation path. ([Hugging Face][1])

---

### 8. The really interesting experiment for you

Given that you already train models, I'd approach SmolLM2 less as a model to **use** and more as a model to **dissect**.

Clone the training code:

```bash
git clone https://github.com/huggingface/smollm
```

Then reproduce this pipeline:

```text
                    ┌──────────────┐
                    │ Raw corpus   │
                    └──────┬───────┘
                           │
                    filtering /
                    deduplication
                           │
                           ▼
                    ┌──────────────┐
                    │ 2T tokens    │
                    └──────┬───────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ SmolLM2-135M     │
                 │                  │
                 │ embedding        │
                 │ transformer × N  │
                 │ lm_head          │
                 └────────┬─────────┘
                          │
                     next-token CE
                          │
                          ▼
                     checkpoint
                          │
                     SFT / DPO
                          │
                          ▼
                    Instruct model
```

The official repo contains the SmolLM training material and data/training details. ([GitHub][2])

**If your goal is to understand how SmolLM2-135M is actually built**, the next useful step is to walk through its `config.json` and derive the **parameter count layer-by-layer** — embeddings → QKV/GQA → SwiGLU → norms → LM head — until we get to the ~135M number. That's much more educational than just reading the model card.

References:

* [SmolLM2-135M model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M?utm_source=chatgpt.com)
* [SmolLM GitHub repository](https://github.com/huggingface/smollm?utm_source=chatgpt.com)
* [SmolLM2 technical report](https://arxiv.org/abs/2502.02737?utm_source=chatgpt.com)

[1]: https://huggingface.co/HuggingFaceTB/SmolLM2-135M "HuggingFaceTB/SmolLM2-135M · Hugging Face"
[2]: https://github.com/huggingface/smollm/blob/main/text/README.md?utm_source=chatgpt.com "smollm/text/README.md at main · huggingface/smollm · GitHub"
