---
audio: false
generated: true
image: false
lang: en
layout: post
title: Matrix Evolution of Sequence Models
translated: false
type: note
---

Question: **Is it important to understand the evolution from RNN/LSTM → Transformer from the matrix perspective, especially for understanding the development of modern LLMs?**

Answer: **Yes. In fact, I think this is one of the best ways for you to organize the entire LLM history.**

The key is not memorizing architectures. It's seeing the evolution as:

> **How do we turn a sequence of vectors into another sequence of vectors, and how does the model make the transformation increasingly data-dependent and parallelizable?**

### 1. Start from the most primitive view: linear transformation

For a token representation:

[
x_t \in \mathbb R^d
]

a basic neural layer is simply

[
y_t = Wx_t
]

where (W) is fixed after training.

The big historical progression is roughly:

```text
Fixed linear transformation
        ↓
RNN: transformation depends on previous state
        ↓
LSTM: better-controlled recurrent state
        ↓
Attention: transformation depends on all tokens
        ↓
Transformer: massively parallel attention + MLP
        ↓
Modern LLMs: scale + better data + better training + better inference
        ↓
Reasoning / TTT / agents / long-context architectures
```

That's a much more useful mental model than memorizing papers.

---

## 2. RNN: matrix multiplication + recurrence

RNN essentially does:

[
h_t = f(W_x x_t + W_h h_{t-1})
]

The interesting thing is that **the matrix operation at time (t) depends on the previous computation**.

```python
h = 0

for x in sequence:
    h = tanh(Wx @ x + Wh @ h)
```

So:

```text
x1 → h1 → h2 → h3 → h4
      ↑    ↑    ↑
     x2   x3   x4
```

This gives you a very important limitation:

### Sequential dependency

You cannot efficiently compute (h_4) before (h_3).

Even though each operation is just matrix multiplication, the **computation graph is sequential**.

That's one of the fundamental reasons RNNs don't scale like Transformers.

---

## 3. LSTM: same recurrence, but better state dynamics

LSTM didn't fundamentally change the idea of recurrence.

It changed the **state update mechanism**.

Very roughly:

[
f_t = \sigma(W_f[x_t,h_{t-1}])
]

[
i_t = \sigma(W_i[x_t,h_{t-1}])
]

[
o_t = \sigma(W_o[x_t,h_{t-1}])
]

[
c_t = f_t\odot c_{t-1}+i_t\odot\tilde c_t
]

The important idea is:

> Instead of forcing one vector (h_t) to simultaneously remember, forget, and expose information, LSTM gives the network explicit control over the state.

So LSTM is still fundamentally:

```text
previous state
      ↓
matrix transformations
      ↓
gates
      ↓
new state
```

The architecture became much better at preserving information over long sequences.

But the fundamental problem remained:

**time-step dependency.**

---

# 4. Attention changes the game

This is the really important transition.

Instead of:

[
h_t = f(x_t,h_{t-1})
]

we can say:

> For token (t), directly look at all other tokens.

Given

[
X\in\mathbb R^{n\times d}
]

compute:

[
Q=XW_Q
]

[
K=XW_K
]

[
V=XW_V
]

and then:

[
A=\operatorname{softmax}\left(\frac{QK^T}{\sqrt d}\right)
]

[
Y=AV
]

Now look carefully at the matrix dimensions:

```text
X       : n × d

Wq      : d × dk
Wk      : d × dk
Wv      : d × dv

Q       : n × dk
K       : n × dk
V       : n × dv

Q @ Kᵀ  : n × n
A @ V   : n × dv
```

The crucial object is:

[
QK^T
]

It creates an **(n\times n) data-dependent matrix**.

That is fundamentally different from a normal fixed weight matrix.

genui{"linear_algebra_optimization":{"type_id":"MATRIX_MULTIPLICATION_ROW_COLUMN_RULE","locale_override":"en-US"}}

---

# 5. This is why your previous "data-dependent linear layer" observation is so powerful

You were discussing this idea recently, and it's actually a very good lens:

> **Attention is a data-dependent linear transformation.**

Because:

[
Y=AV
]

For a given input (X), (A) is generated from (X):

[
A = \operatorname{softmax}(QK^T)
]

So:

```text
Traditional Linear:

Y = WX

W = fixed parameter


Attention:

Y = A(X)V

A = function(X)

A = data-dependent
```

That's a huge conceptual jump.

