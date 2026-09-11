---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skipping RM Init for Dead GPUs
translated: false
type: note
---

Question: **What does `-skip_rm_state_init` actually do in MODS/MATS, and why is it useful for testing a partially dead NVIDIA GPU?**

Answer:

The key idea is:

> **`-skip_rm_state_init` does not magically make the GPU work. It prevents MODS from doing one particular stage of GPU initialization that may fail on a damaged card.**

Think of MODS as sitting between Linux and the GPU:

```text
Linux
  │
  ▼
MODS
  │
  ├── PCIe access
  ├── MMIO/register access
  ├── NVIDIA RM initialization
  │
  ▼
GPU
  ├── GPU core
  ├── VRAM controller
  └── VRAM chips
```

### 1. What is RM?

**RM = Resource Manager**, NVIDIA's low-level GPU management layer.

Conceptually, RM is responsible for turning a GPU from:

```text
PCIe device detected
        ↓
"GPU exists"
```

into:

```text
GPU initialized
        ↓
memory controller configured
        ↓
GPU engines initialized
        ↓
channels / memory mappings / resources available
        ↓
GPU usable by higher-level software
```

So a normal initialization path is approximately:

```text
PCIe enumeration
      ↓
identify GPU
      ↓
RM state initialization
      ↓
initialize GPU subsystems
      ↓
run tests
```

The important distinction is that **PCIe detection is much weaker than successful GPU initialization**.

A broken RTX 3060 can still appear as:

```text
NVIDIA GPU detected on PCIe
```

while failing later during initialization.

---

### 2. What does `-skip_rm_state_init` change?

Without the flag:

```bash
./mods gputest.js
```

MODS tries to initialize the RM state.

With:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

you are essentially telling MODS:

```text
"Don't perform that RM state initialization step.
Load MODS and leave the GPU in the minimally initialized state
needed for the subsequent test workflow."
```

So:

```text
Normal:

PCIe
 ↓
RM init
 ↓
GPU initialized
 ↓
tests


Skip RM state init:

PCIe
 ↓
[SKIP RM state initialization]
 ↓
MODS remains available
 ↓
MATS
 ↓
VRAM testing
```

That's why this combination is useful for **VRAM repair diagnosis**.

---

### 3. The subtle but important point

I would slightly correct the previous explanation:

> `-skip_rm_state_init` does **not** mean "MODS gets raw unrestricted hardware access."

MODS already has low-level hardware access mechanisms.

Rather, you're avoiding an initialization path that requires more of the GPU to be healthy.

That distinction matters.

For example, suppose an RTX 3060 has:

```text
GPU core       OK
PCIe           OK
VRAM controller OK
M0/M1/M2/M3... missing/damaged VRAM
```

A normal initialization might encounter the bad memory configuration and fail.

But for MATS, you may only need enough of the GPU/memory subsystem to perform:

```text
write VRAM
   ↓
read VRAM
   ↓
compare
```

Therefore:

```text
Full GPU initialization
        ↓
       FAIL
```

doesn't necessarily mean:

```text
VRAM testing impossible
```

That's the whole point of the workaround.

---

### 4. Why `-notest` is paired with it

These flags solve **different problems**:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

`-skip_rm_state_init`:

```text
Don't perform RM state initialization.
```

`-notest`:

```text
Don't immediately execute the gputest test sequence.
```

So conceptually:

```text
                 MODS startup
                     │
          ┌──────────┴──────────┐
          │                     │
  skip_rm_state_init          notest
          │                     │
  skip RM state init       don't run tests
          │                     │
          └──────────┬──────────┘
                     ↓
             MODS stays loaded
                     ↓
                  MATS
```

This is why the command is a **bootstrap/setup command**, rather than the actual VRAM test.

---

### 5. Then MATS does the interesting part

Once MODS is successfully resident:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

and you get the expected successful startup, you can run MATS.

MATS is much more interesting for your repair workflow because it can expose **which VRAM device/address region is bad**.

Conceptually:

```text
GPU
 │
 ├── VRAM M0 ─── OK
 ├── VRAM M1 ─── OK
 ├── VRAM M2 ─── FAIL
 ├── VRAM M3 ─── OK
 ├── VRAM M4 ─── OK
 └── VRAM M5 ─── OK
```

Then instead of merely knowing:

```text
"RTX 3060 crashes"
```

you get something closer to:

```text
"Memory device M2 is failing"
```

That is actionable for board repair.

---

### 6. Think of it as a diagnostic ladder

For your GPU-repair setup, I would think about the entire process like this:

```text
             Does the machine POST?
                       │
                       ▼
             Is the GPU visible on PCIe?
                       │
                       ▼
       Can MODS bootstrap with skip-RM?
                       │
                       ▼
             Can MATS access VRAM?
                       │
                       ▼
          Which memory device fails?
                       │
                       ▼
       Inspect VRAM / power / signals
                       │
                       ▼
              Replace / reball
                       │
                       ▼
                  Test again
```

Each level tells you something different.

So if:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

fails, **don't immediately conclude "the GPU core is dead."**

Possible causes include:

```text
wrong MODS/MATS version
       │
       ├── wrong GPU generation support
       ├── incorrect command/environment
       ├── PCIe communication problem
       ├── GPU power problem
       ├── GPU core problem
       └── sufficiently severe memory/controller problem
```

The command is therefore a **useful diagnostic boundary**, not a binary "GPU alive/dead" test.

For your RTX 3060 VRAM-repair work, I can next map **`M0–M7` physical GDDR6 chips → memory channels/address mapping → how a MATS failure points you to a specific chip**, which is probably the most useful next step.
