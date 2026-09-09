---
audio: false
generated: true
image: false
lang: en
layout: post
title: How MODS and MATS Diagnose GPUs
translated: false
type: note
---

Question: **How do MODS and MATS actually work internally when diagnosing a dead/no-display NVIDIA GPU?**

Answer:

Think of them as two layers:

```text
                    NVIDIA GPU
                       │
              ┌────────┴────────┐
              │                 │
             MODS              MATS
        "Can I control       "Can I test
         the GPU?"            VRAM?"
              │                 │
       GPU/core/driver       VRAM data path
       initialization        + memory chips
```

### 1. MODS = the GPU test framework

**MODS** is much more than a VRAM tester. It is NVIDIA's internal/manufacturing-oriented diagnostic environment.

Conceptually:

```text
mods
 │
 ├── discover PCIe GPU
 ├── initialize GPU
 ├── initialize RM/driver state
 ├── initialize memory controller
 ├── run individual tests
 └── report hardware failures
```

For your no-display card, this command:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

is basically asking:

> "Can I get far enough into NVIDIA GPU initialization that the test framework can communicate with this GPU?"

That is why the **PASS screen is important**.

It doesn't mean:

> "The GPU is healthy."

It means something closer to:

> **The GPU reached a sufficiently functional state for the diagnostic software to take control of it.**

That is a huge distinction.

---

## 2. Why the motherboard iGPU matters

Suppose your RTX 4060 has:

```text
GPU output ─────X──── monitor
```

You don't actually need the discrete GPU to produce video for MODS/MATS.

Instead:

```text
                 CPU iGPU
                   │
                 monitor
                   │
              Linux/test OS
                   │
                 PCIe
                   │
              RTX 4060
```

The OS can display the test program using the iGPU while MODS talks to the discrete GPU over PCIe.

So:

```text
Display path:
CPU iGPU → monitor

Diagnostic path:
CPU → PCIe → NVIDIA GPU
```

This is the trick that makes a **"点不亮" GPU potentially testable**.

---

# 3. What happens electrically

A useful mental model is:

```text
PCIe
 │
 ▼
GPU core
 │
 ├── GPU logic
 │
 ├── memory controller
 │       │
 │       ├── VRAM0
 │       ├── VRAM1
 │       ├── VRAM2
 │       └── ...
 │
 └── display engine
```

A GPU doesn't need its display engine to be functioning perfectly for MODS to potentially communicate with its PCIe endpoint and GPU core.

But it **does** need enough of its power rails and core logic alive.

For example, conceptually:

```text
12V / PCIe power
       │
       ▼
VRM
 │
 ├── GPU core rail
 ├── memory rail
 └── auxiliary rails
       │
       ▼
    GPU starts
       │
       ▼
 PCIe enumeration
       │
       ▼
 NVIDIA initialization
       │
       ▼
      MODS
```

If the GPU never reaches the initialization stage, MODS can't magically bypass the dead silicon.

That's why:

```text
No MODS PASS
        │
        ├── dead power rail
        ├── VRM problem
        ├── GPU core problem
        ├── severe PCIe/core initialization failure
        └── potentially other board-level faults
```

It **doesn't automatically prove "GPU core is bad."**

That's an important practical correction.

---

# 4. MATS is much more specific

Once MODS establishes that the GPU is usable, **MATS** attacks the memory subsystem.

Think:

```text
                GPU core
                   │
             memory controller
                   │
          ┌────────┼────────┐
          │        │        │
        VRAM0    VRAM1    VRAM2 ...
```

MATS writes known patterns into VRAM and reads them back.

For example, conceptually:

```c
write(addr, 0xAAAAAAAA);
read(addr);
compare(expected, actual);
```

Then:

```c
write(addr, 0x55555555);
read(addr);
compare(expected, actual);
```

And more complicated patterns are used to expose different failure modes.

The fundamental operation is:

```text
GPU → memory controller → VRAM
 ↑                         │
 └──────── read back ──────┘
```

---

# 5. Why MATS can identify a particular memory chip

This is the really useful part for GPU repair.

Modern GDDR memory is physically distributed around the GPU:

```text
              VRAM
        ┌──────────────┐
        │      A       │
        │              │
   B ───┤     GPU      ├── C
        │              │
        │      D       │
        └──────────────┘
              │
              E/F...
```

