---
audio: false
generated: true
image: false
lang: en
layout: post
title: Start Simple, Narrow Problems First
translated: false
type: note
---

Question: Is the idea correct that "simple cooking → simple AI models; maybe 10M parameters is enough for code, elementary math, elementary Chinese"?

Answer:

Yes, the intuition is right: **start from simple, narrow problems and optimize for the actual task**. A giant model is not always necessary.

But the key distinction is:

> **Small model + narrow domain + enough high-quality data can be surprisingly strong.**
>
> **Small model + broad intelligence = usually fails.**

A 10M parameter model is roughly the scale of early language models. It can learn:

* character/word statistics
* simple grammar
* pattern matching
* small deterministic tasks

For example:

### 1. Elementary math

A 10M model can probably learn:

```
12 + 35 = 47
23 * 4 = 92
solve x + 3 = 8
```

if the training distribution is narrow.

But true reasoning:

```
A farmer has 17 sheep...
After selling some...
How many remain?
```

requires abstraction, not just memorization.

The model needs internal algorithms. Parameter count matters because the network is storing both:

* facts
* computation circuits

---

### 2. Code

This is actually where your idea is interesting.

A 10M-50M code model can be useful for:

* autocomplete
* syntax repair
* simple scripts
* generating boilerplate

Example:

Input:

```python
def fibonacci(n):
```

Output:

```python
    if n <= 1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)
```

Possible.

But:

```
Design a distributed database with Raft consensus
```

No.

Because large code models are not only storing syntax. They learn:

* software architecture
* API relationships
* debugging patterns
* long context dependencies

---

### 3. The cooking analogy is actually very good

A Michelin chef does not start by making 100 ingredients.

They master:

```
heat
salt
water
time
texture
```

The same applies to AI research:

Start with:

```
tiny transformer
↓
understand forward pass
↓
train on one domain
↓
measure failure
↓
scale only where needed
```

This is close to the philosophy behind many research approaches: understand the minimal mechanism first.

---

A practical experiment:

Train:

```
10M parameter Transformer

Dataset:
- 100M tokens Python only
- 100M tokens elementary math
- 100M tokens textbook Chinese
```

Then compare:

```
10M
50M
100M
1B
7B
```

You will probably see:

* 10M: learns surface patterns
* 50M: starts useful behavior
* 100M+: more robust
* 1B+: generalization improves significantly

The surprising part is that **for a very constrained product, the 10M model may already be enough**.

Examples:

* code formatter → tiny model
* SQL generator for one schema → tiny model
* children's math tutor → small model
* customer support for one product → small model

The mistake is assuming "AI = one giant brain".

The future is likely:

```
big foundation model
        +
many tiny specialized models
        +
agents/tools
```

Like cooking:

```
one huge kitchen is not always better

a sharp knife + simple ingredients + good process
can beat a complicated recipe
```

Your instinct of rebuilding from small models is actually a very good engineering experiment. The important thing is to define the task narrowly enough that the model's capacity matches the problem.
