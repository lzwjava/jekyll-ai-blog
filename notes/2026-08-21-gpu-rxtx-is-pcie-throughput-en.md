---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU RX/TX is PCIe Throughput
translated: false
type: note
---

**Question:** Does "RX: 96.37 MiB/s" in NVIDIA GPU metrics refer to the RX/TX signals on the GPU's motherboard connector pins?

**Answer:**

No, it does not refer to physical RX/TX electrical signals on the PCIe connector pins. In NVIDIA GPU monitoring tools (like `nvidia-smi`, `nvtop`, or similar), **RX** and **TX** in the metrics context mean:

- **RX (Receive)** — data being received **by the GPU** over the PCIe bus (i.e., data transferred from system RAM → GPU VRAM)
- **TX (Transmit)** — data being sent **from the GPU** over the PCIe bus (i.e., data transferred from GPU VRAM → system RAM)

So `RX: 96.37 MiB/s` means the GPU is currently **receiving ~96 MB of data per second** through the PCIe interface — it's a **bandwidth/throughput metric**, not a reference to physical pin-level signals.

### Analogy to networking
The naming borrows from networking terminology (just like a NIC has RX/TX), but here the "channel" is the **PCIe bus**, not a physical RX/TX pin pair on a connector.

### PCIe physical pins, for contrast
The actual PCIe connector does have differential pairs (PERp/PERn for receive, PETp/PETn for transmit), but those are never exposed as labeled metrics — you'd only see those in hardware/signal-integrity documentation, not in GPU monitoring software.

---

**References:**
- [NVIDIA SMI Documentation](https://developer.nvidia.com/nvidia-system-management-interface)
- [PCIe Base Specification – Lane Signals](https://pcisig.com/specifications)
