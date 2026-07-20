---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX vs mATX for Multiple GPUs
translated: false
type: note
---

Question: What is a PCIe extension cable in the context of using multiple GPUs, and why do people recommend ATX motherboards instead of mATX for two or more GPUs?

Answer:

A **PCIe 延长线 (PCIe riser cable / PCIe extension cable)** is a cable that extends the PCIe slot so you can move the GPU away from the motherboard.

Normally:

```
GPU
 |
 |  (direct connection)
 |
PCIe x16 slot on motherboard
```

With a riser:

```
Motherboard PCIe slot
        |
        |
   PCIe extension cable
        |
        |
      GPU
```

The GPU no longer has to physically sit directly above the motherboard slot.

Common examples:

* Mining rigs
* AI multi-GPU servers
* Small cases
* Workstations with large GPUs

A typical riser has:

```
PCIe x16 motherboard adapter
        |
        |
 ribbon cable
        |
        |
PCIe x16 GPU adapter
```

Usually the electrical connection is still only **PCIe x1/x4/x8**, depending on the riser. Many mining risers use PCIe x1 because bandwidth is not important for mining.

For AI inference/training, you generally want:

* PCIe x16 physical slot
* PCIe x8 electrical minimum per GPU if possible
* high quality shielded riser if using extension

---

## Why ATX instead of mATX for 2+ GPUs?

The problem is not only "number of slots"; it is:

1. **Physical spacing**
2. **PCIe lanes**
3. **Cooling**

Example:

### mATX board

```
CPU

PCIe x16
========
RTX 3090 (3-slot)

PCIe x4
====
blocked
```

A RTX 3090 / 4090 is usually 2.5~4 slots thick.

After installing one GPU:

```
GPU
GPU cooler
GPU cooler
GPU cooler
```

it covers the next PCIe slot.

So even if the motherboard has:

```
PCIe x16
PCIe x16
```

physically there is no room.

---

ATX:

```
CPU

PCIe x16
========
(empty spacing)

PCIe x16
========

PCIe x4
====
```

Example:

```
RTX3090
  |
  | 2 slots gap
  |
RTX3090
```

Both cards can breathe.

---

## PCIe lane issue

Consumer platforms are also limited.

Example:

### Intel i9-13900K

CPU PCIe:

```
CPU
 |
 +-- PCIe 5.0 x16
 |
 +-- PCIe 4.0 x4
```

So motherboard manufacturers split:

```
GPU1: x8
GPU2: x8
```

or:

```
GPU1: x16
GPU2: chipset x4
```

depending on design.

For AI workloads:

* LLM inference:

  * PCIe bandwidth matters less
  * multiple GPUs can work

* Training:

  * gradient synchronization matters
  * PCIe bandwidth matters a lot

---

## Example multi-GPU setup

### Cheap AI workstation

```
ATX motherboard

RTX3090
PCIe x8

RTX3090
PCIe x8

128GB RAM

850W~1200W PSU
```

Good.

---

### mATX with risers

Possible:

```
mATX

GPU1
 |
PCIe riser

GPU2
 |
PCIe riser
```

but:

* worse airflow
* fewer lanes
* more cable problems
* harder debugging

It is common in mining, less ideal for AI.

---

## Server/workstation boards solve this

For 4-8 GPUs:

```
EPYC motherboard

CPU PCIe lanes:

128 lanes

GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
GPU5 x16
GPU6 x16
GPU7 x16
GPU8 x16
```

Examples:

* AMD EPYC
* Intel Xeon W
* Xeon Scalable

This is why AI servers use boards like Gigabyte G292-Z20, Supermicro, ASUS ESC series.

---

For your RTX 4070 / possible RTX3090 multi-GPU experiments:

* 2 GPUs → ATX consumer board is reasonable
* 3-4 GPUs → workstation/server board is much better
* 8 GPUs → EPYC + PCIe risers/backplane

PCIe risers are mainly a **mechanical solution**. They do not create more PCIe lanes. The motherboard + CPU determine the actual bandwidth.