---

# 6. Transformer = remove recurrence + use data-dependent mixing

The original Transformer essentially says:

> Why process tokens one after another?

Instead, process the whole sequence as a matrix.

```text
RNN

x1 → h1 → h2 → h3 → h4
      ↑    ↑    ↑


Transformer

x1 ─┐
x2 ─┤
x3 ─┼──→ Attention → output
x4 ─┤
x5 ─┘
```

Mathematically:

```text
RNN:

H[t] depends on H[t-1]


Transformer:

H = Attention(X)
```

The entire sequence can participate in huge matrix multiplications.

That maps beautifully onto GPUs.

---

# 7. Then the history of LLMs becomes much easier to understand

I'd organize modern LLM history into several **matrix/computation transitions**.

### 2017 — Transformer

Attention + MLP + residual + normalization.

The fundamental primitive becomes:

[
X \rightarrow \operatorname{softmax}(XW_Q(XW_K)^T)XW_V
]

instead of recurrent state transition.

---

### 2018–2020 — GPT/BERT scaling

The architecture wasn't radically changing.

The industry discovered:

> **Just make the matrix operations bigger and train on more data.**

GPT-2 → GPT-3 is largely a story of scaling:

```text
more parameters
+
more tokens
+
more compute
```

rather than inventing a completely different neural architecture.

---

### 2020–2022 — scaling becomes the dominant paradigm

The important realization was roughly:

[
\text{Performance}
\approx f(\text{parameters},\text{data},\text{compute})
]

This led naturally toward giant Transformer models.

---

### 2022–2024 — instruction tuning / RLHF / chat

The base Transformer wasn't enough.

The stack became:

```text
Pretraining
    ↓
SFT
    ↓
Preference optimization / RLHF
    ↓
Chat model
```

The underlying matrix machinery remained remarkably similar.

---

### 2023–2025 — efficiency becomes critical

Now people started attacking the computational bottlenecks:

```text
Attention
   ↓
FlashAttention
   ↓
GQA / MQA
   ↓
Paged KV cache
   ↓
quantization
   ↓
MoE
```

Notice how much of this is really about:

> **How do we make the matrix computation cheaper?**

---

### 2024–2026 — reasoning changes the inference/training picture

Now the interesting question becomes:

> What if intelligence can improve by spending more computation **after** the model has already been trained?

So you get things like:

```text
Base model
    ↓
longer reasoning
    ↓
search
    ↓
verification
    ↓
tool use
    ↓
agent loops
```

And increasingly, architectures such as **TTT** ask an even deeper question:

> Can the model's parameters themselves adapt during inference?

That's philosophically much closer to:

```text
RNN:
state changes


TTT:
parameters / representations can change
```

rather than simply computing another fixed forward pass.

---

# 8. The really beautiful historical story

If you compress the whole thing:

```text
RNN
│
│  "Remember the past in a state."
│
▼
LSTM
│
│  "Control what to remember/forget."
│
▼
Attention
│
│  "Directly access relevant tokens."
│
▼
Transformer
│
│  "Do the whole sequence with giant matrix ops."
│
▼
Scaling
│
│  "Make the matrices + data + compute enormous."
│
▼
MoE / efficient attention
│
│  "Don't compute everything for everything."
│
▼
Reasoning
│
│  "Spend more inference-time computation."
│
▼
Agents / TTT / adaptive models
│
│  "Let computation/state/parameters adapt over time."
│
▼
???
```

And **that last question is where current research becomes interesting**.

---

## 9. The most useful way for you to study this

Don't study:

> RNN → LSTM → Transformer → GPT → GPT-2 → GPT-3 → GPT-4 → ...

as a list of models.

Study the evolution of the **operator**:

```text
1. Fixed linear map
       Y = WX

2. Recurrent linear map
       h_t = W_x x_t + W_h h_{t-1}

3. Gated state transition
       LSTM(...)

4. Data-dependent token mixing
       Y = softmax(QKᵀ)V

5. Sparse/data-dependent computation
       MoE(X)

6. Inference-time computation
       X → model → reasoning → model → ...

7. Adaptive parameters/state
       θ' = θ + Δθ(X)
```

Then every new architecture becomes much easier to place.

**This is probably the right "spine" for understanding the last ~15 years of deep learning.** Once you understand what changed in the underlying matrix/operator, the papers and model names stop looking like an arbitrary pile of acronyms.