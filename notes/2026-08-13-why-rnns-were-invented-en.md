---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why RNNs Were Invented
translated: false
type: note
---

Question: Why were RNNs invented?

Answer:

Feedforward nets (MLPs, early CNNs) have a fixed-size input and no memory. Two problems that creates:

**1. Variable-length sequences don't fit a fixed input vector.**
A sentence, a time series, an audio waveform — arbitrary length. You'd need to pad/truncate to some fixed window, which either wastes capacity or loses context. RNNs process one token at a time and carry state forward, so the architecture doesn't care how long the sequence is.

**2. No parameter sharing across positions = no generalization across time.**
If you feed a fixed window into an MLP, position 1 and position 50 get different weights. The network can't recognize "this pattern I saw at t=3" if it shows up again at t=47 — it has to relearn it. RNNs reuse the *same* weight matrices at every timestep:

```
h_t = tanh(W_xh @ x_t + W_hh @ h_{t-1} + b_h)
y_t = W_hy @ h_t + b_y
```

Same `W_xh`, `W_hh`, `W_hy` at every step. This is the actual invention — not "a network with loops" but **weight sharing over time + a hidden state acting as compressed memory of everything seen so far**. `h_t` is a lossy summary of `x_1...x_t`.

Minimal forward pass, numpy, no framework:

```python
import numpy as np

def rnn_forward(xs, h0, Wxh, Whh, Why, bh, by):
    h = h0
    hs, ys = [], []
    for x in xs:                          # x: (input_dim,)
        h = np.tanh(Wxh @ x + Whh @ h + bh)
        y = Why @ h + by
        hs.append(h); ys.append(y)
    return hs, ys

# toy dims
in_dim, hid_dim, out_dim = 4, 8, 2
Wxh = np.random.randn(hid_dim, in_dim) * 0.1
Whh = np.random.randn(hid_dim, hid_dim) * 0.1
Why = np.random.randn(out_dim, hid_dim) * 0.1
bh, by = np.zeros(hid_dim), np.zeros(out_dim)

xs = [np.random.randn(in_dim) for _ in range(10)]  # seq len 10
h0 = np.zeros(hid_dim)
hs, ys = rnn_forward(xs, h0, Wxh, Whh, Why, bh, by)
print(len(hs), hs[0].shape)  # 10 (8,) — same weights, any seq length
```

Historically: Hopfield (1982) showed recurrent dynamics could store memory/attractors. Elman (1990) and Jordan (1986) proposed simple RNNs for language/sequence tasks specifically because MLPs failed at anything with temporal structure — Elman's "Finding Structure in Time" is the canonical motivation paper: language, motor control, time series all have order-dependence an MLP can't capture without a combinatorial blowup in input size.

The follow-up problem RNNs then hit: vanishing/exploding gradients through `Whh` over long sequences (backprop through time multiplies the same matrix repeatedly), which is why LSTM (1997) added gates to control what gets kept vs forgotten in `h_t`, and why transformers eventually replaced RNNs entirely by dropping sequential recurrence for parallel attention.

References:

- [Elman, "Finding Structure in Time" (1990)](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1402_1)
- [Karpathy, "The Unreasonable Effectiveness of RNNs"](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
- [Hochreiter & Schmidhuber, LSTM (1997)](https://www.bioinf.jku.at/publications/older/2604.pdf)