The GPU's memory controller has different channels / byte lanes connected to different physical memory devices.

Suppose:

```text
VRAM0 → channel 0
VRAM1 → channel 1
VRAM2 → channel 2
VRAM3 → channel 3
```

A damaged chip might produce something like:

```text
Expected: 10101010
Actual:   10100010
              ^
           bit failure
```

MATS can observe **which memory address / channel / data bits fail**.

The diagnostic software then maps that logical failure back to a physical memory device.

That's how a report can effectively tell you:

```text
FBI0A0
address ...
channel ...
data ...
```

and eventually allow the repair technician to infer:

> **"This particular GDDR chip is probably the bad one."**

---

# 6. What does `FBI0A0` mean?

Don't think of `FBI0A0` as:

> "VRAM chip #0."

It's more like a **logical memory-controller/test-engine identifier**.

The exact interpretation depends on the NVIDIA GPU generation and MODS/MATS version.

The important repair workflow is:

```text
MATS failure
      │
      ▼
logical memory failure
      │
      ▼
channel / byte-lane information
      │
      ▼
physical VRAM device mapping
      │
      ▼
replace/reball/test that chip
```

So you shouldn't blindly assume that `FBI0A0` literally means the first physical chip.

---

# 7. Why the `-n 1 -e 5` command matters

For example:

```bash
./mats -n 1 -e 5
```

The exact flags are version-dependent, but conceptually you're telling MATS which GPU/test configuration to execute and how aggressively/which test set to run.

Then:

```bash
less report.txt
```

gives you the result.

The important distinction is:

```text
MODS
 ↓
Can the GPU be initialized?

MATS
 ↓
Can GPU memory reliably store/retrieve data?
```

---

# 8. The really useful repair decision tree

For the kind of used/broken GPUs you're interested in, I'd use this mental model:

```text
                    GPU inserted
                         │
                         ▼
                  Does motherboard
                   see PCIe device?
                    /           \
                  NO             YES
                  │               │
             board-level         │
             investigation       ▼
                            Run MODS
                                │
                         ┌──────┴──────┐
                         │             │
                       FAIL          PASS
                         │             │
                    power/core       Run MATS
                    /PCIe/etc.          │
                                      ┌─┴─┐
                                    PASS FAIL
                                      │    │
                                   likely  VRAM
                                   OK      investigation
                                            │
                                            ▼
                                    identify failing
                                    channel/chip
                                            │
                                            ▼
                                    replace/reball VRAM
                                            │
                                            ▼
                                          MATS
```

And **PCIe enumeration itself is another valuable signal**:

```bash
lspci | grep -i nvidia
```

If Linux sees:

```text
NVIDIA ...
```

that's useful evidence that at least part of the PCIe/device initialization path is alive.

If it doesn't, don't immediately jump to "GPU core dead"—you need to investigate power, PCIe reset, clocks, BIOS/board issues, etc.

---

## 9. For your 4060 repair example

For a card described as:

> PCB burned, VRAM around 1.8 is shorted, usable as donor/reball board

I'd **not start by running MATS**.

First establish:

```text
1. Visual inspection
2. Resistance-to-ground measurements
3. Identify which rail is shorted
4. Check 12V input
5. Check major VRM rails
6. Check GPU/core rail
7. Check memory rail
8. Check PCIe enumeration
9. MODS
10. MATS
```

Because if you have a genuine hard short on a major rail:

```text
shorted rail
    ↓
VRM current limit / protection
    ↓
GPU cannot initialize
    ↓
MODS cannot reach useful testing
    ↓
MATS is irrelevant
```

**MATS is therefore a late-stage diagnostic tool, not a replacement for board-level electrical diagnosis.**

For GPU repair, the most powerful combination is:

```text
multimeter
   +
oscilloscope
   +
boardview/schematic
   +
MODS
   +
MATS
```

That lets you go from **"this 4060 is dead" → "this rail is abnormal" → "GPU does/doesn't initialize" → "this memory channel fails" → "this physical GDDR chip is the likely culprit."**

I can also walk you through a **real RTX 4060 MODS → MATS → VRAM-chip mapping workflow**, including how to go from a MATS error address/channel to the physical chip on the PCB.
