---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrading Deep Learning Workstation with AMD
translated: false
type: note
---

Question: How can I get an AMD Radeon Pro 16GB HBM2 TDP GPU for a deep learning workstation, considering I already have a high-end Intel i9 system with an RTX 4070? Should I modify my current build or make a new one?

Answer:

Since your goal is to have a **deep learning workstation using AMD’s open-source stack** (ROCm), here’s a thorough breakdown of your options:

---

### 1. Understanding the Current Setup

Your current build:

* CPU: Intel i9-13900KF
* GPU: RTX 4070 (NVIDIA, CUDA, proprietary)
* Motherboard: MSI B760M (DDR5, PCIe 5.0, LGA 1700)
* RAM: 64GB DDR5
* Storage: 1TB NVMe + 2TB HDD
* PSU: 750W

**Observations for AMD deep learning:**

* ROCm (AMD’s deep learning software stack) has **limited Intel CPU support**; it works best with AMD CPUs, although some GPUs work with Intel motherboards.
* AMD Radeon Pro GPUs with **HBM2 memory** (like the W6800, MI200 series, or Pro W6600/W6800 16GB) are ideal for memory-intensive deep learning tasks.
* Your motherboard supports PCIe 5.0, which is fine for modern AMD GPUs.

---

### 2. Choosing the Right AMD GPU

For deep learning, you want **high VRAM and ROCm support**:

* **AMD Radeon Pro W6800** – 32GB GDDR6, workstation-focused, ROCm supported.
* **AMD Radeon Pro W6600/W6700** – 8–32GB VRAM, lower cost, but may limit large models.
* **AMD MI200 / MI250** – 64–128GB HBM2, very expensive, mostly for server-grade AI.

**16GB HBM2 options** are rare in consumer/desktop. The closest is **Radeon Pro VII** (16GB HBM2), which is workstation-ready and ROCm compatible.

---

### 3. Modifying Existing Build vs New Build

#### Option A: Swap GPU in Current Build

* Your motherboard has PCIe slots, likely compatible with Radeon Pro.
* **Pros:** Save money, keep existing CPU/RAM/storage.
* **Cons:**

  * Intel CPU may limit ROCm performance slightly.
  * Power supply: Radeon Pro VII TDP ~300W. Your 750W PSU is sufficient.
  * Case size: check GPU length—Radeon Pro VII is ~267mm, your case is “mini” style, may be tight.

#### Option B: New AMD-centric Workstation

* Use an **AMD Threadripper or Ryzen 7000 CPU**, which ROCm supports better.
* Pair with **Radeon Pro VII** (16GB HBM2) or **W6800 32GB** if you want headroom.
* **Pros:** Best performance, fully open-source stack.
* **Cons:** Expensive, need to rebuild.

---

### 4. Recommendations

1. **If budget is tight:**

   * Keep your Intel i9 build.
   * Replace RTX 4070 with **Radeon Pro VII 16GB HBM2**.
   * Check your case for clearance.
   * Install ROCm drivers on Linux (Ubuntu recommended).

2. **If maximizing ROCm & AMD ecosystem:**

   * Build new workstation with AMD CPU (e.g., Ryzen 9 7950X or Threadripper).
   * Add Radeon Pro VII or W6800.
   * Keep your existing RAM and storage if compatible.

3. **Alternative option (multi-GPU hybrid):**

   * Keep RTX 4070 for gaming / CUDA experiments.
   * Add Radeon Pro VII for AMD deep learning.
   * Requires a bigger case and PSU upgrade (~1000W recommended).

---

### 5. Practical Notes

* AMD deep learning ecosystem (ROCm + PyTorch/TensorFlow) is **fully open-source**, unlike CUDA.
* Some large models may need **>=24GB VRAM**, so 16GB is OK but not ideal for huge neural nets.
* Ensure **Linux OS** for ROCm; Windows support is limited.

---

**Summary Table**

| Option                  | Cost/Complexity | Performance | Pros             | Cons                     |
| ----------------------- | --------------- | ----------- | ---------------- | ------------------------ |
| Swap GPU in current PC  | Medium          | Good        | Saves money      | Intel CPU may limit ROCm |
| New AMD-centric build   | High            | Best        | Optimal ROCm     | Expensive, rebuild       |
| Hybrid GPU (NVIDIA+AMD) | High            | Flexible    | Both CUDA & ROCm | PSU/case upgrade needed  |

---

References:

* [ROCm Official Supported GPUs](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation-Guide.html#supported-gpus)
* [AMD Radeon Pro VII Specs](https://www.amd.com/en/products/professional-graphics/radeon-pro-vii)
* [ROCm for Intel CPUs](https://rocmdocs.amd.com/en/latest/Installation_Guide/Intel-CPU.html)

---

If you want, I can **design a concrete plan for your current case** with a Radeon Pro VII or W6800, including PSU, case, and Linux setup for deep learning. This would give you an exact parts and setup guide. Do you want me to do that?