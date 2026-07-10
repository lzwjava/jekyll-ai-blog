---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 PC Build Considerations
translated: false
type: note
---

Question: What motherboard does an AMD Instinct MI50 need? I bought one for 630 CNY and want to build a PC around it.

Answer:

For an **AMD Instinct MI50 (16 GB HBM2)**, the motherboard is actually **not the limiting factor**. The important requirements are:

* PCIe x16 slot (Gen3 or Gen4)
* UEFI BIOS
* Enough physical clearance (the MI50 is a dual-slot card)
* Adequate power supply
* Airflow, because it uses a **passive server heatsink**

The MI50 is designed for servers, so the biggest challenge is **cooling**, not motherboard compatibility.

## 1. Motherboard

Almost any modern ATX or mATX board works.

Examples:

* AMD B450
* AMD B550 (recommended)
* AMD X570
* Intel B660
* Intel Z690
* Intel B760
* Intel Z790

If you're building from scratch today, I'd recommend:

* Ryzen 5 5600
* B550 motherboard
* 32–64 GB DDR4

This is inexpensive and has excellent Linux support.

---

## 2. CPU

AI inference/training doesn't require an expensive CPU.

Good choices:

* Ryzen 5 5600
* Ryzen 7 5700X
* Ryzen 9 5900X (if you compile lots of software)

If buying used:

* Ryzen 3600 + B450
* Ryzen 5600 + B550

Both are great value.

---

## 3. PSU

The MI50 consumes around

* **~300 W TDP**

You'll want

* 750 W quality PSU minimum
* 850 W preferred

Examples

* Corsair RM750e
* Seasonic Focus GX-750
* MSI A750GL

---

## 4. Cooling (Most Important)

This is where many first-time MI50 builders run into trouble.

The MI50 has **no onboard fan**.

Server chassis provide very high airflow through the card.

In a desktop PC you need:

* a 120 mm fan blowing directly into the heatsink
* or 2×120 mm fans

Without airflow the GPU will quickly thermal throttle.

Many hobbyists 3D-print a fan shroud.

---

## 5. Power Connectors

The MI50 typically requires

* 2 × 8-pin PCIe power connectors

Check your exact model, but this is the common configuration.

---

## 6. RAM

I'd recommend

* 32 GB minimum
* 64 GB if training models

DDR4 is inexpensive now.

---

## 7. SSD

A fast NVMe SSD helps with datasets.

Recommended:

* 1–2 TB NVMe PCIe SSD

---

## 8. Operating System

Linux is strongly recommended.

Ubuntu 24.04 LTS works well.

You'll likely install:

```bash
ROCm
PyTorch ROCm
vLLM (limited support depending on version)
llama.cpp
SGLang (experimental)
```

---

## 9. ROCm Support

The MI50 uses the Vega 20 architecture (`gfx906`).

It is one of AMD's older datacenter GPUs, and many ROCm releases still support it, although newer releases are gradually dropping older architectures. If you encounter compatibility issues, using an earlier ROCm release (for example, ROCm 6.2 or similar) is often easier than the newest version.

The MI50 supports:

* FP32
* FP16
* BF16 (limited compared with newer CDNA GPUs)
* ECC memory
* 16 GB HBM2 (~1 TB/s memory bandwidth)

It remains a capable card for experimentation, small-model training, and inference.

---

## Suggested budget build

| Component   | Recommendation                   |
| ----------- | -------------------------------- |
| CPU         | Ryzen 5 5600                     |
| Motherboard | B550 mATX                        |
| RAM         | 64 GB DDR4-3200                  |
| SSD         | 1 TB NVMe                        |
| PSU         | 850 W 80+ Gold                   |
| GPU         | AMD Instinct MI50                |
| Cooling     | Two 120 mm fans aimed at the GPU |

This entire system can often be assembled from used parts for **around 2,000–3,000 CNY**, excluding the GPU.

For **630 CNY**, an MI50 is a very good deal. It offers much higher memory bandwidth than an RTX 3060 (HBM2 vs. GDDR6), although software compatibility is weaker because NVIDIA's CUDA ecosystem is more mature. If you're interested in ROCm, compiler work, or AMD GPU development, it's an excellent platform for learning.