---
audio: false
generated: true
image: false
lang: en
layout: post
title: Physical VRAM Addition to GPUs
translated: false
type: note
---

Question: **Can you physically add VRAM to GPUs like the RTX 3060 and flash a new VBIOS to make the GPU report/use more VRAM?**

Answer: **Yes, sometimes. But VBIOS alone cannot increase VRAM.** You need three layers to line up:

```text
          physical
        ┌────────────┐
        │ VRAM chips │
        └─────┬──────┘
              │
        electrical topology
              │
        ┌─────▼──────┐
        │ GPU memory │
        │ controller │
        └─────┬──────┘
              │
           VBIOS
              │
        ┌─────▼──────┐
        │   driver   │
        └────────────┘
```

If you only flash a VBIOS:

```text
8GB physical VRAM
       +
"16GB" VBIOS
       ↓
usually still 8GB / initialization failure
```

### RTX 3060 is actually an interesting candidate

The RTX 3060 12GB uses a **192-bit memory bus**.

That gives:

```text
192 / 32 = 6 memory channels
```

With typical 2GB GDDR6 packages:

```text
6 × 2GB = 12GB
```

If you replace them with 4GB devices:

```text
6 × 4GB = 24GB
```

So, **in principle**, a 12GB → 24GB physical modification is much more straightforward than trying to make an arbitrary GPU address an unsupported capacity.

The important constraint is the GPU's **memory controller/addressing capability**, not merely the VBIOS.

---

### There are basically 3 different mods

#### A. Same number of chips, higher-density chips

Example:

```text
Original:

GPU
 ├── 2GB
 ├── 2GB
 ├── 2GB
 ├── 2GB
 ├── 2GB
 └── 2GB
       = 12GB


Modified:

GPU
 ├── 4GB
 ├── 4GB
 ├── 4GB
 ├── 4GB
 ├── 4GB
 └── 4GB
       = 24GB
```

This is the cleanest architecture **if the GPU memory controller and VBIOS support those densities**.

---

#### B. Add another chip to each channel

This is the clamshell approach:

```text
channel 0 ──┬── VRAM
            └── VRAM

channel 1 ──┬── VRAM
            └── VRAM

...
```

Potentially:

```text
12GB → 24GB
```

without changing the density of each chip.

But now PCB routing, memory training, signal integrity and firmware become substantially harder.

---

#### C. Just flash a larger-capacity VBIOS

```text
12GB physical
      ↓
24GB VBIOS
      ↓
❌
```

Generally useless.

The VBIOS describes/configures hardware that actually exists; it doesn't create additional DRAM.

---

## The really fun part: finding the maximum

For a GPU modding project, I'd approach it experimentally.

For example:

```text
RTX 3060
   │
   ├── identify GPU memory controller
   │
   ├── identify original GDDR6 chips
   │
   ├── inspect PCB
   │
   ├── inspect VBIOS memory tables
   │
   ├── determine supported density
   │
   └── test replacement chips
```

You can first inspect the stock card:

```bash
nvidia-smi -q
```

Then dump the VBIOS:

```bash
sudo nvflash --save 3060.rom
```

Then inspect it with tools such as **NVIDIA BIOS Editor / community VBIOS tooling** and compare against VBIOSes from cards using different memory configurations.

But **don't flash arbitrary VBIOSes**. A mismatched memory configuration can give you a black-screen card, and recovery may require an external programmer or another GPU.

---

## One particularly important thing

There are two independent questions:

### Can the GPU address it?

```text
GPU memory controller
       ↓
address space
       ↓
maximum supported configuration
```

### Can the board electrically run it?

```text
GDDR6/GDDR7
   ↓
signal integrity
   ↓
PCB traces
   ↓
power
   ↓
memory training
   ↓
stable operation
```

You need **both**.

That's why the Suqiao 96GB 5090 is interesting: they're effectively demonstrating that the Blackwell memory subsystem can be paired with a much larger physical memory configuration, assuming the reported hardware is genuine.

---

### If you want to actually build one

I'd start with a **cheap RTX 3060 12GB**, not a 5090.

The experiment would be:

```text
RTX 3060 12GB
      ↓
identify exact GDDR6 part
      ↓
find 4GB-compatible GDDR6 replacement
      ↓
replace 6 chips
      ↓
modify/patch VBIOS memory configuration
      ↓
boot
      ↓
nvidia-smi
      ↓
CUDA memory test
      ↓
stress test
```

If successful:

```text
3060 12GB
    ↓
3060 24GB
```

would be a very cool proof-of-concept.

**The key first step is identifying the exact 3060 PCB + GPU revision + GDDR6 chip part number.** Different 3060 board revisions can have materially different layouts and memory configurations.

If you give me the **exact RTX 3060 model/PCB (e.g. GPU-Z screenshot or photo of the PCB)**, I can work through the memory chips, bus topology, candidate replacement DRAM, and what would have to change in the VBIOS.
