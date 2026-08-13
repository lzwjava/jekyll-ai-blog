---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual GPT-NeoX 4B Model
translated: false
type: note
---

Question: Intro to `rinna/bilingual-gpt-neox-4b`

Answer:

`rinna/bilingual-gpt-neox-4b` is a **Japanese-English bilingual GPT-NeoX decoder-only language model** released by Rinna. It is a good example of a classic **pretrain-from-scratch Transformer LM** before the current Llama/Qwen era. ([Hugging Face][1])

At a high level:

```
Text
 ↓
SentencePiece tokenizer
 ↓
token ids
 ↓
Embedding
 ↓
GPT-NeoX Transformer blocks × 36
 ↓
LM head
 ↓
next token probabilities
```

It is basically:

```
GPT-style autoregressive LM:

P(x) = Π P(x_t | x_<t)
```

Meaning it learns:

> given previous tokens, predict the next token.

Example:

```
Input:
今日は天気が

Model predicts:
良い
```

---

## Model size / architecture

Key numbers: ([Hugging Face][1])

| item         | value                               |
| ------------ | ----------------------------------- |
| Parameters   | 3.8B (~4B)                          |
| Architecture | GPT-NeoX                            |
| Layers       | 36                                  |
| Hidden size  | 2816                                |
| Context      | base model (8K variant also exists) |
| Precision    | FP16                                |
| Languages    | Japanese + English                  |
| License      | MIT                                 |

The architecture:

```
hidden = 2816

for layer in 36:
    x = x + Attention(LayerNorm(x))
    x = x + MLP(LayerNorm(x))
```

Attention:

```
Q = XWq
K = XWk
V = XWv

Attention(Q,K,V)
 = softmax(QKᵀ / sqrt(d))V
```

Same Transformer mechanism you are studying.

---

## Why hidden size 2816?

For GPT-NeoX:

```
hidden_size = 2816

attention heads = ?
```

Usually:

```
head_dim = hidden_size / num_heads
```

For example:

```
num_heads = 22

2816 / 22 = 128
```

So each attention head operates in a 128-dimensional space.

The model internally has:

```
token embedding:

vocab_size × 2816
```

Every token becomes:

```
token id
   |
embedding lookup
   |
2816 dimensional vector
```

Then every Transformer layer transforms this vector.

---

## Training data

The model was pretrained on around **524B tokens** from a mixture including:

* Japanese CC-100
* Japanese C4
* The Pile
* other corpora ([Hugging Face][1])

This is interesting because:

A 4B model with 524B tokens is heavily trained.

Compare Chinchilla scaling:

```
optimal tokens ≈ 20 × parameters

4B × 20
= 80B tokens
```

They used:

```
524B tokens
```

which is much more data than the Chinchilla optimum.

So this model is somewhat **data-rich**.

---

## Relationship to GPT-NeoX

GPT-NeoX was created by EleutherAI.

Architecture:

```
GPT-2
 |
GPT-Neo
 |
GPT-NeoX
 |
rinna bilingual GPT-NeoX
```

The main improvements:

* parallel attention + MLP implementation
* rotary positional embeddings (RoPE)
* better scaling for larger models

The code base is based on EleutherAI GPT-NeoX. ([Hugging Face][1])

---

## Compared with your nanoGPT experiments

Your GPT-2 124M:

```
layers        ~12
hidden        768
params        124M
```

rinna:

```
layers        36
hidden        2816
params        3.8B
```

Approximate comparison:

```
Embedding dimension:

768
 |
2816
(3.7x larger)

Layers:

12
 |
36
(3x deeper)

Parameters:

124M
 |
3.8B
(~30x bigger)
```

The forward pass is conceptually identical.

Your nanoGPT:

```python
x = embedding(tokens)

for block in blocks:
    x = block(x)

logits = lm_head(x)
```

rinna:

```python
x = embedding(tokens)

for block in 36 GPTNeoXBlocks:
    x = block(x)

logits = lm_head(x)
```

Just much larger.

---

## Available variants

The family has:

```
bilingual-gpt-neox-4b
        |
        +-- base model
        |
        +-- instruction-sft
        |
        +-- instruction-ppo
        |
        +-- minigpt4 (vision)
```

The SFT version adds instruction following:

```
base model
      |
      | supervised fine tuning
      ↓
chat model
```

The PPO version adds RLHF alignment. ([Hugging Face][2])

---

## Hardware requirement

FP16 weights:

```
3.8B parameters × 2 bytes

≈ 7.6GB
```

Plus runtime memory:

```
weights        7.6GB
KV cache       depends on context
activations    depends on batch
CUDA overhead  ~1GB
```

Inference:

* RTX 4070 12GB: possible with low batch
* RTX 4090 24GB: comfortable
* CPU: possible quantized

For fine-tuning:

LoRA:

```
12GB GPU: possible
24GB GPU: comfortable
```

Full training:

```
3.8B × optimizer states

FP32 Adam:

weights
+ gradients
+ m
+ v

≈ 16 bytes/parameter

3.8B × 16
≈ 60GB
```

Need distributed GPUs.

---

## Why this model is interesting historically

It represents the transition period:

```
GPT-2 era
(2019)
 |
GPT-NeoX 20B
(2022)
 |
rinna bilingual 4B
(2023)
 |
Llama 2
 |
Qwen / DeepSeek era
```

Today a 4B model seems small, but it was a serious open bilingual model with a large pretraining budget.

For learning Transformer internals, it is actually a very nice size:

* small enough to understand
* large enough to show real scaling behavior
* open weights
* pure decoder Transformer

References:

* [rinna/bilingual-gpt-neox-4b on Hugging Face](https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com)
* [Release of Pre-Trained Models for the Japanese Language paper](https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com)
* [rinna/bilingual-gpt-neox-4b-instruction-sft](https://huggingface.co/rinna/bilingual-gpt-neox-4b-instruction-sft?utm_source=chatgpt.com)

[1]: https://huggingface.co/rinna/bilingual-gpt-neox-4b?utm_source=chatgpt.com "rinna/bilingual-gpt-neox-4b · Hugging Face"
[2]: https://huggingface.co/rinna/bilingual-gpt-neox-4b-instruction-sft?utm_source=chatgpt.com "rinna/bilingual-gpt-neox-4b-instruction-sft · Hugging Face"
