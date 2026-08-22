---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPUs with Firmware-Only Differentiation
translated: false
type: note
---

**Question:** What other GPUs use firmware-only differentiation similar to NVIDIA's CMP 170HX, and could similar methods apply to them?**Answer:** This is a very broad industry pattern, not unique to NVIDIA. Here's a structured breakdown:

---

### NVIDIA GPUs (Most Directly Applicable)

The paper's exploit targets NVIDIA's **Falcon secure coprocessor** — a component shared across many NVIDIA GPU generations. Any card using the same Falcon HS firmware architecture is potentially in scope:

- **CMP 170HX / A100 (GA100)** — the paper's direct target; community tools are now packaging the exploit into installable scripts
- **Other CMP mining cards** (e.g., CMP 90HX, 50HX) — same family of firmware-gated differentiation
- **A100 Drive / Orin variants** — there were also A100 Drive models whose pricing nearly doubled after people figured out how to use them in desktops, suggesting similar firmware-only gating
- **H100 / H200 / Hopper family** — use the same Falcon+NV-RISCV coprocessor architecture; whether the specific HS bug exists there is unconfirmed, but the structural vulnerability class (writable canary reference word in flat firmware) is a **toolchain default**, not a one-off mistake

---

### AMD GPUs (Historically Documented, Lower Barrier)

AMD has a long, well-documented history of firmware-only differentiation:

- The unlocking process works with some "Pro" SKU graphics cards utilizing AMD's Fiji, Hawaii, or Tonga GPUs (R9 Fury, R9 390/290, R9 380/285), where AMD used a cut-down version with some compute units disabled through firmware modifications or permanent laser-cutting. AMD's method is simpler — just flashing a modded VBIOS, no secure coprocessor exploit needed.
- A firmware update for the Radeon RX 460 can unlock additional stream processors and TMUs that AMD disabled at the factory — bumping from 896 to 1,024 shaders.
- Creating new SKUs from the same silicon by locking features has been common practice in the industry since at least the Radeon 9500 in 2002.

AMD's older cards used BIOS-level locking (easier to bypass), not a hardened secure coprocessor like NVIDIA's Falcon. Newer AMD Instinct cards likely use more robust firmware security.

---

### The Key Distinction: What Makes NVIDIA's Case Unique

| Factor | AMD (older) | NVIDIA (Falcon-based) |
|---|---|---|
| Lock mechanism | VBIOS flash | Signed HS firmware + fuse shadow registers |
| Bypass method | Modded VBIOS flash | Secure coprocessor exploit required |
| Difficulty | Low (community tools) | High (required original paper's research) |
| Applies if | Firmware-disabled | Firmware-disabled AND Falcon bug present |

---

### What Would Need to Be True for the Method to Apply Elsewhere

The paper's specific technique (canary reference-word overwrite via unbounded DMA) requires:

1. A **secure coprocessor** that enforces fuse overrides (NVIDIA Falcon / NV-RISCV)
2. The **specific regression bug** in the signed booter (confirmed absent in older firmware, present in 580-era open-kernel-modules booter)
3. Features gated by **firmware-read fuses**, not physical datapaths

The paper explicitly notes that higher PCIe generations remain blocked by a fuse burned into the silicon at manufacturing time, which software cannot bypass — so features backed by true physical gates are immune regardless of the exploit.

---

**Bottom line:** The *structural lesson* (firmware-only fuse gating is weaker than physical gating) applies industry-wide to NVIDIA, AMD, and Intel. But the *specific exploit* from the paper is currently tied to NVIDIA's Falcon HS firmware regression in the open-kernel-modules era booter.
