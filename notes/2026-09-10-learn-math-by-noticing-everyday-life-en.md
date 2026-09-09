---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learn Math by Noticing Everyday Life
translated: false
type: note
---

Question: How can I learn math naturally by noticing mathematics in everyday life?

Answer: **Yes — that is one of the best ways to make math feel natural.** The key is to stop treating math as a collection of school topics and start treating it as a **language for describing patterns, quantities, uncertainty, and decisions**.

For someone with your engineering background, I'd use this loop:

> **Notice → estimate → model → calculate → check → generalize**

### 1. Start with estimation

Almost everything around you has numbers.

For example, you're buying a GPU for ¥1,000.

Instead of immediately calculating the price, ask:

* How much is that per GB of VRAM?
* How much is that per TFLOPS?
* How much electricity will it consume?
* If electricity costs ¥0.7/kWh, what does running it 8 hours/day cost?
* If the GPU lasts 3 years, what's the effective daily cost?

You naturally get:

$$
\text{cost/day}
=
\frac{\text{purchase price}}{\text{lifetime days}}
+
\text{electricity/day}
$$

That's already **arithmetic + ratios + linear models + economics**.

---

### 2. Turn ordinary observations into equations

Suppose you drive somewhere.

You know:

$$
d = vt
$$

Then start asking:

> "If I drive 60 km/h, how far can I get in 20 minutes?"

$$
d = 60\times\frac{20}{60}=20\text{ km}
$$

Then make it slightly more interesting:

> "Why does increasing speed from 60 → 80 km/h not reduce travel time by 25%?"

Now you're thinking about:

$$
t = \frac{d}{v}
$$

and nonlinear relationships.

This is much more powerful than memorizing "inverse proportionality."

---

### 3. Cooking is basically applied math

If a recipe serves 4 people and you need 7:

$$
\text{new quantity}
=
\text{original quantity}\times\frac74
$$

Then you encounter:

* ratios
* fractions
* proportions
* unit conversion
* temperature
* timing
* optimization

For example, if you're cooking multiple dishes simultaneously:

> "What's the schedule that minimizes total cooking time?"

That's an **optimization problem**.

---

### 4. Your AI work gives you an enormous mathematical playground

This is probably the most natural route for you.

When you see:

```python
y = x @ W
```

don't just think "PyTorch operation."

Think:

$$
y_i = \sum_j x_jW_{ji}
$$

Then ask:

> What is this operation geometrically?

Now you naturally discover **linear algebra**.

When you see:

```python
p = softmax(logits)
```

ask:

> Why exponentiate?

$$
p_i = \frac{e^{z_i}}{\sum_j e^{z_j}}
$$

Then ask:

> Why does cross entropy use \\(-\log p\\)?

You naturally arrive at **probability, logarithms, information theory and optimization**.

When training a model:

```text
loss → gradient → parameter update
```

you encounter:

$$
\theta_{t+1}
=
\theta_t-\eta\nabla_\theta L
$$

That's calculus becoming something you actually use.

---

### 5. Play the "what if?" game

This is probably the single best habit.

Take something you encounter and repeatedly change one variable.

For example:

> My model has 1B parameters.

Ask:

**What if it becomes 2B?**

Memory roughly doubles.

**What if precision changes BF16 → FP8?**

Memory per parameter roughly halves.

**What if batch size doubles?**

What happens to throughput? GPU memory? optimization?

**What if sequence length doubles?**

For vanilla attention:

$$
O(n^2)
$$

so attention computation can become roughly:

$$
2^2 = 4\times
$$

That's how mathematical intuition develops: **you manipulate relationships rather than memorize formulas.**

---

### 6. Keep a tiny "math notebook"

Not a school notebook.

Something like:

```text
2026-09-10

GPU:
4070 ≈ 200W

8h/day:
0.2 kW × 8h = 1.6 kWh/day

At ¥0.7/kWh:
≈ ¥1.12/day

One year:
≈ ¥409 electricity

Interesting:
electricity is ~40% of a ¥1000 GPU's annualized cost
if I amortize purchase over one year.
```

Then another day:

```text
LLM:

1B parameters × 2 bytes
≈ 2 GB weights

Training with Adam:
parameters
+ gradients
+ first moment
+ second moment

≈ several bytes/parameter

Why?
```

The notebook becomes a collection of **questions**, not formulas.

---

### 7. Don't deliberately "find math" all the time

There's an important distinction.

Don't walk around thinking:

> "I must study mathematics today."

Instead:

> **"Why does this work this way?"**

Then mathematics appears as the answer.

A useful progression is:

```text
real phenomenon
      ↓
question
      ↓
rough estimate
      ↓
equation
      ↓
mathematical concept
      ↓
formal theory
```

For example:

```text
Why does my LLM need so much VRAM?
        ↓
count parameters
        ↓
bytes/parameter
        ↓
memory model
        ↓
linear scaling
        ↓
quantization
        ↓
information/compression theory
```

That's a very natural way to learn.

### The deeper principle

**Math isn't primarily about numbers.**

It's about finding a compact structure underneath reality.

You see:

```text
money → ratios
motion → functions
uncertainty → probability
shapes → geometry
growth → exponentials
change → calculus
optimization → gradients
networks → graph theory
data → statistics
LLMs → linear algebra + probability + optimization
```

So yes: **look for math in daily life, but especially look for relationships.**

Whenever you catch yourself saying:

> "If X changes, what happens to Y?"

you are already doing mathematics.
