---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT's Cross-Entropy Objective
translated: false
type: note
---

Question: Why does GPT use cross-entropy loss?

Answer:

Because GPT is fundamentally trained as a **next-token probability model**:

$$
P(x_t \mid x_1,\ldots,x_{t-1})
$$

At every position, GPT outputs a probability distribution over the vocabulary:

```text
context: "The capital of France is"

logits
   ↓
softmax
   ↓
P(token)
   ↓
[Paris: 0.82, London: 0.03, Berlin: 0.01, ...]
```

The training data gives us the actual next token, e.g.

```text
target = "Paris"
```

Cross-entropy asks:

> **How much probability did the model assign to the correct token?**

For one token:

$$
L=-\log P_\theta(x_t\mid x_{<t})
$$

So if GPT predicts:

```text
P(Paris) = 0.82
```

then

$$
L=-\log(0.82)\approx0.20
$$

Good prediction → small loss.

If:

```text
P(Paris) = 0.001
```

then

$$
L=-\log(0.001)\approx6.91
$$

Very bad prediction → huge loss.

### Why cross-entropy specifically?

There is a deeper reason.

Suppose the real data distribution is \\(p(x)\\), and GPT learns \\(q_\theta(x)\\).

The expected cross-entropy is:

$$
H(p,q)=-\mathbb E_{x\sim p}[\log q_\theta(x)]
$$

And:

$$
H(p,q)=H(p)+D_{KL}(p\|q)
$$

Since \\(H(p)\\) doesn't depend on the model:

$$
\arg\min_\theta H(p,q_\theta)
=
\arg\min_\theta D_{KL}(p\|q_\theta)
$$

So minimizing cross-entropy is essentially asking GPT to make its predicted distribution \\(q_\theta\\) approach the distribution that generated the training text.

---

### Why not MSE?

Imagine the target is:

```text
Paris = 1
London = 0
Berlin = 0
...
```

You *could* use MSE:

$$
\sum_i (q_i-y_i)^2
$$

But classification is naturally a **probability distribution**, and cross-entropy has much better behavior.

For softmax + cross-entropy, there's a particularly beautiful gradient.

Let:

$$
z_i = \text{logit}_i
$$

$$
p_i=\operatorname{softmax}(z)_i
$$

and target \\(y_i\\) is one-hot.

Then:

$$
L=-\sum_i y_i\log p_i
$$

The derivative is simply:

$$
\boxed{\frac{\partial L}{\partial z_i}=p_i-y_i}
$$

That's extremely convenient.

For example:

```text
prediction: [0.1, 0.7, 0.2]
target:     [0,   1,   0]

gradient:   [0.1, -0.3, 0.2]
```

The model gets a direct signal:

* probability too high → push it down
* probability too low → push it up
* correct token → gradient reflects how far its probability is from 1

---

### And this is exactly what GPT does

For a sequence:

```text
The cat sat on the mat
```

GPT creates training examples:

```text
"The"              → "cat"
"The cat"           → "sat"
"The cat sat"       → "on"
"The cat sat on"    → "the"
"The cat sat on the" → "mat"
```

Then:

$$
L=
-\frac1T
\sum_{t=1}^{T}
\log P_\theta(x_t|x_{<t})
$$

In code, conceptually:

```python
logits = model(tokens[:, :-1])

loss = F.cross_entropy(
    logits.reshape(-1, vocab_size),
    tokens[:, 1:].reshape(-1),
)
```

Then:

```python
loss.backward()
optimizer.step()
```

That's the core GPT training loop.

**Cross-entropy isn't an arbitrary choice.** GPT's job is to estimate a categorical probability distribution for the next token, and negative log-likelihood / cross-entropy is the natural maximum-likelihood objective for learning that distribution.