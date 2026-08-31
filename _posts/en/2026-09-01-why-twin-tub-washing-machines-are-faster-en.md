---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Twin-Tub Washing Machines Are Faster
translated: false
type: note
---

Question: Is the post’s argument about twin-tub/semi-automatic washing machines being much faster actually correct?

Answer: **Yes — the core engineering argument is basically right**, but there is one important distinction: a twin-tub machine is faster mainly because **you operate the process as a pipeline**, not because its washing mechanism is universally more efficient.

Think of it like this:

### 1. A fully automatic washer is mostly sequential

A typical cycle looks roughly like:

```text
fill
  ↓
wash
  ↓
drain
  ↓
rinse
  ↓
drain
  ↓
spin
  ↓
done
```

For the next batch:

```text
fill → wash → drain → rinse → drain → spin
```

The machine is doing a lot of **state transitions and waiting**.

---

### 2. A twin-tub machine lets YOU turn it into a pipeline

You can instead do:

```text
                 ┌── wash batch #2 ──┐
                 │                   │
wash batch #1 ──→ spin #1            │
                     ↓               │
                  finished           │
                                     ↓
                              spin #2
```

More concretely:

```text
WASH TUB                    SPIN TUB

batch A ────────→          spin A
batch B ────────→          spin B
batch C ────────→          spin C
batch D ────────→          spin D
```

While **A is spinning**, you're already **washing B**.

That's essentially the same idea as a production line.

If:

```text
wash = 6 min
spin = 3 min
```

then after the pipeline is filled, you can potentially process batches at roughly:

```text
one batch every ~6 minutes
```

rather than:

```text
6 min wash + 3 min spin = ~9 min/batch
```

assuming your manual handling and other operations don't become the bottleneck.

This is the really interesting part of the post.

---

### 3. The water reuse argument is also real

A fully automatic machine tends to think in terms of:

```text
one load
    ↓
wash
    ↓
drain
    ↓
rinse
    ↓
drain
    ↓
next load
    ↓
new water
```

A twin-tub machine gives you direct control:

```text
water
 ↓
wash A → spin A
 ↓
wash B → spin B
 ↓
wash C → spin C
```

You can keep relatively clean wash water for several loads, depending on how dirty the clothes are.

So the twin-tub gives you another optimization dimension:

```text
                   Fully automatic
                   ────────────────
                   machine optimizes
                   one load at a time

Twin tub
────────
human optimizes
the entire workload
```

That's actually a pretty deep distinction.

---

### 4. But I would challenge one statement

> "Fully automatic washing machines are inefficient, therefore they need 30–40 minutes."

That's **too broad**.

The long cycle isn't simply because the washing mechanism is inefficient.

Modern automatic machines deliberately spend time on things like:

* water filling/draining
* detergent mixing
* soaking
* multiple wash/rinse phases
* load sensing
* water-level control
* spin-speed ramping
* imbalance detection
* redistribution
* reducing vibration/noise
* fabric-care constraints

And modern front-loaders can actually have very good washing efficiency.

The problem is that the machine is solving a much more constrained optimization problem:

```text
                     Twin tub
                     ↓
          "Give me the controls.
           I'll manage the process."

Automatic washer
                     ↓
          "I'll make the process
           safe, unattended,
           repeatable and idiot-proof."
```

The latter necessarily has overhead.

---

### 5. The single-towel spin problem is a particularly good example

This is not really a "washing efficiency" problem.

It's a **control problem**.

Suppose the drum contains:

```text
        heavy towel
             ↓

    ┌─────────────────┐
    │                 │
    │       ███       │
    │                 │
    └─────────────────┘
```

If the towel stays concentrated in one region, the center of mass moves away from the rotation axis.

At high RPM:

$$
F = m r \omega^2
$$

Even a relatively small imbalance becomes a huge periodic force as angular velocity increases.

So the machine does something like:

```text
slow rotation
     ↓
detect imbalance
     ↓
stop
     ↓
reverse / tumble
     ↓
redistribute clothes
     ↓
try again
     ↓
detect imbalance
     ↓
...
```

That's why the machine sometimes appears to be "wasting time."

It's not stupid. It's protecting itself and your floor/wall.

A twin-tub spinner is much simpler. **You manually decide what goes in it**, so you can often distribute the load yourself.

---

### 6. The deeper insight is actually about **batch processing**

This is the part I think is worth stealing from the post as an engineer.

Suppose you have:

```text
N batches

washing time = W
spinning time = S
```

A sequential machine approximately has:

$$
T_{seq} \approx N(W+S)
$$

A two-stage pipeline can approach:

$$
T_{pipeline} \approx W+S+(N-1)\max(W,S)
$$

For example:

```text
W = 6 min
S = 3 min
N = 5
```

Sequential:

$$
5(6+3)=45\text{ min}
$$

Pipeline:

$$
6+3+4(6)=33\text{ min}
$$

And that's **before** considering water-fill/drain overhead.

So the twin-tub isn't magically making washing faster.

It's exploiting **parallelism**.

That's exactly the same concept as:

```text
CPU pipeline
GPU pipeline
data-processing pipeline
LLM inference pipeline
CI/CD pipeline
factory assembly line
```

Instead of:

```text
A: wash → spin
B: wash → spin
C: wash → spin
```

you do:

```text
A: wash → spin
B:        wash → spin
C:               wash → spin
```

Two independent machines/stages allow the work to overlap.

### Bottom line

The post is **directionally very correct**:

> Twin-tub washing machines can be surprisingly fast because they expose the pipeline to the human operator.

The tradeoff is basically:

| Twin tub                  | Fully automatic              |
| ------------------------- | ---------------------------- |
| Fast for multiple batches | Convenient                   |
| Manual labor              | Push button and leave        |
| Water can be reused       | Automatic water management   |
| Wash + spin can overlap   | Mostly sequential per load   |
| Simple mechanics          | Sophisticated control system |
| Cheap/simple              | More expensive               |
| Human handles imbalance   | Machine handles imbalance    |

So the interesting conclusion isn't really **"old washing machines are better."**

It's:

> **When the operator is willing to manage the pipeline, a simple two-stage system can outperform a sophisticated automated system on throughput.**

That's a very general engineering principle.
