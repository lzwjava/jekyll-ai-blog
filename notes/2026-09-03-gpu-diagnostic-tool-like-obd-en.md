---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Diagnostic Tool Like OBD
translated: false
type: note
---

Question: Is there a PCIe diagnostic tool for NVIDIA GPUs that works like a car OBD scanner—plug it in, and it tells you which power rail/component is broken?

Answer: **Yes, but not as a single magic “GPU OBD scanner.”** The closest setup is a combination of PCIe POST diagnostics, GPU-specific diagnostic software, and board-level measurement tools.

The important distinction is:

```text
Car:
OBD port
  ↓
ECU diagnostics
  ↓
error code: P0301, etc.
  ↓
fairly high-level fault location


GPU:
PCIe connector
  ↓
PCIe bus enumeration
  ↓
GPU firmware / driver
  ↓
software diagnostics
  ↓
BUT for board-level faults:
multimeter + oscilloscope + current injection
  ↓
VRM / MOSFET / controller / GPU / memory diagnosis
```

### 1. The closest thing: PCIe POST diagnostic card

You can buy a **PCIe diagnostic / POST analyzer**.

It plugs into a motherboard PCIe slot and can show things such as:

```text
PCIe link training
Bus / device / function
PCIe generation
link width
configuration-space transactions
error status
completion errors
AER errors
```

For example, if the NVIDIA card isn't even electrically establishing a PCIe link:

```text
Motherboard
    │
    ├── PCIe slot
    │
    └── GPU
          │
          X  ← no PCIe link
```

a PCIe analyzer can tell you much more than simply "GPU doesn't work."

But it generally **cannot say**:

```text
❌ APW8720 pin 6 broken
❌ GPU core VRM MOSFET Q23 bad
❌ 1.8V rail missing
```

because PCIe is downstream of the GPU's power-management circuitry.

---

### 2. For an NVIDIA GPU, `nvidia-smi` is already a kind of OBD scanner

If the card gets far enough to initialize:

```bash
lspci -nn | grep -i nvidia
```

then:

```bash
nvidia-smi
```

and:

```bash
sudo lspci -vv -s <GPU_BDF>
```

can tell you a surprising amount.

For example:

```bash
lspci -nn
```

might show:

```text
01:00.0 VGA compatible controller:
NVIDIA ...
```

That means:

```text
PCIe physical connection
        ↓
PCIe link
        ↓
configuration space
        ↓
device enumeration
```

is at least sufficiently alive for the motherboard to identify the device.

Then:

```bash
sudo lspci -vv -s 01:00.0
```

can expose PCIe link state, negotiated width/speed, AER information, etc.

This gives you a useful diagnostic hierarchy:

```text
                         GPU
                          │
                ┌─────────┴─────────┐
                │                   │
             Power               PCIe
                │                   │
          VRM / rails          link training
                │                   │
          GPU initialization   enumeration
                │                   │
                └─────────┬─────────┘
                          │
                       driver
                          │
                     nvidia-smi
```

---

### 3. But what you really want for GPU repair is a **GPU board diagnostic platform**

For the kind of repair you're experimenting with, I'd build a bench like this:

```text
                   ┌─────────────────┐
                   │ Linux diagnostic│
                   │ workstation     │
                   └────────┬────────┘
                            │ PCIe
                            ▼
                     ┌─────────────┐
                     │ GPU under   │
                     │ test        │
                     └─────────────┘
                       │   │   │
             ┌─────────┘   │   └──────────┐
             ▼              ▼              ▼
          12V input      VRM rails      PCIe
             │              │              │
        current meter    multimeter    PCIe analyzer
                            │
                       oscilloscope
```

Then you can classify a dead GPU very quickly.

For example:

### Case A — completely dead

```text
Plug GPU in

12V = 0V
fans = 0
PCIe = nothing
```

Look at:

```text
PCIe 12V
8-pin 12V
input fuse
protection MOSFET
5V / 3.3V auxiliary rails
PWM controller enable
```

---

### Case B — input power exists, but no secondary rails

```text
12V = OK
PCIe enumeration = NO
GPU core = 0V
memory rail = 0V
```

This points toward:

```text
power sequencing
        ↓
5V/3.3V auxiliary regulator
        ↓
PWM controller
        ↓
EN / PGOOD
        ↓
VRM
```

This is where your **APW8720 / V5F20** investigation becomes relevant.

---

### Case C — GPU appears in `lspci`, but driver fails

```bash
lspci
    ↓
NVIDIA device found
    ↓
nvidia-smi
    ↓
failure
```

Now you're in a completely different diagnostic layer.

Potentially:

```text
VBIOS
GPU initialization
VRAM
PCIe
driver
GPU silicon
power instability
```

You can inspect:

```bash
sudo dmesg | grep -iE 'nvrm|nvidia|pcie|aer'
```

and:

```bash
sudo lspci -vv -s 01:00.0
```

---

### Case D — GPU works but crashes under load

This is where software alone becomes insufficient.

For example:

```text
idle:

12V ─────────────── OK
1.8V ─────────────── OK
0.9V ─────────────── OK

load:

12V ─────────────── OK
1.8V ─────────────── OK
0.9V ────╲___/────── unstable
```

Now an oscilloscope is much more useful than a PCIe analyzer.

You can correlate:

```text
GPU load
   ↓
VRM current
   ↓
Vcore ripple
   ↓
GPU crash
```

---

## The really interesting tool: PCIe protocol analyzer

There are professional tools that go much further than a cheap POST card.

They can sit between:

```text
CPU / motherboard
       │
       ▼
PCIe analyzer
       │
       ▼
GPU
```

and capture PCIe transactions:

```text
LTSSM
link training
TS1 / TS2
configuration transactions
TLP
DLLP
AER
retries
completion errors
link speed
lane problems
```

These are basically the **OBD scanner equivalent for the PCIe protocol layer**.

The problem is price: professional PCIe analyzers can cost **thousands to tens of thousands of dollars**, so they're generally overkill for repairing cheap second-hand GPUs.

---

## What I'd buy for your GPU-repair bench

I wouldn't start with an expensive PCIe analyzer.

I'd prioritize:

```text
1. Good multimeter
2. Bench PSU with current display
3. Oscilloscope
4. Thermal camera
5. PCIe POST/diagnostic card
6. Cheap known-good motherboard
7. GPU test fixture/riser
8. Linux diagnostic machine
```

Then your workflow becomes:

```bash
# Layer 1
lspci

# Layer 2
sudo lspci -vv -s 01:00.0

# Layer 3
nvidia-smi

# Layer 4
dmesg | grep -iE 'nvrm|nvidia|pcie|aer'
```

while physically measuring:

```text
12V
3.3V
5V
1.8V
memory rail
GPU Vcore
VRM EN
VRM PGOOD
```

That is much closer to an **automotive diagnostic workflow**, except you're combining digital bus diagnostics with analog power-rail diagnosis.

And importantly: **PCIe diagnostic equipment can tell you that the GPU isn't communicating; it usually cannot tell you which VRM component caused that condition.** For that last 10 cm of the fault tree, you still need the schematic/boardview + multimeter + oscilloscope.

If you want, I can also map out a **“dead NVIDIA GPU → 10-minute diagnostic flowchart”**, starting from **“plugged into PCIe, fan doesn't spin”** and ending at **which rail/chip to probe next**.
