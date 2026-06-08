---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tanh Activation Function Explained
translated: false
type: note
---

## Question

Explain tanh (hyperbolic tangent) as an activation function — its role in neural networks, why it matters for RNNs/LSTMs, and how it compares to modern alternatives like ReLU.

## Answer

**Tanh is a zero-centered sigmoid variant that was the default hidden activation before ReLU took over.** Here's what actually matters:

### Core insight: Why zero-centered matters

Sigmoid outputs $(0, 1)$, so all gradients during backprop are *positive*. If your input neurons are mostly firing above 0.5, weight updates always move in one direction — **zigzagging convergence**.

Tanh outputs $(-1, 1)$ with mean 0. This means weights can update in either direction, so **convergence is smoother and faster**. That's the win.

### The math that matters

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

Derivative:
$$\frac{d}{dx}\tanh(x) = 1 - \tanh^2(x)$$

This is elegant — you compute the derivative from the forward pass value alone (one subtraction). Compare to sigmoid's $\sigma(x)(1-\sigma(x))$ which requires two multiplications.

At $x=0$: tanh gradient = 1, sigmoid gradient = 0.25. Early in training, tanh propagates signal 4x better.

### Why it's still essential in LSTMs/GRUs

Modern architectures don't use tanh in hidden layers (ReLU wins on speed and sparsity). But LSTMs use tanh for the *cell state update*:

```python
# LSTM cell update
C_t = f_t * C_{t-1} + i_t * tanh(W_c * [h_{t-1}, x_t] + b_c)
```

Why? Because:
1. **Output range $(-1, 1)$ bounds the cell state** — prevents explosive growth in long sequences
2. **Odd symmetry** ($\tanh(-x) = -\tanh(x)$) makes the gating logic symmetric — forget gate and input gate can cooperate naturally
3. **No dead neurons** — unlike ReLU, every value gets a non-zero gradient

ReLU can't do this. If you use ReLU in cell state updates, values explode without careful layer norm/scaling. Tanh gives you *natural saturation*.

### The real tradeoff

```
ReLU in feedforward/CNN:
  ✅ Fast (single comparison)
  ✅ Sparse activation (50% of neurons off)
  ✅ No gradient vanishing in positive regime
  ❌ Dead neurons (negative inputs = 0 forever)

Tanh in RNN gating:
  ✅ Bounded outputs (-1, 1) — natural saturation
  ✅ No dead neurons
  ✅ Zero-centered
  ❌ Slower (exponentials)
  ❌ Gradient vanishes at extremes (|x| > 3)
```

The gradient vanishing at extremes is fine for LSTM because the *gates* control whether you even reach those regions. The cell state doesn't saturate — it flows.

### Modern context

In transformer-based models (GPT, Claude, DeepSeek), tanh is mostly gone. We use:
- **ReLU/GELU** in feedforward layers (fast, sparse)
- **Softmax** in attention (gating is learned via query-key interaction, not fixed like LSTM gates)

But if you train a small transformer on CPU and need to understand why it works: the attention mechanism *is* learning its own gating logic (via dot products), so the need for bounded activations vanishes.

**TL;DR:** Tanh = zero-centered sigmoid for faster convergence. Irreplaceable in RNNs because its bounded output is essential for gating mechanics. Dead weight in modern transformers because attention handles gating better.
