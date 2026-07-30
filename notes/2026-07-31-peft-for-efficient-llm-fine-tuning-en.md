---
audio: false
generated: true
image: false
lang: en
layout: post
title: PEFT for Efficient LLM Fine-Tuning
translated: false
type: note
---

Question: intro to Hugging Face PEFT (`huggingface/peft`)

Answer:

Hugging Face PEFT (**Parameter-Efficient Fine-Tuning**) is the main library for adapting large language models without updating all model weights.

Repository: [Hugging Face PEFT GitHub](https://github.com/huggingface/peft?utm_source=chatgpt.com)

The core idea:

> Full fine-tuning: update billions of parameters.
> PEFT: freeze the base model, train a tiny number of extra parameters.

Example:

```
Llama/Qwen model
        |
        | freeze
        v
+----------------+
| pretrained LLM |
| 7B parameters  |
+----------------+
        |
        +---- add LoRA adapters
              |
              v
        train ~10M params
```

Instead of:

```
7,000,000,000 parameters
all require gradients
```

you train:

```
~5,000,000 - 50,000,000 parameters
```

Much cheaper.

---

## Why PEFT exists

Suppose you have:

* Qwen3-8B
* Llama-3-8B
* Mistral-7B

Full fine-tuning:

```
8B params × fp16
≈ 16GB weights

optimizer states (Adam)
≈ 32GB+

gradients
≈ 16GB+

total:
60GB-100GB VRAM
```

Hard for normal GPUs.

With LoRA:

```
Base model:
8B params
frozen

LoRA:
10M-100M params
trainable
```

Your RTX 4070 12GB can actually do useful fine-tuning.

---

# Main algorithms supported by PEFT

## 1. LoRA (most popular)

Low-Rank Adaptation.

Original weight:

```
W
```

Instead of changing W:

```
W' = W + ΔW
```

LoRA represents:

```
ΔW = A × B
```

where:

```
W:
4096 × 4096

A:
4096 × r

B:
r × 4096

r = 8 / 16 / 32
```

Example:

```
4096 * 4096
= 16M parameters

LoRA rank 8:

4096*8 + 8*4096
= 65K parameters
```

Huge reduction.

---

## 2. QLoRA

Combination:

```
4-bit quantized base model
+
LoRA adapter
```

Architecture:

```
          frozen
       4-bit Qwen
            |
            |
        forward pass
            |
            v
       LoRA adapter
            |
            |
       gradients only here
```

Popular stack:

```
transformers
      |
      |
     PEFT
      |
      |
 bitsandbytes
```

Example:

```python
from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B"
)

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj"
    ],
)

model = get_peft_model(model, config)

model.print_trainable_parameters()
```

Output:

```
trainable params:
~10M

all params:
8B

trainable:
0.1%
```

---

# PEFT architecture

High level:

```
transformers
     |
     |
     v
+-------------+
| Base Model  |
| Llama/Qwen  |
+-------------+
       |
       |
       v

+-------------+
| PEFT Wrapper|
+-------------+
       |
       |
       +---- LoRA
       |
       +---- Prefix tuning
       |
       +---- Prompt tuning
       |
       +---- IA3
```

---

# Other PEFT methods

## Prefix tuning

Instead of modifying weights:

add virtual tokens:

```
Input:

[system][user][question]

becomes:

[prefix tokens][system][user][question]
```

Train only prefix embeddings.

---

## Prompt tuning

Even smaller:

```
Train:

soft prompt embeddings

instead of model weights
```

---

## IA3

Adjust activations:

```
hidden_state * learned_vector
```

Very small.

---

# Typical modern LLM training pipeline

Today many open-source models use:

```
Pretraining
    |
    |
    v
Base model
    |
    |
    +---- SFT
    |       |
    |       +-- PEFT LoRA
    |
    |
    +---- RLHF / DPO / GRPO
            |
            +-- PEFT
```

Example:

```
Qwen3-8B base
       |
       |
       v
instruction dataset
       |
       |
       v
LoRA SFT
       |
       |
       v
Qwen3-8B-my-domain
```

---

# For your setup (RTX 4070 12GB)

PEFT is exactly the tool to explore.

Good experiments:

## 1. Fine-tune a small coding model

```
Qwen3-4B
+
LoRA
+
your Java/Python code dataset
```

## 2. Reasoning process training

You previously asked about RL/reasoning training.

A practical path:

```
Base model
(Qwen3-8B)

        |
        |
        v

SFT with reasoning traces
        |
        |
        v

LoRA adapter


        |
        |
        v

GRPO/DPO
```

You don't need to retrain the whole model.

---

# Minimal training stack in 2026

Most people use:

```
transformers
      +
datasets
      +
peft
      +
trl
      +
accelerate
      +
bitsandbytes
```

Example:

```
pip install transformers peft trl accelerate bitsandbytes
```

---

# How PEFT fits your learning path

Given you already:

* trained GPT-2 124M from scratch
* played with nanoGPT
* run Qwen models locally
* have RTX 4070

The next logical jump is:

```
nanoGPT
   |
   |
   v
transformers internals
   |
   |
   v
PEFT LoRA
   |
   |
   v
TRL (DPO/GRPO)
   |
   |
   v
agent/model alignment
```

PEFT is not about "training a model from zero".

It is about **turning a general LLM into your specialized model cheaply**.

References:

* Hugging Face PEFT GitHub: [https://github.com/huggingface/peft](https://github.com/huggingface/peft)
* LoRA paper: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* QLoRA paper: [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)
