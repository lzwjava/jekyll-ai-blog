---
audio: false
generated: true
image: false
lang: en
layout: post
title: Plausible But Unconfirmed TPU Claims
translated: false
type: note
---

Question: Is the claim about Google “Frozen V2” TPU integrating SRAM on-die and abandoning TSMC CoWoS for Gemini correct?

Answer:

Short answer: **the direction is plausible, but the article mixes confirmed facts, analyst speculation, and some exaggerated wording.**

The core idea:

* Google is indeed pushing custom TPU architectures to reduce dependence on NVIDIA GPUs.
* Memory bandwidth and data movement are becoming the dominant bottlenecks in AI accelerators.
* Putting more SRAM closer to compute is a real architectural trend.
* But **“abandoning CoWoS completely” and “SRAM directly integrated into silicon” are not publicly confirmed Google product details.**

Let's break it down.

---

## 1. Why SRAM-on-die matters

Modern AI accelerators are mostly limited by:

```
HBM/DRAM
   |
   |  (huge latency + energy cost)
   v
GPU/TPU compute units
```

The expensive part is moving data.

For example:

```
Compute:
  Matrix multiply: cheap

Memory movement:
  Fetch weights
  Fetch activations
  Write intermediate results
  Expensive
```

A rough energy hierarchy:

```
Register        ~1 pJ
SRAM            ~5-20 pJ
HBM             ~100+ pJ
DDR             much higher
```

So if you can put more SRAM close to the TPU cores:

```
Before:

TPU core <---> HBM


After:

+----------------------+
| TPU compute          |
|                      |
| SRAM cache           |
|                      |
+----------------------+
```

You reduce:

* latency
* power
* bandwidth pressure

This is exactly why companies explore:

* SRAM cache
* 3D stacking
* wafer-scale computing
* near-memory computing

---

## 2. But "no CoWoS" is a big claim

NVIDIA's current AI GPUs:

```
GPU die
 |
CoWoS interposer
 |
HBM stacks
```

Example:

```
        HBM
         |
HBM -- interposer -- HBM
         |
       GPU die
```

CoWoS exists because:

* HBM requires extremely wide connections
* GPU die and HBM are separate technologies
* manufacturing yield is better

A pure monolithic approach:

```
+----------------+
| TPU            |
|                |
| SRAM           |
|                |
+----------------+
```

has problems:

### Yield

Large chips fail more often.

If one huge die contains:

* compute
* SRAM
* IO

one defect can kill the entire chip.

### SRAM density

SRAM consumes a lot of silicon area.

Example:

A 1GB SRAM cache is enormous compared with logic.

Modern processors usually use:

```
CPU:
small SRAM cache
+
large DRAM

AI:
needs enormous memory bandwidth
```

---

## 3. The interesting part: inference vs training

This architecture makes more sense for **Gemini inference** than training.

Training:

```
Huge model
+
Huge optimizer states
+
Huge datasets
```

requires:

* HBM
* networking
* distributed clusters

Inference:

```
Fixed model
Repeated queries
```

can benefit from:

* custom memory hierarchy
* fixed weights
* specialization

A Gemini inference chip could be:

```
Google Search
      |
      v
Gemini model
      |
      v
Frozen TPU
      |
      v
High throughput inference
```

Google controls the whole stack:

```
Model
 |
Compiler
 |
TPU
 |
Datacenter
```

This is their biggest advantage.

---

## 4. The Taalas comparison

The Taalas approach is more extreme.

They basically say:

```
Traditional:

chip executes neural network

Taalas:

chip IS the neural network
```

Weights become hardware.

Like:

```
Software model:

W1
W2
W3

↓

Silicon wiring
```

Advantages:

* extremely fast inference
* very low power

Disadvantage:

Model changes require new silicon.

This is similar to ASIC vs CPU:

```
CPU:
general purpose

ASIC:
10x faster for one workload
but fixed
```

---

## 5. My assessment

I would rate the article:

| Claim                                 | Confidence |
| ------------------------------------- | ---------- |
| Google develops custom Gemini TPU     | High       |
| Google wants better memory efficiency | High       |
| SRAM closer to compute is a trend     | High       |
| Frozen V2 exists exactly as described | Medium/low |
| No CoWoS at all                       | Low        |
| TPU replaces NVIDIA GPUs              | Too strong |

The real trend is probably:

```
NVIDIA:
GPU + HBM + CoWoS

Google:
TPU + custom memory hierarchy

Amazon:
Trainium + Inferentia

Microsoft:
Maia

Meta:
MTIA
```

The AI hardware future is likely not "GPU dies suddenly."

It is:

```
General AI accelerator
        |
        +-- NVIDIA GPU
        |
        +-- Google TPU
        |
        +-- Amazon Trainium
        |
        +-- ASIC inference chips
        |
        +-- wafer-scale systems
```

Google has one unique advantage: **Gemini is their model, TPU is their silicon, and Google owns the datacenter.** That vertical integration allows them to make aggressive architectures that NVIDIA cannot easily copy because NVIDIA must serve many customers.

References:

* Google TPU architecture: [https://cloud.google.com/tpu/docs](https://cloud.google.com/tpu/docs)
* TSMC CoWoS packaging: [https://www.tsmc.com/english/technology/cowos](https://www.tsmc.com/english/technology/cowos)
* NVIDIA Hopper architecture: [https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/](https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/)
* Taalas AI silicon: [https://taalas.com/](https://taalas.com/)
