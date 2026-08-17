---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RoFormer: Rotary Position Embedding Explained"
translated: false
type: note
---

## Question: Explain arXiv:2104.09864v5 — **RoFormer: Enhanced Transformer with Rotary Position Embedding (RoPE)**

Answer:

This paper introduces **RoPE (Rotary Position Embedding)**, the positional encoding method used by many modern LLMs:

* LLaMA / LLaMA 2 / LLaMA 3
* Qwen
* Mistral
* DeepSeek
* GPT-NeoX style models

The core idea:

> Instead of adding position embeddings to token embeddings, rotate the Query and Key vectors according to their positions, so attention naturally learns relative positions.

Paper: ([Star Oceans][1])

---

# 1. Why do Transformers need position information?

Self-attention itself has no concept of order.

Example:

```
"The cat eats fish"
"The fish eats cat"
```

The tokens are the same set:

```
cat
eats
fish
```

Attention only sees vectors:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

There is no "token 1", "token 2".

So we need position information.

---

# 2. Original Transformer positional embedding

The original Transformer adds position vectors:

[
x_i = token_i + position_i
]

Example:

```
token embedding:

cat  ---> [0.2,0.5,0.1...]

position:

pos=3 ---> [0.01,0.03,0.02...]

sum:

[0.21,0.53,0.12]
```

This works.

But problems:

1. Position is mixed into content.

2. Maximum length is fixed.

For example:

Training:

```
context length = 2048
```

The model learns:

```
position 0 ... 2047
```

At inference:

```
position 4096
```

There is no learned embedding.

---

# 3. Relative position idea

Humans care about relative distance.

Example:

```
The cat sat on the mat
        ^
        |
        current token
```

The relationship:

```
cat -> sat

distance = +1
```

is more important than:

```
cat position = 2
```

So we want attention to know:

[
relative\ distance = m-n
]

where:

* m = query position
* n = key position

---

# 4. RoPE key idea

RoPE says:

Don't add position.

Rotate vectors.

Before:

```
Q
|
|
attention
|
K
```

After RoPE:

```
Q ---> rotate(position m) ---> Q'

K ---> rotate(position n) ---> K'


attention:

Q'K'^T
```

The magic property:

[
(R_m q)^T(R_n k)
]

becomes:

[
q^T R_{n-m} k
]

Meaning:

The dot product only depends on:

[
n-m
]

the relative distance.

This is the whole paper.

---

# 5. Intuition: 2D rotation

Imagine a vector:

```
        y
        |
        |
        *
       /
      /
-----*---------- x
```

Rotate it:

position 0:

```
angle = 0°
```

position 1:

```
angle = θ
```

position 2:

```
angle = 2θ
```

position n:

```
angle = nθ
```

So position becomes angle.

---

Mathematically:

A 2D rotation:

[
R(\theta)=
\begin{bmatrix}
cos\theta & -sin\theta\
sin\theta & cos\theta
\end{bmatrix}
]

For token at position m:

[
q_m=R(m\theta)q
]

For token at position n:

[
k_n=R(n\theta)k
]

Attention:

[
q_m^Tk_n
]

becomes:

[
q^TR((n-m)\theta)k
]

The absolute positions disappear.

Only distance remains.

---

# 6. Extending to high dimensions

LLM hidden size:

```
4096
```

Not 2.

RoPE splits dimensions into pairs:

Example:

```
hidden vector:

[x0,x1,x2,x3,x4,x5,...]

pairs:

(x0,x1)
(x2,x3)
(x4,x5)
...
```

Each pair rotates with different frequency.

Like:

```
dimension pair 0:

fast rotation

dimension pair 1:

slower rotation

dimension pair 2:

even slower
```

The frequencies:

[
\theta_i=10000^{-2i/d}
]

So:

low dimensions:

```
high frequency
(short distance patterns)
```

high dimensions:

```
low frequency
(long distance patterns)
```

Similar to Fourier features.

---

# 7. PyTorch implementation

A simplified RoPE:

```python
import torch

def rotate_half(x):
    x1 = x[..., :x.shape[-1]//2]
    x2 = x[..., x.shape[-1]//2:]

    return torch.cat(
        (-x2, x1),
        dim=-1
    )


def apply_rope(x, cos, sin):
    return (
        x * cos +
        rotate_half(x) * sin
    )
```

During attention:

```python
q = apply_rope(q, cos, sin)
k = apply_rope(k, cos, sin)

attn = q @ k.transpose(-2,-1)
```

That is basically what LLaMA does.

---

# 8. Why RoPE works well for LLMs

## Property 1: Relative distance

Attention naturally knows:

```
token A is 3 positions away
```

instead of:

```
token A is position 3812
```

---

## Property 2: No learned position table

Old:

```
nn.Embedding(max_position, dim)

2048 positions
```

RoPE:

```
calculate sin/cos
```

You can extend length.

---

## Property 3: Long-distance decay

The paper shows:

As distance increases:

```
attention score decreases
```

This matches language.

Nearby words:

```
"The cat sat"
       ^
       important
```

Far words:

```
"The cat sat ................. yesterday"
```

less related.

---

# 9. Why modern LLMs modify RoPE

Original RoPE:

```
context 2k
```

Modern models:

```
32k
128k
1M
```

Problems appear:

high positions rotate too much.

Example:

```
position 0

angle = 0


position 100000

angle = huge
```

Solutions:

## NTK scaling

Used by many models.

Idea:

change frequencies:

[
\theta_i
]

so the same rotations cover longer context.

---

## YaRN

Improves long-context extrapolation.

---

## LongRoPE

Extends RoPE to millions of tokens.

---

# 10. Connection to Fourier transform

A useful mental model:

RoPE is a learned-friendly Fourier feature.

Fourier:

```
signal
 |
different frequencies
 |
encode position
```

RoPE:

```
token vector
 |
rotate with frequencies
 |
encode position
```

Different dimensions represent different "position clocks".

---

# 11. Why this paper became extremely important

The paper itself was about RoFormer, but the bigger impact was:

```
RoPE
 |
 +--> LLaMA
 |
 +--> Qwen
 |
 +--> Mistral
 |
 +--> DeepSeek
 |
 +--> almost every open LLM today
```

It became the default positional encoding for decoder-only LLMs. ([Science Stack][2])

---

A good way to remember:

```
Absolute PE:
    token + position

Relative PE:
    explicitly calculate distance

RoPE:
    rotate Q,K
    dot product automatically becomes relative distance
```

The mathematical trick is:

[
\boxed{
(R_m q)^T(R_n k)=q^TR_{n-m}k
}
]

That single equation is why RoPE dominates modern LLM architectures. ([Science Stack][3])

References:

* RoFormer: Enhanced Transformer with Rotary Position Embedding ([Star Oceans][1])
* RoFormer summary and properties ([Science Stack][2])

[1]: https://staroceans.org.s3.amazonaws.com/stable-diffusion/2104.09864v5.pdf?utm_source=chatgpt.com "ROFORMER: ENHANCED TRANSFORMER WITH ROTARY"
[2]: https://www.sciencestack.ai/paper/2104.09864v5?utm_source=chatgpt.com "RoFormer: Enhanced Transformer with Rotary Position Embedding (arXiv:2104.09864v5) - ScienceStack"
[3]: https://www.sciencestack.ai/paper/2104.09864?utm_source=chatgpt.com "RoFormer: Enhanced Transformer with Rotary Position Embedding (arXiv:2104.09864v5) - ScienceStack"
