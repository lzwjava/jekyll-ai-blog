---
audio: false
generated: true
image: false
lang: en
layout: post
title: "XLNet: Overcoming BERT's Limitations"
translated: false
type: note
---

## Question: Introduction to XLNet, the work from Zhilin Yang

Zhilin Yang is one of the main authors behind **XLNet: Generalized Autoregressive Pretraining for Language Understanding** (2019), a major NLP model that competed with Google's BERT and influenced later Transformer models.

Paper:
**XLNet: Generalized Autoregressive Pretraining for Language Understanding**
Authors: Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, Quoc V. Le

---

## 1. Why XLNet existed: BERT's limitation

Before XLNet:

### GPT (2018)

Autoregressive:

```
x1 → x2 → x3 → x4
```

Training objective:

[
P(x)=\prod_t P(x_t|x_{<t})
]

It predicts the next token.

Problem:

* only learns left-to-right dependency
* cannot see future tokens

---

### BERT (2018)

BERT introduced **masked language modeling (MLM)**:

Input:

```
The cat [MASK] on the mat.
```

Predict:

```
sat
```

BERT sees both sides:

```
The cat <MASK> on the mat
          ↑
     left + right context
```

Advantage:

* bidirectional representation

Problem:

The training objective does not match real generation.

During training:

```
The cat [MASK] on the mat
```

During inference:

```
The cat sat on the mat
```

The model never sees `[MASK]` at inference.

This creates **pretrain-finetune discrepancy**.

---

# 2. XLNet's key idea: Permutation Language Modeling

XLNet combines:

* GPT's autoregressive objective
* BERT's bidirectional context

The trick:

Instead of predicting tokens in fixed order:

```
1 → 2 → 3 → 4
```

randomly choose an ordering.

Example:

Original sentence:

```
A B C D
```

Permutation:

```
C A D B
```

Training:

Predict:

```
C
given nothing

A
given C

D
given C,A

B
given C,A,D
```

Mathematically:

[
P(x)=
\prod_t P(x_{z_t}|x_{z_{<t}})
]

where:

* z is a random permutation

---

## 3. Why this gives bidirectional context

Example:

Sentence:

```
I love machine learning
```

Predict:

```
machine
```

A normal GPT:

```
I love → machine
```

Only sees:

```
I love
```

XLNet can sample:

```
learning → machine
```

So when predicting "machine":

```
I love
+
learning
```

both sides can contribute.

It learns:

```
left context + right context
```

without using `[MASK]`.

---

# 4. Transformer-XL connection

XLNet was built on top of Transformer-XL.

Transformer-XL introduced:

## Segment recurrence

Normal Transformer:

```
tokens
 ↓
attention
 ↓
forget everything
```

Transformer-XL:

```
segment 1
    ↓
memory
    ↓
segment 2
```

It keeps previous hidden states:

[
h_{t-1}
]

as memory.

Benefits:

* longer context
* faster training
* better long-document understanding

XLNet used this because language modeling needs long-range dependencies.

---

# 5. XLNet architecture

High level:

```
Text
 |
Tokenizer
 |
Transformer-XL backbone
 |
Permutation attention
 |
Language modeling head
 |
Next-token prediction
```

It is still a decoder-style Transformer.

Unlike BERT:

```
BERT:
Encoder Transformer
```

XLNet:

```
Autoregressive Transformer
```

---

# 6. Two-stream attention

A very important technical detail.

Problem:

If predicting token x3, the model cannot directly know x3 itself.

XLNet uses:

## Content stream

Normal hidden representation:

[
h_t
]

contains token information.

## Query stream

Prediction representation:

[
g_t
]

does not contain the target token.

Example:

Predict:

```
C
```

Query:

```
A B ?
```

Content:

```
A B C
```

The query attends to content but not itself.

This prevents information leakage.

---

# 7. XLNet vs BERT vs GPT

| Model              | Objective      | Context    |
| ------------------ | -------------- | ---------- |
| GPT                | next token     | left only  |
| BERT               | masked token   | both sides |
| XLNet              | permutation AR | both sides |
| GPT-4 style models | AR scaling     | left only  |

---

# 8. Why XLNet did not dominate later

XLNet was extremely strong in 2019:

* beat BERT on many benchmarks
* introduced better objectives

But later, scaling changed everything.

The industry moved toward:

```
simple objective
+
huge data
+
huge compute
```

The GPT-style objective won because:

1. It is naturally generative
2. Easier scaling
3. Works directly for chat
4. Better engineering ecosystem

Today:

```
GPT-3
GPT-4
Llama
Qwen
DeepSeek
```

all use causal autoregressive training.

---

# 9. Historical importance

The evolution:

```
RNN/LSTM
    |
    v
Transformer (2017)
    |
    +---- GPT (autoregressive)
    |
    +---- BERT (masked modeling)
    |
    +---- Transformer-XL (long memory)
              |
              v
            XLNet
              |
              v
       Modern large language models
```

XLNet was one of the last major attempts to improve the pretraining objective before the field discovered:

> Scaling a simple autoregressive Transformer beats designing a more clever objective.

---

# 10. Zhilin Yang's broader contribution

Zhilin Yang worked on several important NLP topics:

* XLNet
* Transformer-XL
* language modeling
* representation learning

His work helped bridge:

```
small NLP models
      ↓
large-scale pretrained language models
```

The core insight of XLNet was:

> You can keep the mathematically clean autoregressive objective while recovering the bidirectional information flow that made BERT powerful.

That idea influenced how researchers think about **attention, information flow, and training objectives** in modern LLMs.

References:

* Yang et al., "XLNet: Generalized Autoregressive Pretraining for Language Understanding" (2019): [https://arxiv.org/abs/1906.08237](https://arxiv.org/abs/1906.08237)
* Dai et al., "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context" (2019): [https://arxiv.org/abs/1901.02860](https://arxiv.org/abs/1901.02860)
* Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2018): [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)
