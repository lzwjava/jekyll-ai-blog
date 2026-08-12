---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recurrent-Depth Transformer Introduction
translated: false
type: note
---

## Question: Introduction to OpenMythos

## Answer:

[OpenMythos GitHub Repository](https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com) is an interesting experimental project by Kye Gomez that tries to **reconstruct a possible next-generation Transformer architecture from first principles**. It is **not an official Claude implementation**; the author explicitly describes it as an independent theoretical reconstruction based on public research and speculation. ([GitHub][1])

The core idea:

> Instead of making Transformers deeper by stacking more unique layers, reuse some layers multiple times inside one forward pass.

This is called a **Recurrent-Depth Transformer (RDT)** or **Looped Transformer**. ([GitHub][2])

---

## 1. Normal Transformer vs OpenMythos

A normal LLM:

```
x
 ↓
Transformer Block 1
 ↓
Transformer Block 2
 ↓
Transformer Block 3
 ↓
...
 ↓
Transformer Block N
 ↓
logits
```

Every layer has different parameters:

```
Layer1: W1
Layer2: W2
Layer3: W3
...
LayerN: WN
```

Depth = number of layers.

---

OpenMythos:

```
x
 ↓
Prelude
 ↓
Recurrent Block
      ↻
      ↻
      ↻
 ↓
Coda
 ↓
logits
```

The middle block is reused:

```
h1 = Block(h0)
h2 = Block(h1)
h3 = Block(h2)
...
hT = Block(hT-1)
```

Same weights:

```
Block parameters = W

apply:
W(h0)
W(h1)
W(h2)
...
```

So instead of:

```
96 unique layers
```

you could have:

```
12 layers
+
8 recurrent iterations
=
96 effective computation depth
```

but with fewer parameters.

---

## 2. Why this idea?

The intuition:

A human does not always need more "knowledge" to solve a problem.

Sometimes you need more **thinking steps**.

Traditional Transformer:

```
more reasoning ability
        |
        v
more layers
        |
        v
more parameters
```

OpenMythos hypothesis:

```
more reasoning ability
        |
        v
more computation steps
        |
        v
reuse existing network
```

This is related to:

* Universal Transformers
* Deep Equilibrium Models
* Adaptive Computation Time (ACT)
* recurrent neural networks

---

## 3. The forward pass

From the repo:

```
Input token IDs
      |
Embedding
      |
Prelude Transformer
      |
Recurrent Block
      |
Coda Transformer
      |
RMSNorm
      |
LM Head
```

The recurrent update:

[
h_{t+1}=A h_t + B e + Transformer(h_t,e)
]

where:

* `h_t`: current hidden state
* `e`: original encoded input
* `A`, `B`: learned parameters

The input injection is important.

Without it:

```
h0
 ↓
Block
 ↓
h1
 ↓
Block
 ↓
h2
```

After many loops, information may drift.

With injection:

```
h0 + input signal
      |
      v
Block
      |
      v
h1 + input signal
      |
      v
Block
```

The model keeps access to the original representation. ([GitHub][3])

---

## 4. It combines several modern LLM ideas

OpenMythos is basically a "research playground" combining:

### Attention

Supports:

### GQA

Grouped Query Attention:

```
many Q heads

share fewer KV heads
```

Goal:

reduce KV cache.

---

### MLA

Multi-Latent Attention from DeepSeek:

Instead of:

```
cache:

K:
seq × heads × head_dim

V:
seq × heads × head_dim
```

compress:

```
latent KV:

seq × low_rank_dim
```

then reconstruct.

This reduces inference memory.

---

### MoE

Instead of one huge MLP:

```
token
 |
 |
MLP
```

use experts:

```
token
 |
router
 |
+---- Expert 1
|
+---- Expert 2
|
+---- Expert 3
```

Only activate some experts.

The repo implements sparse MoE with routed and shared experts. ([GitHub][2])

---

## 5. Relationship with current LLM research

The interesting part is not the code size; it is the direction.

The Transformer scaling recipe:

```
more data
more parameters
more GPUs
```

is expensive.

Researchers are exploring:

### 1. Better parameter efficiency

Example:

```
MoE
MLA
LoRA
weight sharing
```

### 2. Better inference-time scaling

Instead of:

```
train bigger model
```

do:

```
same model
think longer
```

Examples:

```
o1-style reasoning
test-time compute
recurrent depth
```

OpenMythos belongs to this family.

---

## 6. Simple PyTorch version

The core idea is only this:

```python
class LoopedTransformer(nn.Module):
    def __init__(self, block, loops):
        super().__init__()
        self.block = block
        self.loops = loops

    def forward(self, x):
        for _ in range(self.loops):
            x = self.block(x)
        return x
```

Compare:

Normal:

```python
layers = [
    Block(),
    Block(),
    Block(),
    Block()
]
```

Parameters:

```
4 × block_parameters
```

Loop:

```python
block = Block()

for i in range(4):
    x = block(x)
```

Parameters:

```
1 × block_parameters
```

Computation depth is similar, parameter count is smaller.

---

## My view

The most interesting idea here is not "Claude reconstruction". The deeper idea is:

> Transformer layers may be closer to iterative algorithms than fixed-depth feed-forward networks.

A Transformer layer is a learned update rule:

[
h_{t+1}=f_\theta(h_t)
]

Today:

```
apply f1, f2, f3...
```

Future:

```
apply f repeatedly until enough computation
```

This connects LLMs with classical iterative optimization:

* gradient descent
* numerical solvers
* recurrent systems

OpenMythos is basically asking:

**Can a language model learn its own internal reasoning loop instead of having reasoning depth fixed at architecture design time?**

That is the important research direction. ([GitHub][2])

References:

* [OpenMythos GitHub](https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com)
* [OpenMythos Documentation](https://github.com/kyegomez/OpenMythos/blob/main/docs/open_mythos.md?utm_source=chatgpt.com)
* [OpenMythos PyPI](https://pypi.org/project/open-mythos/?utm_source=chatgpt.com)

[1]: https://github.com/kyegomez/OpenMythos/blob/main/README.md?utm_source=chatgpt.com "OpenMythos/README.md at main · kyegomez/OpenMythos · GitHub"
[2]: https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com "GitHub - kyegomez/OpenMythos: A theoretical reconstruction of the Claude Mythos architecture, built from first principles using the available research literature. · GitHub"
[3]: https://github.com/kyegomez/OpenMythos/blob/main/docs/open_mythos.md?utm_source=chatgpt.com "OpenMythos/docs/open_mythos.md at main · kyegomez/OpenMythos · GitHub"