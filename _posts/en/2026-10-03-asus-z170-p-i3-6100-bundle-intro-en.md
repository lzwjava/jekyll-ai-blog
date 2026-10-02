---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS Z170-P i3-6100 Bundle Intro
translated: false
type: note
---

Question: Intro to this ASUS Z170-P + i3-6100 motherboard bundle.

Answer:

ASUS Z170-P is a mid-range Intel Z170 chipset motherboard from the Skylake era (2015–2016). This bundle includes an Intel Core i3-6100 CPU.

![Image](https://images.openai.com/static-rsc-4/iplQ9I4jlH7ekXSf8-dpMWsjazySl_d-WO8fjh7DthAeuuYYSQ88D8zFkJ9HsZ6rr-ll5hPsmIvBtOWWldPDGJy_NvEcmNXO2n0z5HMoQ6H5Yn4b6aAe4lbvKrQQQkOzt9aAseU6GWHjN1wdlhwVWqaD4V139ygTeGXrQw8ugX4Q1m7hcBeDbBO2ytVoz2Tq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dwS6bprg4lsBQb3iiVU41YhEwbR3BGn5l7Eyi2WGP3sNc1y7HY7sMXfxsF2ECG8YNvUPQjyXEvB8zPjshDSsCV3TY5DuqME0VpHqIuDFcKhMi-L-p1tn1jCg1tmTePidAMengO1xWRScNBdp35y-Qu67b-m9O9xsyO8CHvpVUNyh4rZCWN4qcO_Op7GfszJp?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3aymNS2M6gxCn0p_opGKTidq3j8XsO3u7ObHdgC0WGEtHbBq7-SEtRP_jQ5v_BYxkeSlP15naT02mA1uvoLQt-8nRNOxWc_v392h_b_wooZBZsHQxLo7nt2Gkmq_6BgA-pTcRk8WCRPxtsPjYNq-dR5bd1Od2qrE2-1IXC0JsGHhMOyizL47MdBbB6-tGOWJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lNnIOdqzs-5UPbZTr9pw_MaeW9GOpAaYCEnHGWBcdZGF_iEwdG9RI_QjlRyDpK0Bjx9ApdjPqJpnjguRcDEfwr7WkYVSqJykohU1UzK3uUHX-NbNB6ZCNYUIN0uB-hDI-zb1nnbuMRiuPZK37VF8umBwYTFKRqMTsdVLDBh9hsfCaddRipj3ZvUtuklwuvLM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Of0CX7AgcZ0H1bBZci6gTf6Mc_cE3u4l5b3yRZyN1km-ZXhhMXyYQ1UUrX7DYi9tP3QCXX3TKlOROVeP70ghd12lP9kn4L_NB-e5Y-bD7L5BPn9h4XrAJViWOwLw67eRuJWR23x335ZWIB1bPjbWLNoBZ--NWnXN6QNmFXLv5bVpUBPAWnpffKw8pcXduSro?purpose=fullsize)

### 1. Motherboard: ASUS Z170-P

Key specs:

* **Socket:** LGA 1151
* **Chipset:** Intel Z170
* **CPU support:**

  * 6th Gen Intel Core (Skylake) officially
  * Some 7th Gen Kaby Lake CPUs after BIOS update
* **Memory:**

  * 4 × DDR4 DIMM slots
  * Usually up to 64GB DDR4
  * Supports XMP memory overclocking
* **Expansion:**

  * 1 × PCIe 3.0 x16 (GPU slot)
  * Additional PCIe slots for cards
* **Storage:**

  * M.2 slot (PCIe 3.0 x4 NVMe support)
  * SATA 6Gb/s ports
* **Display outputs:**

  * HDMI
  * DVI
  * VGA
    (only useful when using Intel integrated graphics)
* **Network:**

  * Gigabit Ethernet
* **USB:**

  * USB 3.0 support

The Z170 chipset is actually a higher-end chipset compared with H110/B150 because it supports:

* CPU overclocking with unlocked "K" CPUs
* Memory overclocking
* More PCIe lanes

The Z170-P itself is a budget Z170 board, not an enthusiast board like ASUS Z170 Pro Gaming, but still a solid platform.

---

### 2. CPU: Intel Core i3-6100

Specs:

| Item         | Specification         |
| ------------ | --------------------- |
| Architecture | Skylake               |
| Cores        | 2                     |
| Threads      | 4                     |
| Base clock   | 3.7 GHz               |
| TDP          | 51W                   |
| iGPU         | Intel HD Graphics 530 |
| Socket       | LGA1151               |

Performance today:

* Office / browsing: OK
* Linux server: OK
* NAS / router: OK
* Light coding: OK
* Older games: OK
* Modern AI workloads: Not useful

The CPU is the weak point. The motherboard can support much stronger CPUs:

Possible upgrades:

* i5-6500 / i5-6600
* i7-6700
* i7-7700 (with BIOS update)
* i7-6700K / i7-7700K (overclocking depends on board BIOS)

---

### 3. For GPU experiments / AI lab

Since you often look at old GPUs, this platform is interesting:

Advantages:

✅ PCIe 3.0 x16
✅ DDR4 platform
✅ M.2 NVMe
✅ Cheap replacement parts
✅ Supports older NVIDIA cards

But limitations:

* Only 16 PCIe lanes from CPU
* No PCIe 4.0/5.0
* No Resizable BAR officially (ReBarUEFI can sometimes help)
* i3-6100 is weak for GPU compute host tasks

For GPUs like:

* GTX 1060/1070/1080 → fine
* RTX 3060 → fine
* RTX 3090 → works, but CPU bottleneck
* Tesla P100/M40 → possible, but BIOS/PCI resource issues may appear

---

### 4. Used market value (China second-hand)

Approximate 2026 value:

* ASUS Z170-P motherboard: ~150–250 CNY
* i3-6100 CPU: ~50–100 CNY

Bundle reasonable price:

* **200–300 CNY:** good deal
* **300–400 CNY:** acceptable if clean/tested
* **>400 CNY:** not attractive

For a GPU repair/test bench, this platform is actually more useful than a cheap H110 because Z170 gives more BIOS options and PCIe flexibility.

Compared with the MSI Z170A SLI PLUS you asked about earlier, ASUS Z170-P is a lower-end board:

* Z170-P: basic Z170, fewer power phases, fewer expansion features
* Z170A SLI PLUS: better VRM, more PCIe slots, more suitable for multi-GPU experiments

For a **GPU repair bench + old Tesla/Pascal GPU testing**, I would prefer the Z170A SLI PLUS if the price difference is small. For a cheap daily test machine, this ASUS bundle is fine.
