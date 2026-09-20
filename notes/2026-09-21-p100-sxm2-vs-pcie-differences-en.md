---
audio: false
generated: true
image: false
lang: en
layout: post
title: P100 SXM2 vs PCIe Differences
translated: false
type: note
---

**Question:** What are the differences between the NVIDIA Tesla P100 SXM2 and its PCIe version?

**Answer:**

The Tesla P100 SXM2 and PCIe share the same GP100 die and CUDA core count (3,584), but differ in several important ways:

---

### 1. Form Factor & Installation
The SXM2 version uses a proprietary NVIDIA module that connects directly to the motherboard via an SXM2 socket, rather than fitting into a standard PCIe slot like a normal expansion card. This means SXM2 requires a dedicated compatible server platform (like NVIDIA DGX-1 or HGX boards), while PCIe cards drop into any standard server.

---

### 2. Compute Performance (Clock & FLOPS)
The PCIe P100 has slightly scaled-back performance compared to the SXM2 (NVLink) version:

| Metric | PCIe | SXM2 (NVLink) |
|---|---|---|
| Double-precision | 4.7 TFLOPs | 5.3 TFLOPs |
| Single-precision | 9.3 TFLOPs | 10.6 TFLOPs |
| Half-precision | 18.7 TFLOPs | 21.2 TFLOPs |

The boost clock is also lower — 1,303 MHz for PCIe vs. 1,480 MHz for SXM2.

---

### 3. Memory Bandwidth & Capacity
The 12 GB PCIe version uses a narrower 3072-bit HBM2 interface with 549 GB/s bandwidth, while the 16 GB PCIe and all SXM2 versions use a 4096-bit interface delivering up to 732 GB/s. So the 12 GB PCIe variant is at a notable memory bandwidth disadvantage.

---

### 4. GPU-to-GPU Interconnect (NVLink)
The SXM2 version supports NVLink with 160 GB/s of inter-GPU bandwidth, while the PCIe version has no NVLink and is limited to 32 GB/s PCIe bandwidth. This is the most critical difference for multi-GPU workloads.

---

### 5. TDP & Power Delivery
The SXM2 requires a 300 W power supply and draws power directly through the SXM2 socket — no external power cables needed. The PCIe version operates at a lower TDP, making it more suitable for standard server power budgets.

---

### 6. Cooling
Power delivery being handled by the SXM socket, combined with horizontal mounting, allows more efficient cooling mechanisms, enabling SXM-based GPUs to operate at a higher TDP than their PCIe counterparts.

---

### Summary Table

| Feature | P100 SXM2 | P100 PCIe |
|---|---|---|
| Form Factor | Proprietary SXM2 socket | Standard PCIe slot |
| Boost Clock | 1,480 MHz | 1,303 MHz |
| FP32 Performance | 10.6 TFLOPs | 9.3 TFLOPs |
| Memory | 16 GB HBM2 | 12 GB or 16 GB HBM2 |
| Memory Bandwidth | 732 GB/s | 549 GB/s (12 GB) / 732 GB/s (16 GB) |
| NVLink | 160 GB/s | None |
| TDP | 300 W | ~250 W |
| Server Compatibility | Requires NVLink/HGX platform | Any standard server |

**Bottom line:** Choose SXM2 for maximum performance and multi-GPU scaling (AI/HPC clusters). Choose PCIe for broader hardware compatibility and lower infrastructure cost.

---

**References:**
- [NVIDIA Developer Blog – P100 Specs](https://developer.nvidia.com/blog/?p=6535)
- [TechGage – PCIe vs NVLink P100](https://techgage.com/?p=37889)
- [Wikipedia – SXM Socket](https://en.wikipedia.org/wiki/SXM_(socket))
- [IT Creations – Tesla P100 SXM2](https://www.itcreations.com/nvidia-gpu/nvidia-tesla-p100-sxm2-gpu)
