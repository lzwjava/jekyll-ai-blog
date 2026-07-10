---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCIe 4.0 vs 3.0 Bandwidth
translated: false
type: note
---

Question: PCIe 4.0 vs PCIe 3.0 comparison

Answer:

PCIe (Peripheral Component Interconnect Express) is the high-speed bus connecting CPU ↔ GPU, NVMe SSD, network cards, etc.

The main difference is **bandwidth per lane**.

| Version  | Year | Transfer rate per lane | Effective bandwidth per lane | x16 slot bandwidth |
| -------- | ---- | ---------------------: | ---------------------------: | -----------------: |
| PCIe 3.0 | 2010 |                 8 GT/s |                    ~985 MB/s |         ~15.8 GB/s |
| PCIe 4.0 | 2017 |                16 GT/s |                   ~1.97 GB/s |         ~31.5 GB/s |
| PCIe 5.0 | 2019 |                32 GT/s |                   ~3.94 GB/s |           ~63 GB/s |

PCIe 4.0 is basically **2× PCIe 3.0 bandwidth**.

---

### GPU example: RTX 4070

RTX 4070 supports PCIe 4.0 x16 electrically, but many modern GPUs do not saturate PCIe 4.0.

Typical:

```
CPU
 |
PCIe 4.0 x16
 |
RTX 4070
 |
GPU VRAM
```

For normal gaming:

* PCIe 3.0 x16 → almost no difference
* PCIe 4.0 x16 → slightly better
* PCIe 4.0 x8 → still usually fine

Because once data is loaded into VRAM, the GPU mostly works internally.

---

### AI training / LLM case

For your use case (PyTorch training, LLM inference):

The important part is **GPU VRAM bandwidth**, not PCIe.

Example:

RTX 4070:

```
GDDR6X VRAM bandwidth:
~504 GB/s

PCIe 4.0 x16:
~32 GB/s
```

The GPU memory is ~15× faster than PCIe.

During training:

```
GPU:
  load tensors
  compute matmul
  update weights

VRAM <----> CUDA cores
```

PCIe is mostly used for:

* loading batches
* CPU ↔ GPU transfers
* multi-GPU communication (unless NVLink)

---

### AMD MI50 case

Your MI50 is interesting:

AMD Radeon Instinct MI50

It supports:

* PCIe 4.0 x16
* 16GB HBM2
* ~1 TB/s memory bandwidth

But if you put it into a PCIe 3.0 motherboard:

```
MI50 PCIe 4.0 x16
        |
        ↓
Motherboard PCIe 3.0 x16

Result:
PCIe bandwidth halves
```

You get:

```
PCIe 4.0 x16:
~31.5 GB/s

PCIe 3.0 x16:
~15.8 GB/s
```

However, the HBM2 bandwidth remains:

```
HBM2:
~1 TB/s
```

so compute workloads are usually still fine.

---

### For your MSI B760M + MI50 setup

Your board:

* Intel B760 chipset
* CPU PCIe 4.0/5.0 depending on slot
* GPU slot likely PCIe 4.0 x16

So MI50 can run at:

```
MI50
 |
PCIe 4.0 x16
 |
CPU
```

No issue.

The bigger problems with MI50 are:

1. ROCm compatibility
2. power connector
3. cooling
4. driver support

not PCIe.

---

A simple mental model:

```
PCIe = highway from CPU to GPU

VRAM/HBM = GPU's local warehouse

GPU compute = factory
```

Making the highway wider helps only when trucks are constantly moving between CPU and GPU. For LLM training, you mostly want a bigger/faster warehouse (VRAM + memory bandwidth). That's why an old MI50 with HBM2 can still be interesting in 2026.
