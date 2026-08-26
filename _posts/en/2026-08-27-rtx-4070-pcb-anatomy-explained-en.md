---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 PCB Anatomy Explained
translated: false
type: note
---

**Question:** What makes an RTX 4070 GPU special, and what components are physically on the circuit board/card?

**Answer:**

---

## 🧠 What Makes the RTX 4070 Special

The RTX 4070 is built on NVIDIA's **Ada Lovelace** architecture (AD104 die), fabricated on **TSMC's 4N process node** (effectively ~5nm class). Key highlights:

- **5888 CUDA Cores** — the parallel processors that do most GPU work
- **36 RT Cores** (ray tracing, one per SM) — dedicated hardware for lighting/shadow simulation
- **184 Tensor Cores** — AI/matrix math, powers DLSS 3 upscaling
- **12GB GDDR6X VRAM** on a **192-bit memory bus**
- **200W TDP** — relatively power-efficient for its performance tier
- **PCIe 4.0 x16** interface

---

## 🔩 What's Physically ON the Card (PCB Components)

### 🟢 The Main Chip — GPU Die

- The large square chip in the center, covered by a metal heat spreader
- Contains billions of transistors (AD104 = ~35.8 billion)
- Bonded to the PCB via **solder bumps (flip-chip)**

### 🔵 VRAM — Video Memory Chips

- Multiple **GDDR6X memory chips** surrounding the GPU die (usually 6 chips for 12GB)
- Made by Micron, very fast — up to 21 Gbps per pin
- Arranged around the GPU in a ring/halo pattern

### ⚡ VRM — Voltage Regulator Module

- A cluster of components that **convert PCIe/power connector voltage (12V) to the precise, lower voltages** the GPU needs (often ~0.8–1.1V)
- Made up of:
  - **MOSFETs / DrMOS chips** — the switching transistors (appear as small black chips in rows)
  - **Inductors (chokes)** — chunky coils that smooth out current, look like small metal squares/cylinders
  - **Capacitors (bulk caps)** — cylindrical or flat SMD caps that buffer power and filter noise
  - **PWM Controller IC** — a small chip that tells the VRMs how fast to switch

### 🟡 Capacitors (Several Types)

| Type | Location | Job |
| --- | --- | --- |
| **Bulk electrolytic caps** | Near power input | Hold large charge reserves |
| **MLCC (ceramic SMD caps)** | Everywhere on PCB | High-frequency noise filtering |
| **POSCAPs / SP-CAPs** | Near GPU/VRAM | Decoupling, reduce voltage ripple |

### 🔌 Power Connectors

- RTX 4070 uses the **16-pin PCIe 5.0 connector** (or adapter from 2× 8-pin)
- Feeds power directly to the VRM section

### 🖥️ Display Output Circuitry

- **DisplayPort 1.4a** and **HDMI 2.1** controller chips near the output ports
- ESD protection diodes, signal filtering caps around ports

### 🧩 PCIe Edge Connector

- The gold-fingered edge that slots into your motherboard
- Carries both data (x16 PCIe lanes) and some power

### 🌡️ Thermal Sensors

- Small SMD components scattered around the board; report temp to the GPU die and fan controller

### 🎮 BIOS Chip

- A tiny flash memory chip (usually 8-pin SOP package) storing the GPU firmware/BIOS

### 🔒 Other ICs

- **Clock generator / PLL** — ensures precise timing signals
- **Power sequencing ICs** — controls which voltages turn on in what order at boot

---

## How It All Flows Together

```
Wall Power → PSU → 12V Rail
                      ↓
              PCIe connector + slot
                      ↓
              VRM (MOSFETs + inductors + caps)
                      ↓
         GPU Die ←→ GDDR6X VRAM
                      ↓
           Display ICs → your monitor
```

---

**References:**

- [NVIDIA RTX 4070 Specs — NVIDIA Official](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070/)
- [GPU PCB Anatomy — NVIDIA A100 Case Study (AnandTech style)](https://images.nvidia.com/aem-dam/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf)
- [What is a VRM? — Hardware Explained](https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html)
- [GDDR6X Memory — Micron](https://www.micron.com/products/graphics-memory/gddr6x)
