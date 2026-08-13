---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Transformer vs RNN: Training-Inference Tradeoff"
translated: false
type: note
---

Question: Is it true that Transformer (attention + KV cache) is training-friendly but inference-unfriendly, while RNN is the opposite (inference-friendly, training-unfriendly)?

Answer: Yes, that's the correct standard characterization — it's literally the motivating tension behind Mamba/RWKV/RetNet/SSMs. Let me walk the mechanics.

**Transformer: parallel training, serial+memory-bound inference**

Training uses teacher forcing — the full target sequence is known upfront, so masked self-attention computes all positions in one shot:

```
Q, K, V = X @ Wq, X @ Wk, X @ Wv        # X: [T, d], one matmul, all T positions
scores = Q @ K.T / sqrt(d)               # [T, T]
scores = scores.masked_fill(causal_mask, -inf)
attn = softmax(scores) @ V               # [T, d]
```

No position waits on another position's *output* — the causal mask just zeroes out illegal attention weights inside one big parallel matmul. This is why Transformers saturate GPUs beautifully: it's O(1) sequential depth (per layer), O(n²) FLOPs, all dense matmuls.

Inference is the opposite. You generate token t+1 one at a time, and each step needs attention over *all* previous keys/values:

```
# decode step t
k_t, v_t = x_t @ Wk, x_t @ Wv
kv_cache_k.append(k_t); kv_cache_v.append(v_t)   # cache grows every step
scores = q_t @ kv_cache_k.T                       # O(t) compute
out = softmax(scores) @ kv_cache_v
```

You avoid recomputing K/V for old tokens (that's what the cache buys you), but:

- Memory: O(n) and grows with context — cache size = `2 × layers × heads × head_dim × n × batch × bytes`.
- Every step you must *read the entire cache from HBM* just to produce one token → arithmetic intensity collapses → decode is memory-bandwidth bound, not compute bound. this avoids recomputation and makes inference much faster, but comes with a simple tradeoff: the cache size grows linearly with sequence length — the longer the context, the more memory it consumes, and LLMs are not compute-bound, they are memory-bound
- This is why long context wrecks serving economics — decode is often memory-bandwidth bound, not compute-bound; on a 70B model on an 80GB H100, a 4K context supports ~59 concurrent users but 128K context drops to ~1 user.

**RNN: cheap inference, sequential training**

Inference step is O(1) memory and O(1) compute regardless of how long the sequence has been, because all history is compressed into a fixed-size hidden state:

```
h_t = tanh(Wx @ x_t + Wh @ h_{t-1} + b)   # constant size, no cache growth
```

Training (BPTT) is where it hurts: `h_t` *depends on* `h_{t-1}`'s actual output, not just a mask — you can't compute step t until step t-1 is done. That's a hard sequential dependency chain of length T, so you can't collapse the sequence into one big matmul the way attention does. Low GPU utilization, plus vanishing/exploding gradients across long chains.

**Why this matters practically**

This exact asymmetry is why the SSM/linear-RNN wave (Mamba, RWKV, RetNet) exists — they're built with a recurrent form (cheap, O(1) inference, like RNN) that also admits a parallel-scan / chunked form (dense matmul, cheap training, like Transformer):

RWKV integrates a linear attention mechanism, enabling parallelizable training like transformers while retaining the efficient inference characteristics of RNNs, achieving constant computational and memory complexity during inference. Mamba enjoys linear-time scaling during training, and constant memory cost during inference as the entire state is summarized in a fixed size tensor, offering up to 5× higher throughput in inference tasks.

| | Transformer (attn+KV cache) | RNN | Mamba/RWKV/RetNet |
| --- | --- | --- | --- |
| Train parallelism | O(1) sequential depth, dense matmul | O(T) sequential (BPTT) | O(1) via parallel scan/chunked form |
| Inference memory | O(n), grows with context | O(1), fixed state | O(1), fixed state |
| Inference bottleneck | HBM bandwidth (reading KV cache) | negligible | negligible |
| Inference compute/token | O(n) (attends over full cache) | O(1) | O(1) |

So your statement holds. The one caveat: Transformer training being "friendly" is specifically because there's no *recurrent* dependency during training (masking substitutes for recurrence), not because attention is cheap — it's still O(n²), which is why prefill (not decode) is compute-bound and quadratic-cost for long prompts.

References:

- [The Mamba in the Llama: Distilling and Accelerating Hybrid Models](https://www.together.ai/blog/the-mamba-in-the-llama-distilling-and-accelerating-hybrid-models)
- [A Survey on LLM Acceleration based on KV Cache Management](https://arxiv.org/pdf/2412.19442)
- [KV Cache and KV Caching: The Hidden Bottleneck of LLM Inference](https://medium.com/@sulbha.jindal/kv-cache-and-kv-caching-a46acea80fe4)
- [Transformers vs Mamba vs Linear Attention: Who Wins Long Context?](https://machine-learning-made-simple.medium.com/transformers-vs-mamba-vs-linear-attention-who-wins-long-context-f1dc8ceb5ede)
