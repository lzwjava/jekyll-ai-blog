---
audio: false
generated: true
image: false
lang: en
layout: post
title: "TTT: Test-Time Training Explained"
translated: false
type: note
---

Question: **What is TTT in Ilya Sutskever’s/new-model direction?**

Answer: **TTT = Test-Time Training**. The core idea is surprisingly simple:

> **Instead of keeping the model's internal memory as a fixed vector/KV cache, make the memory itself a small trainable model, and update that model while reading the test sequence.**

This is one of the more interesting alternatives to Transformer attention for **very long context**.

### 1. Normal Transformer

For a sequence

```text
x1 x2 x3 ... xt
```

attention essentially stores:

```text
K = [k1, k2, ..., kt]
V = [v1, v2, ..., vt]
```

and the current query searches over all previous tokens:

```python
attention(q_t, K, V)
    = softmax(q_t @ K.T / sqrt(d)) @ V
```

So memory grows with `t`.

Approximately:

```text
KV cache: O(T)
attention computation: O(T²)
```

TTT asks:

> **Why do I need to keep all previous tokens? Why not train a little model to compress what I have seen?**

That little model becomes the **hidden state**.

---

### 2. The key conceptual change

Normal RNN:

```python
h_t = f(x_t, h_{t-1})
```

where `h` is just a vector/tensor.

TTT:

```python
W_t = update(W_{t-1}, x_t)
```

where **`W` itself is a neural network's weights**.

So:

```text
RNN:
    memory = vector

TTT:
    memory = neural network
```

This is the really important idea.

The TTT paper describes exactly this: the hidden state is itself a machine-learning model, and its update is a self-supervised learning step. ([GitHub][1])

---

### 3. A minimal mathematical example

Suppose the fast model is just a linear layer:

```python
y = W @ x
```

When token `x_t` arrives, construct a target `z_t` and minimize:

```math
L_t(W) = ||W x_t - z_t||²
```

Then update:

```math
W_{t+1}
=
W_t - η ∇_W L_t
```

For MSE:

```math
∇_W L
=
2(Wx-z)x^T
```

so:

```math
W_{t+1}
=
W_t - 2η(W_t x_t-z_t)x_t^T
```

That is your **memory update**.

Notice what's happening:

```text
token x_t
   ↓
small model W
   ↓
prediction
   ↓
self-supervised loss
   ↓
gradient
   ↓
update W
```

That's why it's called **training at test time**.

---

### 4. Why this is interesting for LLMs

Imagine reading a 1-million-token book.

Transformer:

```text
token 1 ─┐
token 2 ─┤
token 3 ─┤
   ...
token 1M ┘
      ↓
   KV cache
```

You retain enormous amounts of token-level information.

TTT:

```text
token stream
     ↓
┌───────────────┐
│ fast weights W│
└───────────────┘
     ↑
     │ gradient updates
     │
  new tokens
```

The sequence gets **compressed into the weights of the fast model**.

That's extremely close to:

> **learning instead of remembering.**

The 2025 TTT-E2E work pushes this further: a Transformer with sliding-window attention continues learning through next-token prediction while reading the context, effectively compressing the context into its weights. Their 3B model showed constant inference latency with context length and was reported as **2.7× faster than full attention at 128K context**. ([arXiv][2])

---

### 5. TTT vs KV cache

This is the cleanest mental model:

|                     | Transformer                    | TTT                               |
| ------------------- | ------------------------------ | --------------------------------- |
| Memory              | K/V tensors                    | Model weights                     |
| Update              | append token                   | gradient update                   |
| Query               | attention                      | run fast model                    |
| Memory capacity     | roughly #tokens × dimensions   | capacity of fast model            |
| Long context        | expensive                      | potentially linear                |
| Information storage | explicit token representations | learned/compressed representation |

So TTT is not merely:

> "Let's increase context length."

It's more fundamental:

> **Replace explicit token memory with learned memory.**

---

### 6. There is an important subtlety

Don't interpret TTT as:

```python
# train the entire 7B LLM every time you talk to it
```

That's obviously absurd.

The architecture separates:

```text
slow weights
    ↓
large pretrained model
    ↓
mostly frozen

fast weights
    ↓
small internal learner
    ↓
updated during inference
```

Conceptually:

```python
slow_model = pretrained_model

fast_state = initialize()

for x in sequence:
    fast_state = fast_state - lr * grad(
        self_supervised_loss(fast_state, x),
        fast_state
    )

    y = slow_model(x, fast_state)
```

The **fast weights are temporary state**.

This connects TTT to older ideas like **fast weights, online learning, meta-learning, and learned memory**. ([Test-Time Training][3])

---

### 7. Why Ilya's direction is interesting

I wouldn't equate **Ilya himself with TTT**—TTT was developed by the Stanford/TTT research group, not invented as an SSI/Ilya architecture. But it is highly relevant to the broader direction Ilya has been emphasizing: **future scaling may increasingly come from computation/learning during inference rather than simply more static pretraining**.

Ilya explicitly argued in 2024 that conventional pretraining is approaching a data limitation because humanity has essentially one Internet, while future systems may increasingly generate data and reason/search at inference time. ([Reuters][4])

That's philosophically very compatible with TTT:

```text
Old paradigm:

pretraining
     ↓
frozen model
     ↓
inference


New paradigm:

pretraining
     ↓
model learns how to learn
     ↓
inference
     ↓
continual learning / search / reasoning
     ↓
better solution
```

And the really wild extension is **TTT-Discover**: instead of merely adapting memory to a sequence, the model can actually perform reinforcement learning/search at test time to solve a particular problem. That's much closer to "the model keeps learning while solving the problem." ([Reddit][5])

### The one-sentence intuition

**Transformer:** *"I remember everything I've seen."*

**RNN:** *"I compress everything I've seen into a state vector."*

**TTT:** *"I continuously train a small model to remember what I've seen."*

That last idea is the interesting one. ([GitHub][1])

References:

* [Learning to (Learn at Test Time)](https://arxiv.org/abs/2407.04620?utm_source=chatgpt.com)
* [Official TTT PyTorch implementation](https://github.com/test-time-training/ttt-lm-pytorch?utm_source=chatgpt.com)
* [End-to-End Test-Time Training for Long Context](https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com)

[1]: https://github.com/test-time-training/ttt-lm-pytorch?utm_source=chatgpt.com "GitHub - test-time-training/ttt-lm-pytorch: Official PyTorch implementation of Learning to (Learn at Test Time): RNNs with Expressive Hidden States · GitHub"
[2]: https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com "End-to-End Test-Time Training for Long Context"
[3]: https://testtimetraining.com/?utm_source=chatgpt.com "Test-Time Training: Adaptive Learning at Inference Across AI, Medical Imaging, and Autonomous Systems"
[4]: https://www.reuters.com/technology/artificial-intelligence/ai-with-reasoning-power-will-be-less-predictable-ilya-sutskever-says-2024-12-14/?utm_source=chatgpt.com "AI with reasoning power will be less predictable, Ilya Sutskever says"
[5]: https://www.reddit.com/r/singularity/comments/1ql39n9/learning_to_discover_at_test_time/?utm_source=chatgpt.com "Learning to Discover at Test Time"
