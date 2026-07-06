---
audio: false
generated: true
image: false
lang: en
layout: post
title: TALOS-V2 FPGA Transformer Accelerator
translated: false
type: note
---

Question: Intro to the repo [https://github.com/Luthiraa/TALOS-V2](https://github.com/Luthiraa/TALOS-V2)

Answer:

I’ll split it into **what it is, what’s inside, and why it matters**.

---

## 1. What TALOS-V2 is

TALOS-V2 is a **Transformer → FPGA RTL hardware accelerator project**.

Instead of running a GPT-style model in Python/CUDA, it:

* compiles Transformer inference into **Verilog-style datapaths**
* runs it directly on an FPGA (Cyclone V class board)
* pushes token generation fully on hardware (no host-side decoding loop)

It’s a **teaching + research accelerator**, not production ML infra.

Key claim:

* ~**50k+ tokens/sec inference throughput** on a small character-level GPT

---

## 2. Core idea (mental model)

Think of a Transformer block:

```
x → [QKV projections] → attention → MLP → logits → sampling → next token
```

TALOS-V2 rewires this into:

```
stream tokens →
  fixed-point vector →
    shared MatVec engine →
      QKV + MLP reused tile →
    attention scheduled FSM →
    LUT-softmax + bounded divider →
    hardware sampler →
  next token emitted
```

So instead of:

* tensor ops on GPU kernels

You get:

* **state machines + MAC arrays + ROM weights + streaming datapaths**

---

## 3. Architecture (what’s actually built)

### (1) Fixed-point core

* Q4.12 (16-bit signed fixed-point)
* avoids floating point entirely
* weights stored in FPGA ROM (`$readmemh` style)

Why:

* deterministic timing
* fits FPGA DSP + LUT budget

---

### (2) Reusable MatVec engine (centerpiece)

Everything reduces to:

```
y = W · x
```

Used for:

* Q, K, V projections
* attention output projection
* MLP expansion + projection
* LM head

Design:

* **16-lane streamed MAC tile**
* time-multiplexed across layers

Key tradeoff:

> reuse hardware instead of duplicating parallel blocks

---

### (3) Attention is a schedule, not a formula

Original math:

[
softmax(QK^T / \sqrt{d}) V
]

RTL decomposition:

* dot-product stream Q/K
* max tracking (for stability)
* LUT exp approximation
* accumulation
* multicycle division engine

Important:

* softmax is **not a function block**
* it’s a **multi-stage FSM pipeline**

---

### (4) Optimizations that actually mattered

Not “more parallelism everywhere”, but:

* **folding FSM work into compute passes**

  * e.g. max tracking during dot-product
* **bounded math engines**

  * div / RMSNorm iterative units
* **streaming instead of buffering**
* **hardware sampling (no CPU)**
* **targeted dual-divider for attention bottleneck**
* clock bump after timing closure (~56.25 MHz)

---

## 4. Performance claim

* ~**53k tokens/sec**
* full generation loop on FPGA
* host not involved in token selection

This is important:

> sampling + next-token loop is fully on-chip

So it’s not “fast kernel execution”, it’s **hardware autoregressive inference loop**.

---

## 5. Why this repo is interesting (engineering view)

This is basically:

> “what if GPT inference was a CPU pipeline design problem”

Key learning signals:

### A. Transformers are just repeated MatVec

Once you see:

```
Attention = MatVec + reduction + normalization
MLP      = MatVec + activation + MatVec
```

The architecture collapses into one reusable compute tile.

---

### B. Hardware forces schedule thinking

In software:

* ops are declarative

In TALOS:

* everything is **cycle-ordered FSM steps**

---

### C. Bottlenecks are memory + division, not MACs

* softmax/div dominates design complexity
* compute is cheap compared to routing + timing closure

---

## 6. Minimal mental diagram

```
            +-------------------+
token --->   | embedding ROM     |
            +---------+---------+
                      |
                      v
            +-------------------+
            | 16-lane MatVec    | <--- shared across all layers
            +----+---+---+------+
                 Q   K   V   MLP
                      |
                      v
            +-------------------+
            | attention FSM     |
            | LUT exp + div     |
            +---------+---------+
                      |
                      v
            +-------------------+
            | LM head + sampler |
            | (hardware RNG)    |
            +---------+---------+
                      |
                      v
                 next token
```

---

## 7. One-line summary

TALOS-V2 is a **Transformer inference engine compiled into FPGA datapaths**, where:

* MatVec = single reusable hardware tile
* Attention = scheduled FSM
* Softmax/div = bounded approximations
* sampling = on-chip logic
* result = ~50k tok/s autoregressive generation

---

If you want, I can break down:

* exact FSM schedule per token cycle
* how 16-lane tile maps to QKV weights
* or compare it to TensorRT / CUDA kernel fusion vs this RTL approach

---

References:

* [https://github.com/Luthiraa/TALOS-V2](https://github.com/Luthiraa/TALOS-V2)
* [https://v2.talos.wtf/](https://v2.talos.wtf/) ([v2.talos.wtf][1])

[1]: https://v2.talos.wtf/?utm_source=chatgpt.com "Talos"
