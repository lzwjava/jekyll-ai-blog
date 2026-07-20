---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fenvi Riser Works, Dual GPU Limited
translated: false
type: note
---

**Question: Can the Fenvi PCIe 5.0 x16 riser cable work with MSI MAG B760M Mortar and allow two RTX GPUs?**

**Answer:**

Short answer: **yes, the PCIe 5.0 x16 riser cable is compatible with MSI MAG B760M Mortar, but it does NOT solve the "two RTX GPU" problem by itself.** The limitation is the motherboard PCIe layout, not the riser cable.

Your setup:

* Motherboard: MSI MAG B760M Mortar
* CPU: likely Intel 12th/13th/14th gen
* GPU: RTX 4070 / RTX 3090 etc.
* Riser: Fenvi PCIe 5.0 x16 20cm

## 1. Will PCIe 5.0 riser work?

Yes.

PCIe is backward compatible:

```
PCIe 5.0 riser
        |
        v
PCIe 4.0 motherboard slot
        |
        v
RTX 4070 / RTX 3090
```

It will negotiate down:

```
PCIe 5.0 x16 cable
        ↓
PCIe 4.0 x16 link
        ↓
GPU runs normally
```

RTX 4070 is PCIe 4.0 x16.
RTX 3090 is PCIe 4.0 x16.

No performance loss from a good 20cm PCIe 5.0 riser.

---

## 2. Can MSI B760M Mortar run two RTX cards?

The answer is: **physically yes, practically limited.**

The board usually has:

```
CPU PCIe lanes:

16 lanes -> top GPU slot
4 lanes  -> M.2 SSD


Chipset PCIe lanes:

x4/x1 slots
```

Typical layout:

```
CPU
 |
 +---- PCIe x16 slot
 |        |
 |        RTX GPU #1
 |
 +---- M.2


Chipset
 |
 +---- PCIe x16 physical slot (x4 electrical)
          |
          RTX GPU #2
```

So:

GPU #1:

```
PCIe 4.0 x16
```

GPU #2:

```
PCIe 4.0 x4
```

The second GPU works, but bandwidth is much lower.

---

## 3. For AI workloads, is x4 enough?

Depends.

For inference:

Example:

```
RTX 4070 12GB
+
RTX 3090 24GB
```

You can run:

* vLLM multi-GPU
* llama.cpp split mode
* PyTorch model parallel
* CUDA distributed

The second GPU being x4 is often acceptable.

Reason:

LLM inference is mostly:

```
GPU compute
+
VRAM capacity
```

not PCIe bandwidth.

Example:

```
70B model

GPU0:
35GB

GPU1:
35GB

PCIe traffic:
only activation synchronization
```

Not constantly moving the whole model.

---

For training:

Much worse.

Example:

```
DDP training

GPU0 <---- gradients ----> GPU1
```

You want:

```
PCIe x16
NVLink
InfiniBand
```

x4 becomes a bottleneck.

---

## 4. Physical problem: GPU size

The bigger issue with B760M Mortar:

Two RTX cards normally cannot fit.

Example:

RTX 3090:

```
3-slot width
```

RTX 4070:

```
2-slot width
```

Together:

```
3090 ███
4070 ██

needs 5 slots
```

mATX board:

```
[ GPU slot ]
[ blocked ]
[ small slot ]
```

Usually impossible.

A riser helps:

```
GPU #1
vertical outside case


GPU #2
normal slot
```

Example:

```
        RTX3090
          |
          |
     PCIe riser
          |
----------------
 MSI B760M
----------------
      RTX4070
```

---

## 5. Recommended configuration

For your AI experiments:

### Option A: Keep B760M

Good:

```
RTX3090
+
RTX4070

RTX3090 -> main x16 slot
RTX4070 -> riser / second slot x4
```

Works for:

* local LLM inference
* agents
* vLLM testing
* LoRA experiments

### Option B: Serious multi-GPU

Move to workstation platform:

```
Threadripper
EPYC
Xeon W
```

Example:

```
PCIe lanes:

GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
```

Then multiple RTX 3090/4090 makes sense.

---

## 6. About Fenvi PCIe 5.0 riser

The product you mention:

```
Fenvi PCIe5.0 X16
20cm
90 degree
```

is actually a good choice.

Why:

* PCIe 5.0 signal quality margin
* backward compatible
* short cable (20cm is better than 50cm)
* x16 wiring

For AI rigs, I would prefer:

```
PCIe 5.0 x16 riser
20cm
shielded
```

over cheap PCIe 3.0 risers.

---

Final recommendation for your B760M:

```
MSI B760M Mortar
        |
        +-- RTX3090
        |     PCIe x16
        |
        +-- RTX4070
              PCIe x4 via Fenvi riser
```

This is a reasonable **AI inference / agent workstation**.

But if your goal is:

```
4x RTX3090
5x RTX3060
multi-GPU training
```

then don't spend money on risers for B760M. The CPU PCIe lane count is the real wall.
