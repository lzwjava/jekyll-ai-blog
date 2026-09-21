---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Hardware Modding Techniques
translated: false
type: note
---

Question: **Generally, how do people hardware-mod (“魔改”) GPUs?**

Answer: **GPU modding is usually a combination of hardware rework + VBIOS modification + sometimes driver-level work.** It is not one single trick.

The typical stack looks like this:

```text
                  GPU MOD
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    DRAM mod      VBIOS mod    PCB/power mod
        │            │            │
    capacity       timings       VRM
    density        straps        power limit
    population     clocks        voltage
```

### 1. VRAM mod — most common "魔改"

The simplest interesting case is:

```text
RTX 3060 12GB
     │
     │ replace DRAM
     ↓
RTX 3060 24GB
```

There are several techniques:

**Higher-density DRAM**

```text
original:
6 × 2GB = 12GB

replacement:
6 × 4GB = 24GB
```

**Additional DRAM**

```text
original:

GPU ── 6 memory channels

modified:

GPU ── 6 channels
       ├── chip
       └── chip
```

This requires the GPU memory controller + PCB + firmware to support the topology.

---

### 2. VBIOS modification

VBIOS contains configuration for things such as:

```text
GPU initialization
memory configuration
memory timings
memory clocks
power limits
voltage tables
fan behavior
PCIe configuration
```

So a modder might have:

```text
stock VBIOS
     │
     ├── extract
     │
     ├── modify tables
     │
     └── flash
             ↓
       modified behavior
```

For example:

```text
Power Limit: 250W → 350W
Memory clock: X → Y
Memory configuration: A → B
```

But **VBIOS cannot create hardware that isn't physically present**.

---

### 3. GPU core / memory straps

Older NVIDIA cards were particularly interesting because **memory "straps"** could be modified.

Conceptually:

```text
Memory frequency
      ↓
timing selection
      ↓
tRCD / tRP / tRAS / etc.
      ↓
GDDR initialization
```

A modder can sometimes use tighter/looser timings to get:

```text
higher memory clock
        ↕
stability
        ↕
bandwidth
```

This is why two otherwise identical cards can have very different overclocking behavior after VBIOS modification.

---

### 4. PCB modification

This is where serious Chinese GPU ODMs get much more interesting.

They can manufacture a new PCB:

```text
NVIDIA GPU
    │
    ├──────── memory bus ────────┐
    │                            │
    │                        custom PCB
    │                            │
    ├── VRM                     ├── more VRAM
    │                            ├── different VRAM topology
    │                            ├── different power stages
    │                            └── different connectors
```

At this point it's barely a "modified retail GPU" anymore.

It's basically:

> **same GPU silicon + custom board design**

This is likely the category that products like the claimed 96GB 5090 fall into.

---

### 5. Power-limit / VRM mods

Another classic:

```text
stock:
GPU → 450W

modified:
GPU → 600W+
```

Possible changes include:

```text
VBIOS power tables
        +
shunt resistors
        +
VRM configuration
        +
better cooling
```

But increasing the power limit doesn't automatically increase performance; you're trading against voltage, thermals, and silicon limits.

---

### 6. Sometimes people modify the physical GPU itself

Much rarer and much harder.

Examples include:

```text
GPU package
   ↓
remove package
   ↓
reball / replace
   ↓
different memory configuration
```

Or replacing the GPU die/package with another compatible variant.

This is extremely different from flashing a VBIOS.

---

## The useful mental model

Think of a GPU as:

```text
              ┌──────────────┐
              │   GPU die    │
              │              │
              │ SMs          │
              │ cache        │
              │ memory ctrl  │
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              │     PCB      │
              └──┬───────┬───┘
                 │       │
              VRAM       VRM
                 │       │
              capacity   power
              bandwidth  voltage
```

**魔改 means changing one or more layers underneath the same GPU silicon.**

The interesting combinations are:

```text
12GB → 24GB
   = DRAM + VBIOS

250W → 350W
   = VRM + VBIOS

lower timings
   = VBIOS/DRAM

different memory topology
   = PCB + DRAM + VBIOS

5090 32GB → 96GB
   = custom PCB + DRAM + firmware
```

And there is a very important historical distinction: **Pascal/Turing/Ampere-era cards can have very different modding possibilities depending on the exact memory controller and PCB.** You cannot generalize "RTX 3060" from one board partner to another.

If you're interested in actually doing this, the rabbit hole I'd suggest is **RTX 3060 12GB → 24GB**. It's cheap enough to sacrifice a board and gives you a clean way to understand the entire chain: **GDDR6 datasheet → PCB topology → memory controller → VBIOS → CUDA enumeration**.
