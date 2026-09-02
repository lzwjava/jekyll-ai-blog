---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA GPU MATS MODS Guide
translated: false
type: note
---

Question: **What is the Levirepair thread about, and is it the MATS/MODS GPU memory-testing tool you're looking for?**

Answer:

Yes. **This is highly relevant to GPU repair.** The page is a community-maintained collection of **NVIDIA MATS + MODS + NVMT tools and bootable Linux environments** specifically for diagnosing graphics cards. ([Levirepair][1])

[Levirepair — Nvidia MATS & MODS USB stick thread](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com)

### 1. The three important tools

| Tool     | What it tests                  | Useful for                                         |
| -------- | ------------------------------ | -------------------------------------------------- |
| **MATS** | GPU **VRAM**                   | Finding bad GDDR memory                            |
| **MODS** | GPU + VRAM / GPU functionality | Broader GPU hardware testing                       |
| **NVMT** | NVIDIA information/diagnostics | VBIOS, device information, memory-related analysis |

The author explicitly says:

> `mods` will test the GPU with memory
> `mats` will only test the memory of the GPU. ([Levirepair][1])

So the mental model is:

```text
                    NVIDIA GPU
                       │
             ┌─────────┴─────────┐
             │                   │
          GPU core             VRAM
             │                   │
           MODS                 MATS
       GPU + memory          memory only
```

### 2. This is basically the kind of tool you were asking about

You previously asked whether there is something analogous to a **car diagnostic scanner** for an NVIDIA GPU.

**MATS/MODS is one of the closest things in the GPU-repair world.**

Instead of:

```text
Car
  ↓
OBD scanner
  ↓
Error code
  ↓
Faulty subsystem
```

you get something closer to:

```text
GPU
 ↓
Boot diagnostic Linux
 ↓
MATS / MODS
 ↓
Memory / GPU test
 ↓
Error information
 ↓
Map error → VRAM channel / chip / GPU subsystem
 ↓
Physical repair
```

For example, if you're repairing a card with **black screen / artifacts / driver crashes**, MATS can potentially tell you that the VRAM subsystem is producing errors rather than making you blindly replace components.

### 3. The really interesting part: it maps VRAM errors

The thread contains **memory-layout diagrams** and mappings for different generations, including GDDR5/GDDR6/GDDR6X. ([Levirepair][1])

It also contains information specifically intended to correlate memory testing with physical memory chips.

That's extremely useful for your current direction:

```text
MATS error
    ↓
memory channel / address
    ↓
physical GDDR chip
    ↓
measure surrounding circuit
    ↓
replace VRAM / repair trace / investigate GPU
```

That's much more useful for repair than simply running FurMark or a CUDA benchmark.

### 4. It is bootable from USB

The main package described in the thread is a Linux-based USB environment.

The original package contains:

* MATS
* MODS
* NVMT
* multiple MODS versions
* scripts
* automatic report saving
* different GPU-generation environments

The thread says the main image is around **2.31 GB**, and the installation instructions use Rufus to write it to a USB stick. ([Levirepair][1])

There are also newer separate environments for:

```text
GTX
RTX
RTX 50-series
```

The author specifically notes that RTX 50-series requires **UEFI and PCIe Gen 5** for this environment. ([Levirepair][1])

### 5. Primary vs secondary GPU

This part is particularly useful for a dead GPU.

If the GPU still outputs video:

```text
GPU
 │
 └── HDMI/DP → monitor

boot USB
   ↓
MATS/MODS
```

You can test it as the primary GPU.

But if the GPU **doesn't produce an image**, the thread describes using a motherboard/CPU with integrated graphics:

```text
CPU iGPU
   │
   └── monitor

broken NVIDIA GPU
   │
   └── PCIe x16

        ↓

boot MATS/MODS

        ↓

modsinit
        ↓
MATS/MODS tests secondary GPU
```

The instructions explicitly give:

```bash
modsinit
mods
```

for MODS, and:

```bash
modsinit
mats -n 1
```

for MATS on a secondary GPU. ([Levirepair][1])

**That is very relevant to your repair experiments.**

### 6. There is even a VRAM-temperature experiment

The thread gives this MODS command:

```bash
./mods gputest.js -test 13 \
    -run_on_error \
    -bg_dram_temp 1000
```

It's intended to test/log VRAM temperature and help identify a problematic memory chip. ([Levirepair][1])

That is an interesting repair workflow:

```text
Run memory/GPU test
       ↓
error occurs
       ↓
observe DRAM temperature
       ↓
identify suspicious VRAM
       ↓
inspect that chip electrically
       ↓
replace/reball/etc.
       ↓
rerun MATS
```

### 7. There is also channel disabling

The thread contains MODS `floorsweep` information for disabling particular FBIO/FBP channels.

For example:

```text
A = 0x01
B = 0x02
C = 0x04
D = 0x08
E = 0x16
F = 0x32
```

and explains combining masks to disable multiple channels. ([Levirepair][1])

This is **advanced GPU repair territory**: you're no longer simply asking "does VRAM work?" You're experimenting with the GPU's memory topology to isolate a defective memory channel.

---

## For your 4090/4070 repair learning

I'd put this site very high on your list.

Your eventual workflow could look like:

```text
              ┌──────────────────┐
              │ Dead / faulty GPU│
              └────────┬─────────┘
                       │
              visual inspection
                       │
              resistance / diode
                       │
              power rails
                       │
              PCIe / auxiliary power
                       │
              ┌────────▼────────┐
              │   Does GPU POST?│
              └───────┬─────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
         YES                      NO
          │                       │
       MATS/MODS              electrical
          │                   diagnosis
          │                       │
      VRAM errors?            power/BIOS/
          │                   GPU-core etc.
          ↓
    map memory channel
          ↓
    identify physical
       GDDR chip
          ↓
    repair/replace
          ↓
       MATS again
```

**MATS/MODS should therefore be one of the first software tools you learn**, alongside the multimeter, oscilloscope, boardview/schematic, and eventually a programmer/rework setup.

One important caveat: the thread is a **community distribution**, not an NVIDIA-supported diagnostic product. The page also points users toward community sources for obtaining some MODS versions. ([Levirepair][1]) So I'd treat downloaded images/tools as untrusted software: verify hashes where provided, use a dedicated test machine, and don't put sensitive data on the boot environment.

The page provides an MD5 hash for its main image:

```text
3cc2ce1e4b9836548a8fad6479a2c4c3
```

and CRC32:

```text
15B10F3F
```

([Levirepair][1])

For **your current GPU-repair setup**, the next thing I'd learn is **exactly how MATS converts an error like `FBIO / channel / address` into "this physical GDDR6(X) chip on the board is probably bad."** That's the part that turns MATS from a benchmark into a repair diagnostic.

[1]: https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3 "Nvidia MATS & MODS USB stick (with NVMT): Forum - Levirepair"
