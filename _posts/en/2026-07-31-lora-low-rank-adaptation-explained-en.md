---
audio: false
generated: true
image: false
lang: en
layout: post
title: "LoRA: Low-Rank Adaptation Explained"
translated: false
type: note
---

## Question: What does LoRA mean in LLM?

## Answer:

**LoRA = Low-Rank Adaptation**. It is a technique to fine-tune large language models (LLMs) by training only a small number of additional parameters instead of updating all model weights.

Original paper: LoRA: Low-Rank Adaptation of Large Language Models

---

## 1. The problem: full fine-tuning is expensive

A transformer layer has weight matrices:

```
W ∈ R^(d × d)
```

Example:

Llama-70B:

```
70 billion parameters
≈ 140 GB BF16 weights
```

During training you need:

* model weights
* gradients
* optimizer states (Adam keeps momentum + variance)

Memory:

```
weights       ~140 GB
gradients     ~140 GB
Adam states   ~560 GB

total        ~840 GB+
```

So fine-tuning a 70B model needs huge GPU clusters.

---

## 2. The LoRA idea

Instead of changing the original weight:

```
W
```

freeze it.

Add a small update:

```
W' = W + ΔW
```

But instead of storing a full:

```
ΔW ∈ R^(d × d)
```

LoRA decomposes it:

```
ΔW = B × A
```

where:

```
A ∈ R^(r × d)

B ∈ R^(d × r)
```

`r` is the rank.

Usually:

```
r = 4, 8, 16, 32
```

Much smaller.

---

Example:

Assume:

```
d = 4096
```

Full update:

```
4096 × 4096

= 16,777,216 parameters
```

LoRA:

```
r = 8

A:
8 × 4096
= 32,768

B:
4096 × 8
= 32,768

total:
65,536
```

Reduction:

```
16M → 65K

~250x smaller
```

---

## 3. Forward pass

Normal transformer linear layer:

```
x
 |
 v
Linear

y = Wx
```

LoRA:

```
             frozen
              W
              |
x ----------> Linear --------+
                             |
                             v
                          y1 + y2
                             ^
                             |
x --> A --> B --------------+
       trainable

y2 = BAx
```

Mathematically:

```
y = Wx + BAx
```

During training:

```
W: frozen
A: update
B: update
```

Only LoRA weights receive gradients.

---

## 4. Why low-rank works?

The key observation:

When adapting a pretrained model, the weight changes often have low intrinsic dimension.

Meaning:

A model with billions of parameters may only need a small "direction change".

Example:

Original knowledge:

```
W = general English model
```

Fine tune:

```
ΔW = medical style adjustment
```

The required change is not random.

It is a small subspace:

```
high-dimensional space

        *
       /
      /
-----*------------->
    low rank direction
```

LoRA learns that direction.

---

## 5. Practical example

Base:

```
Llama-8B
```

Instead of:

```
llama-8b-finetuned.bin

8B parameters
```

you save:

```
adapter.bin

~10-100MB
```

Deployment:

```
Llama-8B
+
my_lawyer_LoRA

= lawyer model
```

You can swap adapters:

```
Llama-8B
 |
 +-- coding LoRA
 |
 +-- medical LoRA
 |
 +-- customer service LoRA
 |
 +-- Chinese LoRA
```

One base model, many personalities.

---

## 6. LoRA vs full fine-tuning

|                  | Full FT       | LoRA          |
| ---------------- | ------------- | ------------- |
| Update           | all weights   | small adapter |
| GPU memory       | huge          | small         |
| Training speed   | slower        | faster        |
| Quality          | best possible | close         |
| Storage          | GB-TB         | MB-GB         |
| Multiple domains | expensive     | easy          |

---

## 7. LoRA in modern LLM training stack

Typical pipeline:

```
Base model
    |
    v
SFT dataset
    |
    v
LoRA training
    |
    v
Adapter
    |
    v
Merge(optional)
    |
    v
Production model
```

Tools:

* [Hugging Face PEFT](https://github.com/huggingface/peft?utm_source=chatgpt.com)
* [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory?utm_source=chatgpt.com)
* [Axolotl](https://github.com/axolotl-ai-cloud/axolotl?utm_source=chatgpt.com)

---

## 8. LoRA variants

### QLoRA

Quantized LoRA:

```
Base model:
FP16 → 4-bit

LoRA:
FP16
```

Allows:

```
70B model
+
single 48GB GPU
```

training.

Paper:

QLoRA: Efficient Finetuning of Quantized LLMs

---

### DoRA

Weight-decomposed LoRA:

```
W = magnitude × direction
```

Improves quality closer to full fine-tuning.

---

## 9. For your setup

Given you have:

* RTX 4070 12GB
* trained GPT-2 124M
* experimenting with nanoGPT/vLLM

LoRA is exactly the next step.

Example:

```
Qwen3-8B
+
LoRA adapter
+
your SEC filings dataset
```

Your RTX 4070 cannot full fine-tune 8B, but can do:

```
4-bit QLoRA

8B model
12GB VRAM
```

roughly:

```
base model     ~5GB
LoRA           <1GB
optimizer      few GB

fits
```

A minimal training command:

```bash
pip install transformers peft bitsandbytes trl
```

Conceptually:

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj"
    ]
)

model = get_peft_model(model, config)

model.print_trainable_parameters()
```

Output:

```
trainable params:
~10M

total params:
8B
```

That is the magic of LoRA.

References:

* LoRA paper: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* QLoRA paper: [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)
* Hugging Face PEFT: [https://github.com/huggingface/peft](https://github.com/huggingface/peft)
