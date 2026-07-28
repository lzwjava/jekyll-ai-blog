---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evolution of LLM Architecture Explained
translated: false
type: note
---

Question: What does the attached “22580: From GPT-2 to Kimi3, Explained” article mean?

Answer:

This is a technical explanation of **how modern LLM architectures evolved from GPT-2 (2019) to Kimi K3 (2026)**. The main point is:

> Modern LLM progress is not only "make the model bigger"; it is about improving **memory, retrieval, efficiency, and capacity management**.

The author starts with a comparison:

> "At 2.8 trillion parameters, one KimiK3 model contains roughly as many parameters as 22,580 GPT-2 models."

Meaning:

* GPT-2:

  * 124M parameters
  * 12 transformer layers
  * 12 attention heads
  * 768 hidden dimension
* Kimi K3:

  * ~2.8T parameters

But the interesting part is not just scale.

---

## 1. GPT-2: pure Transformer

GPT-2 is a normal decoder-only Transformer:

```
tokens
  |
embedding
  |
Transformer blocks
  |
linear head
  |
next token prediction
```

Each block:

```
x
 |
LayerNorm
 |
Attention
 |
+
 |
LayerNorm
 |
MLP
 |
+
 |
output
```

The code in the article:

```python
x = x + self.attn(self.ln_1(x))
x = x + self.mlp(self.ln_2(x))
```

is the core GPT architecture.

---

## 2. Problem: Attention memory grows with context length

Normal attention:

```
Q × K^T
```

For sequence length N:

```
attention matrix:

N × N
```

Example:

10,000 tokens:

```
10000 × 10000
= 100 million attention scores
```

The article explains that without KV cache, generation recomputes old tokens repeatedly.

KV cache solves this:

During generation:

```
old tokens
   |
store K,V
   |
new token only computes new Q
```

But:

```
KV cache size ∝ sequence length
```

Long context becomes a memory bandwidth problem.

---

# 3. Linear Attention: replace growing memory

Traditional attention:

```
Attention(Q,K,V)

= softmax(QKᵀ)V
```

The expensive part:

```
QKᵀ

N × N
```

Linear attention changes the order:

Instead of:

```
(QKᵀ)V
```

do:

```
Q(KᵀV)
```

Now:

```
KᵀV
```

becomes a fixed-size state.

Memory:

```
Transformer attention:
O(N)

KV cache grows forever


Linear attention:
O(1)

fixed memory
```

The article explains:

> Linear attention folds growing K/V vectors into a fixed D×D state.

---

# 4. The problem with Linear Attention

The problem:

A fixed memory has limited capacity.

Imagine:

```
memory = 1000 slots

write:
cat = animal
dog = animal
...

after millions facts:

cat?
dog?
```

Information overlaps.

The article calls this:

> "information interference"

Basically:

```
old knowledge
+
new knowledge
=
memory collision
```

---

# 5. DeltaNet: learn what to overwrite

DeltaNet introduces smarter memory updates.

Instead of:

```
memory += new information
```

it does:

```
old_value = memory[key]

error = new_value - old_value

memory += error
```

Like gradient descent.

Example:

Before:

```
memory:
Apple -> fruit
```

New information:

```
Apple -> company
```

Delta update:

```
remove old association
write new association
```

The article:

> "Old information is removed and new information is written in its place."

---

# 6. Gated DeltaNet: add forgetting

Human memory forgets.

Pure DeltaNet:

```
update specific memories
```

but cannot globally forget.

Gated version:

```
memory = alpha * old_memory + new_information
```

where:

```
alpha = 0

forget everything

alpha = 1

keep memory
```

The article connects this idea with Mamba-style state decay.

---

# 7. Kimi Linear: hybrid architecture

Kimi Linear combines:

```
DeltaNet
+
MLA attention
+
MoE
```

Meaning:

### DeltaNet

cheap long-term memory:

```
constant memory
```

### MLA (Multi-head Latent Attention)

precise retrieval:

```
full attention when needed
```

### MoE

more parameters without activating everything.

Example:

```
898 experts

token chooses 16 experts
```

The article states:

> KimiK3 has 898 experts; 16 are selected per token.

So:

```
Total model:

898 experts

but each token only uses:

16 experts
```

This saves compute.

---

# 8. Kimi K3 architecture intuition

A simplified view:

```
Input

 |
 |
Delta Attention
(fast memory)

 |
MoE
(specialized knowledge)

 |
Delta Attention

 |
MLA
(expensive retrieval)

 |
MoE

 |
Output
```

The model has two types of memory:

### Fast memory

DeltaNet:

```
cheap
constant size
long context
```

### Exact memory

MLA:

```
expensive
accurate retrieval
```

Similar to a computer:

```
RAM + SSD

not one storage system
```

---

# The big idea

The evolution:

```
GPT-2
 |
 | scale parameters
 v
GPT-3
 |
 | better training
 v
GPT-4
 |
 | efficient memory
 v
Linear Attention
 |
 | better memory updates
 v
DeltaNet
 |
 | hybrid memory
 v
Kimi Linear
 |
 | MoE + MLA + scaling
 v
Kimi K3
```

The author’s conclusion:

> The important change is not scale alone. Each architecture changes what the model stores, how it updates memory, or how it retrieves information.

For someone who trained GPT-2 style models with nanoGPT: the key takeaway is that **future LLMs are moving from "huge Transformer with bigger KV cache" toward "neural memory systems"**.

GPT-2:

```
attention = read everything every time
```

Kimi K3:

```
fast learned memory
+
selective retrieval
+
sparse experts
```

That is the architectural shift.
