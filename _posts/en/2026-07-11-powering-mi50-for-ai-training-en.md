---
audio: false
generated: true
image: false
lang: en
layout: post
title: Powering MI50 for AI Training
translated: false
type: note
---

Question: Can a Corsair CX650F / 750W PSU power an AMD Radeon Instinct MI50 16GB for AI training?

Answer:

Yes, a **Corsair CX650F 650W** or **750W 80+ PSU** can power an AMD MI50, but there are a few important details.

AMD Radeon Instinct MI50 power requirements:

* **TDP:** ~300W
* **Power connector:** **1 × 8-pin PCIe power connector + 1 × 6-pin PCIe power connector** (not the same as RTX 4070)
* **Recommended PSU:** usually 650W+ depending on the rest of the system

The MI50 is a datacenter card, so it does not use the newer RTX 40-series style 12VHPWR connector.

Your PSU:

Corsair CX650F RGB

or the 750W version:

* PCIe 8-pin cables: yes
* Enough wattage: yes
* Quality: acceptable for a single MI50

A typical system:

```
CPU (Ryzen 7 / Intel i7)     80-150W
Motherboard + RAM            50W
SSD + fans                   20W
AMD MI50                     ~300W
----------------------------------
Total                       ~450-520W
```

So a good 650W PSU has enough headroom.

However, check the **PCIe power cables**:

MI50 needs:

```
PSU PCIe cable
       |
       +---- 8-pin PCIe -> MI50
       |
       +---- 6-pin PCIe -> MI50
```

Do **not** use:

```
SATA -> PCIe adapter  ❌
Molex -> PCIe adapter ❌
```

because the card can pull close to 300W continuously during AI workloads.

---

Your Xianyu MI50 listing:

> 16G HBM2 ECC, performance similar to RTX 3060, AI training, temperature 90°C

The description is mostly reasonable, but some notes:

### Performance

MI50:

* 16GB HBM2 ECC
* 10240 stream processors
* ~13.3 TFLOPS FP32
* ~1TB/s memory bandwidth

Compared with RTX 3060:

| GPU           | VRAM          | Memory bandwidth | FP32        |
| ------------- | ------------- | ---------------- | ----------- |
| RTX 3060 12GB | GDDR6 12GB    | 360 GB/s         | 12.7 TFLOPS |
| MI50          | HBM2 16GB ECC | ~1 TB/s          | 13.3 TFLOPS |

For **large model inference / training**, MI50 can actually feel better because:

* 16GB VRAM
* huge bandwidth
* ECC
* cheap used price

But software is the problem:

* CUDA ecosystem ❌
* PyTorch ROCm support ⚠️
* many AI packages assume NVIDIA

You need ROCm-compatible versions.

---

At 630 CNY, the MI50 is interesting:

```
RTX 4070:
12GB GDDR6X
CUDA
~200W

MI50:
16GB HBM2 ECC
~300W
ROCm
```

For your use case (local LLM experiments), the biggest advantage is:

**16GB VRAM + ECC at 630 CNY is extremely cheap.**

The main thing I would verify before buying:

```bash
lspci | grep VGA
rocm-smi
python -c "import torch; print(torch.cuda.is_available())"
```

after installing ROCm.

Also check cooling. MI50 cards often run hot because they were designed for server airflow. A desktop case with poor airflow can easily hit 90°C. For long training runs, add a strong side/front airflow or a blower setup.
