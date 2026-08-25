---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache Optimization in LLM Inference
translated: false
type: note
---

Question: How does KV cache work in `nano-vLLM` and similar minimal LLM inference engines?

Answer: The key idea is:

> **KV cache turns autoregressive decoding from “recompute attention over the whole prefix every token” into “compute K/V once, append them, and only compute Q for the new token.”**

For a transformer layer, given tokens (x_1,\ldots,x_t):

[
Q = XW_Q,\quad K=XW_K,\quad V=XW_V
]

and causal attention is:

[
\text{Attention}(Q,K,V)
=======================

\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
]

During generation, suppose we've already generated 1000 tokens and now want token 1001.

### Without KV cache

You effectively do:

```text
tokens[0:1001]
       ↓
embedding
       ↓
Q, K, V for all 1001 tokens
       ↓
attention
       ↓
next token
```

Then for token 1002:

```text
tokens[0:1002]
       ↓
recompute Q,K,V for all 1002
```

So you're repeatedly recomputing the old K/V.

### With KV cache

At token 1001:

```text
old KV cache:
K[0:1000], V[0:1000]

new token:
x1001
  ↓
Q1001, K1001, V1001
  ↓
append K1001,V1001
  ↓
attention(Q1001, K[0:1001], V[0:1001])
```

At token 1002:

```text
Q1002
   │
   ├── K cache: K0 ... K1002
   └── V cache: V0 ... V1002
             ↓
          attention
```

You only calculate **one new Q/K/V per layer**.

---

## 1. What nano-vLLM is actually caching

Conceptually, every transformer layer has:

```python
k_cache[layer][position]
v_cache[layer][position]
```

For a normal multi-head attention model:

```text
K cache
[layer]
   └── [sequence position]
          └── [KV head]
                 └── [head dimension]

V cache
[layer]
   └── [sequence position]
          └── [KV head]
                 └── [head dimension]
```

For example:

```python
k_cache.shape
# [num_layers, max_seq_len, num_kv_heads, head_dim]

v_cache.shape
# [num_layers, max_seq_len, num_kv_heads, head_dim]
```

The exact layout in `nano-vLLM` can differ because layout is heavily optimized for CUDA kernels, but this is the conceptual model.

---

# 2. The important trick: only the newest token needs Q

Suppose:

```text
prompt = "The capital of France is"
```

The prompt phase is called **prefill**.

You process all tokens simultaneously:

```text
X
│
├── Q
├── K ───────────────→ KV cache
└── V ───────────────→ KV cache
```

For:

```text
"The capital of France is"
```

you obtain:

```text
K0 K1 K2 K3 K4
V0 V1 V2 V3 V4
```

and save them.

Then suppose the model predicts:

```text
Paris
```

Now you have:

```text
K0 K1 K2 K3 K4 K5
V0 V1 V2 V3 V4 V5
```

For the next generation step, you don't need to calculate:

```text
Q0 Q1 Q2 Q3 Q4 Q5
K0 K1 K2 K3 K4 K5
V0 V1 V2 V3 V4 V5
```

You only calculate:

```text
Q6 K6 V6
```

Then:

```text
Q6
 │
 ├────────────── K0
 ├────────────── K1
 ├────────────── K2
 ├────────────── K3
 ├────────────── K4
 ├────────────── K5
 └────────────── K6
                  ↓
              softmax
                  ↓
             V0...V6
```

That's the fundamental KV-cache algorithm.

---

# 3. Why this matters so much

Without cache, generation has approximately:

[
O(T^2)
]

work over a sequence of length (T), because every new token repeatedly processes the old prefix.

With KV cache, generation has roughly:

[
O(T)
]

incremental projection work plus the attention scan:

[
q_t K_{0:t}^T
]

which is (O(t)) for each generated token.

So total decoding attention work is still:

[
\sum_{t=1}^{T} O(t) = O(T^2)
]

but **the enormous repeated K/V projection and transformer computation disappears**.

This distinction is important.

KV cache does **not** magically make attention itself linear in sequence length. It makes autoregressive decoding much cheaper by avoiding recomputation of previous states.

---

# 4. nano-vLLM's more interesting problem: batching requests

This is where `vLLM`-style systems become much more interesting than a simple Hugging Face implementation.

Imagine:

```text
Request A:
"The cat sat on"

Request B:
"Once upon a time"

Request C:
"Explain transformers"
```

Their lengths differ.

You don't want:

```text
GPU memory
┌────────────────────────────┐
│ Request A KV               │
│ Request B KV               │
│ Request C KV               │
│ huge contiguous tensors    │
└────────────────────────────┘
```

because sequences constantly grow.

Instead, modern engines use **paged/block KV cache**.

---

# 5. Paged KV cache

Think virtual memory.

Instead of:

```text
sequence
0 1 2 3 4 5 6 7 8 9 ...
```

requiring one giant contiguous allocation, divide it into blocks:

```text
block 0: tokens  0-15
block 1: tokens 16-31
block 2: tokens 32-47
...
```

Then maintain a mapping:

