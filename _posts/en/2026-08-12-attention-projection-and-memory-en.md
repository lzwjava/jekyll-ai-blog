---
audio: false
generated: true
image: false
lang: en
layout: post
title: Attention Projection and Memory
translated: false
type: note
---

Question: Is the statement "Q/K projection is information filtering, and KV is self-association mathematically" correct from a first-principles view?

Answer:

Your friend's intuition is **mostly correct**, but some terminology needs refinement.

The key is to view attention as a sequence of linear projections:

[
x \in R^{d_{model}}
]

A transformer takes the hidden state (x) and projects it:

[
q=xW_q
]

[
k=xW_k
]

[
v=xW_v
]

where:

* (W_q): query projection
* (W_k): key projection
* (W_v): value projection

Usually:

[
W_q,W_k,W_v \in R^{d_{model}\times d_{head}}
]

with:

[
d_{head}<d_{model}
]

Example:

```
hidden_size = 4096
num_heads = 32

head_dim = 4096 / 32 = 128
```

So each head does:

[
4096 \rightarrow 128
]

This is a dimensionality reduction.

genui{"linear_algebra_optimization":{"type_id":"VECTOR_PROJECTION","locale_override":"en-US"}}

---

### 1. Is Q projection "filtering information"?

Yes.

Suppose:

[
q=xW_q
]

The matrix (W_q) maps a 4096-dimensional hidden state into a 128-dimensional subspace.

The original information space:

[
R^{4096}
]

becomes:

[
R^{128}
]

This is a compression.

If (W_q) is not full rank:

[
rank(W_q)<4096
]

then there exist many different hidden states:

[
x_1 \neq x_2
]

but:

[
x_1W_q=x_2W_q
]

Meaning:

after projection, the model cannot distinguish them.

The lost information is in the null space:

[
(x_1-x_2)W_q=0
]

So yes:

> Q/K projection is not a reversible transformation. It extracts features useful for attention and discards other information.

---

### 2. Why pseudo-inverse cannot recover x?

Your friend said:

[
qW_q^+
]

cannot recover (x).

Correct.

The pseudo-inverse gives the best least-square reconstruction:

[
\hat{x}=qW_q^+
]

but:

[
\hat{x}\neq x
]

unless (W_q) preserves all dimensions.

Example:

```
x:
[cat, color, position, grammar, emotion, ... 4096 features]

Wq:

keeps:
    "is this token relevant to my query?"

drops:
    many semantic details
```

After projection:

```
q:
[relevance features only]
```

You cannot reconstruct the original hidden state.

---

### 3. Is KV "self-association"?

This part needs nuance.

Attention:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

The first part:

[
QK^T
]

computes similarity.

A query asks:

> "Which tokens contain information relevant to me?"

Keys represent:

> "What kind of information does this token provide?"

Values represent:

> "Actual content to retrieve."

So:

```
Q:
what I need

K:
address/index

V:
information
```

A database analogy:

```
K = index
V = value

Q = search query
```

---

### 4. Why "self-association"?

From the network perspective, attention is usually called:

**hetero-associative memory**

because:

[
Q \rightarrow K,V
]

The query is matched against another representation.

Classic associative memory:

```
input pattern → stored pattern
```

For transformer:

```
query → retrieve value
```

So mathematically:

[
QK^T
]

is a lookup mechanism.

But your friend's intuition:

> KV comes from the same hidden variable x, so it is self-association

is also reasonable.

Because:

For every token:

[
x_i
\rightarrow
(k_i,v_i)
]

The memory is created from the same sequence itself.

Example:

Sentence:

```
The Eiffel Tower is in Paris.
```

During generation:

The model stores:

```
K:
"Eiffel Tower"

V:
"Paris"
```

Later:

```
Q:
Where is Eiffel Tower?
```

retrieves:

```
V:
Paris
```

The memory is built from itself.

So:

* **architecture view:** hetero-associative retrieval
* **data origin view:** self-generated associative memory

Both are valid.

---

### 5. "KV projection matrix is usually not full rank"

Correct.

For example:

[
W_v:
4096 \rightarrow 128
]

The maximum rank:

[
rank(W_v)\le128
]

So it cannot encode all 4096 dimensions.

The model learns:

"Which 128-dimensional latent features are useful for future retrieval?"

Not:

"store the whole hidden state."

This is exactly why architectures like:

* Multi-Query Attention (MQA)
* Grouped Query Attention (GQA)
* Multi-head Latent Attention (MLA)

try to optimize KV representation.

Especially MLA (DeepSeek):

Instead of storing:

[
K,V
]

directly:

it compresses:

[
KV \rightarrow latent
]

and reconstructs useful parts later.

---

A more precise statement would be:

> Q/K/V projections are learned low-dimensional feature extractors. They discard information intentionally and preserve only features useful for attention. KV acts like a learned associative memory: keys provide addressing, values provide retrieved content. It is self-generated from previous hidden states but functions as hetero-associative retrieval during attention.

That is the mathematically accurate version.
