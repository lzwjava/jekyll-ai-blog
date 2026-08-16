---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Mamba: Selective State Space Model for LLMs"
translated: false
type: note
---

Question: **What does Mamba mean in LLMs?**

Answer:

**Mamba is a neural network architecture for sequence modeling that replaces Transformer self-attention with a more efficient mechanism called a *Selective State Space Model (SSM)*.**

The key idea is:

> **Instead of asking every token to attend to every other token, Mamba maintains a compact hidden state that is updated as tokens arrive.**

### 1. Transformer vs. Mamba

A Transformer layer roughly does:

```text
x₁ ─┐
x₂ ─┤
x₃ ─┤──> Self-Attention ──> y₁,y₂,y₃,...
x₄ ─┤
... ┘
```

For each token, attention computes:

[
\text{Attention}(Q,K,V)
=======================

\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
]

So with sequence length (L), the attention matrix is roughly:

```text
L × L
```

This is why vanilla attention has **O(L²)** interaction cost.

Mamba instead looks more like:

```text
x₁ ──> state₁ ──> y₁
          │
x₂ ──────>state₂ ──> y₂
             │
x₃ ─────────>state₃ ──> y₃
                │
x₄ ────────────>state₄ ──> y₄
```

There is a recurrent state:

[
h_t = f(h_{t-1}, x_t)
]

and output:

[
y_t = g(h_t, x_t)
]

So the model doesn't need to explicitly construct an (L\times L) attention matrix.

---

### 2. What is the "S" in SSM?

A classical state-space model has something like:

[
h_t = Ah_{t-1} + Bx_t
]

[
y_t = Ch_t
]

Think of:

* (x_t): current token
* (h_t): model's memory
* (A): how previous memory is preserved/transformed
* (B): how new input enters memory
* (C): how memory produces output

This is basically a **learned recurrent memory**.

The problem with older SSMs was that their parameters were relatively fixed.

Mamba's important trick is:

> **Make the state-space parameters depend on the current input.**

Conceptually:

```python
B_t = f_B(x_t)
C_t = f_C(x_t)
Δ_t = f_Δ(x_t)

h_t = A(Δ_t) @ h_{t-1} + B_t @ x_t
y_t = C_t @ h_t
```

Therefore the model can learn:

```text
"this token is important → remember it"

"this token is irrelevant → forget it"

"this token changes the meaning → update state strongly"
```

That's why it is called **Selective** State Space.

---

### 3. Why is this interesting for LLMs?

The fundamental tradeoff is:

|                               | Transformer        | Mamba                    |
| ----------------------------- | ------------------ | ------------------------ |
| Core mechanism                | Attention          | SSM                      |
| Training sequence interaction | O(L²) attention    | ~O(L)                    |
| KV cache during generation    | grows with context | much smaller/fixed state |
| Long context                  | expensive          | potentially much cheaper |
| Random access to old tokens   | excellent          | weaker                   |
| Mature ecosystem              | excellent          | newer                    |

The really interesting part is inference.

For a Transformer generating token (t), you generally keep a **KV cache**:

```text
K₁ V₁
K₂ V₂
K₃ V₃
...
Kₜ Vₜ
```

The cache grows with sequence length.

Mamba can instead maintain something conceptually like:

```text
state
  ↓
constant-size memory
  ↓
next token
```

So its recurrent state doesn't grow linearly with context length.

---

### 4. Why "Mamba" specifically?

The name comes from the **mamba snake**. The architecture was introduced in the paper:

**"Mamba: Linear-Time Sequence Modeling with Selective State Spaces"** by Albert Gu and Tri Dao, 2023.

The important conceptual contribution isn't the name. It's:

```text
SSM
 ↓
input-dependent / selective parameters
 ↓
efficient recurrent state
 ↓
linear-time sequence modeling
```

---

### 5. Mamba is not simply "RNN 2.0"

This is the interesting part.

A naive RNN:

```python
h = RNN(h, x)
```

has trouble with:

* long-range dependencies
* vanishing/exploding gradients
* efficient parallel training

Mamba/SSMs are designed so that the recurrence has mathematical structure that permits **parallel computation during training**, while still behaving like a recurrent model during inference.

So you get an interesting hybrid:

```text
Training:

x₁ x₂ x₃ x₄ x₅ x₆
 └──── parallel hardware-friendly computation ────┘


Inference:

x₁ → state → x₂ → state → x₃ → state → ...
```

This is one of the reasons Mamba is interesting from a systems perspective.

---

### 6. The deeper idea

I would frame the Transformer → Mamba difference this way:

**Transformer:**

> "Given this token, retrieve relevant information from the entire sequence."

**Mamba:**

> "As I read the sequence, continuously decide what information deserves to remain in my state."

So they're two different approaches to **memory**.

```text
Transformer
    │
    └── external memory = all previous K/V
             ↓
       retrieve with attention


Mamba
    │
    └── compressed memory = hidden state
             ↓
       selectively update state
```

This also explains Mamba's fundamental weakness:

**compression can lose information.**

If an important fact from 20,000 tokens ago was compressed incorrectly into the state, Mamba doesn't have the Transformer's ability to simply go back and retrieve the original token.

Attention effectively says:

```text
"I'll keep the whole database and search it."
```

Mamba says:

```text
"I'll continuously summarize what matters."
```

That is probably the most useful mental model.

### References

* [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752?utm_source=chatgpt.com)
* [Mamba official GitHub repository](https://github.com/state-spaces/mamba?utm_source=chatgpt.com)
* [Transformers: Attention Is All You Need](https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com)