```text
Request A
logical block 0 → physical block 17
logical block 1 → physical block 42
logical block 2 → physical block  3

Request B
logical block 0 → physical block  8
logical block 1 → physical block 19
```

So GPU memory looks more like:

```text
Physical KV memory:

[block 0]
[block 1]
[block 2]
...
[block 17] ← A's logical block 0
...
[block 42] ← A's logical block 1
...
```

The sequence doesn't care that its blocks aren't physically adjacent.

This is basically **virtual memory for KV cache**.

---

# 6. Why this is called PagedAttention

The original vLLM idea was essentially:

```text
virtual token positions
        ↓
logical KV blocks
        ↓
block table
        ↓
physical KV blocks
        ↓
GPU memory
```

For example:

```python
block_table = {
    request_A: [17, 42, 3],
    request_B: [8, 19],
}
```

The attention kernel receives the block mapping and fetches the appropriate K/V blocks.

This solves several problems simultaneously:

* variable sequence lengths
* dynamic sequence growth
* GPU memory fragmentation
* continuous batching
* KV-cache sharing
* prefix caching

---

# 7. GQA makes KV cache much smaller

This is another important detail for modern models.

Suppose:

```text
num_attention_heads = 32
num_kv_heads       = 8
head_dim            = 128
```

With normal MHA:

```text
K: 32 heads
V: 32 heads
```

With GQA:

```text
Q: 32 heads
K:  8 heads
V:  8 heads
```

Each KV head is shared by 4 Q heads:

```text
Q0 Q1 Q2 Q3 → KV0
Q4 Q5 Q6 Q7 → KV1
...
```

So KV memory is reduced by:

[
\frac{32}{8}=4\times
]

This is a **huge deal** for inference.

For a model with:

```text
L = 32 layers
H_kv = 8
D = 128
context = 32K
dtype = FP16
```

KV memory for one sequence is approximately:

[
2 \times L \times H_{kv} \times D \times T \times 2\text{ bytes}
]

which gives:

[
2 \times 32 \times 8 \times 128 \times 32768 \times 2
\approx 4\text{ GiB}
]

So a single 32K sequence can consume **~4 GB just for KV cache**.

That's why inference engines obsess over KV memory.

---

# 8. Prefill vs decode

This distinction is essential when reading nano-vLLM code.

### Prefill

You have:

```text
prompt = 1000 tokens
```

Run:

```python
Q, K, V = model(prompt)
```

and populate:

```text
KV cache:
[0 ... 999]
```

This is highly parallel and compute-heavy.

### Decode

Now generate one token:

```text
1000 → 1001
1001 → 1002
1002 → 1003
...
```

Each iteration essentially does:

```python
q, k, v = model(new_token)

cache.append(k, v)

logits = attention(
    q,
    cache.K,
    cache.V,
)
```

The batch dimension may contain many requests:

```text
request A → token
request B → token
request C → token
request D → token
```

This is where continuous batching becomes powerful.

---

# 9. The minimal implementation

A toy KV cache can literally be:

```python
class KVCache:
    def __init__(self, max_seq_len, n_kv_heads, head_dim):
        self.k = torch.empty(
            max_seq_len,
            n_kv_heads,
            head_dim,
            device="cuda",
        )

        self.v = torch.empty(
            max_seq_len,
            n_kv_heads,
            head_dim,
            device="cuda",
        )

    def update(self, pos, k, v):
        self.k[pos] = k
        self.v[pos] = v

    def get(self, end):
        return self.k[:end], self.v[:end]
```

Then decoding:

```python
for pos in range(prompt_len, max_seq_len):

    q, k, v = model(
        input_ids[:, pos:pos+1]
    )

    cache.update(pos, k, v)

    K, V = cache.get(pos + 1)

    y = attention(q, K, V)

    next_token = sample(y)
```

That's basically the conceptual core.

The real `nano-vLLM` implementation adds:

```text
block allocation
block tables
batched requests
CUDA kernels
RoPE
GQA
memory management
continuous batching
sampling
```

but the fundamental state machine remains this.

---

# 10. The really important mental model

Think of the KV cache as **persistent intermediate activations across autoregressive time**.

Normally:

```text
token t
   ↓
transformer
   ↓
K,V
   ↓
discard
```

KV caching changes it to:

```text
token t
   ↓
transformer
   ↓
K,V
   ↓
GPU memory
   ↓
used by every future token
```

So the model's effective state becomes:

```text
Transformer weights
        +
KV cache
        ↓
next-token distribution
```

The **weights are static**, while the **KV cache is the dynamic state of each active sequence**.

That's also why serving LLMs is fundamentally different from serving an ordinary stateless neural network.

---

## If you read nano-vLLM source

I'd trace these four things in this order:

```text
1. Request / Scheduler
       ↓
2. KV-cache block allocation
       ↓
3. Model.forward()
       ↓
4. Attention kernel
```

Especially look for the path:

```text
request
  → block_table
  → slot_mapping
  → k_cache / v_cache
  → attention()
```

Once you understand **`block_table` + `slot_mapping` + K/V tensor layout**, nano-vLLM's KV-cache implementation becomes much less mysterious. The rest is mostly making this simple algorithm GPU-efficient.
