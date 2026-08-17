---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RoPE: Separate Rotations Yield Relative Positions"
translated: false
type: note
---

Let's go deeper. The confusing part is **why rotating Q and K separately makes the attention score become relative position**.

This is the core mathematical trick of RoPE.

---

# 1. Start from normal attention

Transformer attention:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

The important part:

[
QK^T
]

is just a dot product.

Example:

```
Query token:

Q = [0.8, 0.2]


Key token:

K = [0.5, 0.9]


score:

Q · K

=0.8*0.5 + 0.2*0.9

=0.58
```

The larger the dot product, the more attention.

---

# 2. The problem

Suppose:

```
"The cat eats fish"
```

Positions:

```
The     cat     eats     fish

0       1        2        3
```

When `eats` attends to `cat`:

```
query position:

m = 2


key position:

n = 1
```

The model should know:

```
cat is one token before eats

distance = -1
```

But normal attention only sees:

```
Q vector
K vector
```

No position.

---

# 3. Idea: encode position into the vector itself

Instead of:

```
Q

K
```

we create:

```
position 2:

Q rotated by angle 2θ


position 1:

K rotated by angle 1θ
```

So:

[
Q'=R(2\theta)Q
]

[
K'=R(1\theta)K
]

Then attention becomes:

[
Q'^TK'
]

or:

[
(R(2\theta)Q)^T(R(\theta)K)
]

---

# 4. Let's understand rotation

A 2D vector:

```
        y
        |
        |
        *
       /
      /
-----*---------- x
```

Suppose:

[
q=[1,0]
]

It points right.

Angle:

```
0 degrees
```

---

Rotate 90 degrees:

[
R(90^\circ)
]

Now:

```
        *
        |
        |
        |
--------+--------


```

Vector becomes:

[
[0,1]
]

---

Rotation matrix:

[
R(\theta)=
\begin{bmatrix}
cos\theta&-sin\theta\
sin\theta&cos\theta
\end{bmatrix}
]

Multiply:

[
R(\theta)
\begin{bmatrix}
x\
y
\end{bmatrix}
]

Example:

[
\theta=90^\circ
]

because:

[
cos90=0
]

[
sin90=1
]

we get:

[
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

---

# 5. The magic property

Now the important part.

Assume:

Query position:

[
m
]

Key position:

[
n
]

RoPE does:

[
Q'=R(m\theta)q
]

[
K'=R(n\theta)k
]

Attention:

[
Q'^TK'
]

Substitute:

[
(R(m\theta)q)^T(R(n\theta)k)
]

Transpose rule:

[
(AB)^T=B^TA^T
]

so:

[
q^T R(m\theta)^T R(n\theta) k
]

For rotation matrices:

[
R(\theta)^T=R(-\theta)
]

Therefore:

[
q^T R(-m\theta)R(n\theta)k
]

Rotation composition:

[
R(a)R(b)=R(a+b)
]

therefore:

[
q^T R((n-m)\theta)k
]

That is the magic.

---

# 6. What disappeared?

Before:

[
R(m\theta),R(n\theta)
]

We had:

```
query position = m

key position = n
```

Two absolute positions.

After simplification:

[
R((n-m)\theta)
]

Only:

```
distance = n-m
```

remains.

---

Example:

Sentence:

```
I love machine learning
```

positions:

```
I       love       machine      learning

0        1            2            3
```

Query:

```
learning

m=3
```

Key:

```
machine

n=2
```

Relative distance:

[
n-m=2-3=-1
]

RoPE attention sees:

```
-1
```

not:

```
position 3
position 2
```

---

# 7. Why use rotation instead of adding vectors?

Compare:

## Old positional embedding

```
token vector

[0.3,0.7]


+

position vector

[0.1,0.2]


=

[0.4,0.9]
```

Position and meaning are mixed.

---

## RoPE

Original:

```
meaning vector:

direction in space
```

Position:

```
rotate the direction
```

Example:

```
same word:

"cat"
```

Different positions:

```
cat at position 1:

   /

cat at position 100:

       \
```

Same semantic vector, different angle.

---

# 8. Extending to 4096 dimensions

A real LLM vector:

```
hidden state:

[
x0,
x1,
x2,
x3,
...
x4095
]
```

RoPE groups dimensions:

```
(x0,x1)

(x2,x3)

(x4,x5)

...

(x4094,x4095)
```

Each pair is a 2D vector.

Example:

```
pair 0:

[x0,x1]

rotate by θ0


pair 1:

[x2,x3]

rotate by θ1


pair 2:

[x4,x5]

rotate by θ2
```

Different frequencies:

```
pair 0:
fast rotation


pair 100:
slow rotation
```

Like Fourier transform.

---

# 9. Why multiple frequencies?

Imagine a clock.

Fast clock:

```
0 1 2 3 4 5 ...
```

Useful for nearby positions.

Slow clock:

```
0 ........ 100 ........ 200
```

Useful for long distance.

LLM needs both:

Example:

```
"The cat sat on the mat"

cat -> sat

distance 1


"The cat ......... animal"

cat -> animal

distance 20
```

Different dimensions capture different scales.

---

# 10. Complete mental model

Think of RoPE like this:

```
Token meaning
      |
      v
vector direction


Position
      |
      v
rotation angle


Q:
meaning + position rotation


K:
meaning + position rotation


attention:

compare two rotated vectors


angle difference:

n-m


therefore:

relative position
```

The entire RoPE paper is basically this one mathematical observation:

[
\boxed{
(R_mq)^T(R_nk)
==============

q^TR_{n-m}k
}
]

A very small change to attention, but it solved the positional encoding problem for modern long-context LLMs.
