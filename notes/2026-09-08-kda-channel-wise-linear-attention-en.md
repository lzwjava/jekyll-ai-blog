---
audio: false
generated: true
image: false
lang: en
layout: post
title: "KDA: Channel-Wise Linear Attention"
translated: false
type: note
---

**Question:** What is KDA (Kimi Delta Attention) in LLMs?

**Answer:**

**KDA = Kimi Delta Attention** — a **linear attention** mechanism introduced by the Kimi team as the core of their *Kimi Linear* model family (and later Kimi K3). It is a refinement of *Gated DeltaNet* designed for long-context efficiency.

---

### The Problem it Solves

Traditional linear attention mechanisms maintain a matrix-valued memory state, but suffer from unlimited memory growth and the inability to erase old information.

Standard softmax attention is quadratic O(n²) in sequence length. KDA is a linear-attention mechanism that keeps a fixed-size recurrent state instead of a growing KV cache, making 1M-token context affordable.

---

### The Core Formula

KDA replaces the scalar α_t of Gated DeltaNet with a **channel-wise decay vector** α_t ∈ ℝ^{d_k}:

$$S_t = (I - \beta_t k_t k_t^{\top}) \operatorname{Diag}(\alpha_t) S_{t-1} + \beta_t k_t v_t^{\top}$$

where Diag(α_t) ∈ ℝ^{d_k × d_k} is the diagonal matrix with α_t on its diagonal.

---

### Three Key Components

| Component | Role |
| --- | --- |
| `Diag(α_t)` | Channel-wise forgetting — each feature dimension forgets at its own rate |
| `(I - β_t k_t k_tᵀ)` | Delta rule — targeted overwrite of old memory at current key |
| `β_t` | Scalar write gate — controls how much new value is committed |

Because the weight matrix W maps transformed-key features to values, the diagonal decay matrix multiplies on the right of W and acts along the key-feature dimension. This allows some feature dimensions to be preserved while others are forgotten more aggressively. If the vector gate collapses to a scalar, the update reduces to the scalar-forgetting form used by Gated DeltaNet.

---

### Connecting to Your Code Snippet

The CUDA kernel you posted fuses the gate computations that implement exactly α_t and β_t:

```python
# g[t,h,j] = lower_bound * sigmoid(decay[h] * (raw[t, h*K+j] + dt_bias[h*K+j]))
# This is α_t — the channel-wise decay (one value per key dimension j)

# beta[t,h] = sigmoid(b_raw[t,h])
# This is β_t — the scalar write/erase gate (one value per head)
```

- **`decay[h]`** is the per-head exponential decay (`exp(A_log)`), the global forgetting rate.
- **`dt_bias[h*K+j]`** shifts the raw input per-channel before applying sigmoid — this is what makes α *channel-wise*.
- **`lower_bound`** prevents α from going all the way to zero (catastrophic forget).
- The kernel fuses ~7 separate float ops (cast → bias → sigmoid → multiply) into one elementwise CUDA kernel for efficiency.

---

### Architecture Usage

Kimi Linear uses a 3:1 ratio — for every three transformer blocks employing KDA linear attention, there is one block using full attention. Kimi Linear also replaces the standard full attention module with Multi-Head Latent Attention (MLA), and applies NoPE (No Positional Embedding) in MLA layers, letting MLA run as pure multi-query attention at inference.

---

### KDA vs. Gated DeltaNet

| | Gated DeltaNet | KDA |
| --- | --- | --- |
| Forget gate | Scalar α (same for all channels) | Vector α (per key-channel) |
| Write gate | Scalar β | Scalar β |
| Memory control | Coarse (whole head) | Fine (per feature dimension) |

Gated DeltaNet-2 (a successor) further generalizes KDA by separating the erase gate and write gate, which KDA still ties together as a single scalar β_t.

---

**References:**

- [Kimi Linear explained (Medium)](https://medium.com/@cenghanbayram35/kimi-linear-a-revolutionary-attention-mechanism-for-ai-models-03f4de12047c)
- [KDA topic overview (EmergentMind)](https://www.emergentmind.com/topics/kimi-delta-attention-kda)
- [Linear Attention Architectures paper](https://arxiv.org/pdf/2607.07953)
- [vLLM Kimi K3 support blog](https://vllm.ai/blog/2026-07-27-k3)
- [You Could Have Come Up With KDA (Doubleword)](https://blog.doubleword.ai/you-could-have-come-up-with-kimi-delta-attention)
