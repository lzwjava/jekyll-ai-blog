---
audio: false
generated: true
image: false
lang: en
layout: post
title: SXM Meaning in NVIDIA H200
translated: false
type: note
---

Question: What does **SXM** mean in NVIDIA H200?

Answer:

**SXM = SXM form factor (Socket eXchange Module)**. In NVIDIA GPU products, it refers to the **server module packaging format**, not the GPU architecture.

For the NVIDIA H200 Tensor Core GPU, you usually see two physical versions:

1. **H200 SXM**

   * Designed for large AI servers
   * Uses NVIDIA's SXM connector
   * Connects through NVIDIA NVLink directly between GPUs
   * Much higher bandwidth and power envelope

2. **H200 PCIe**

   * Standard PCIe card (like a normal GPU expansion card)
   * Easier to put into existing servers
   * Lower inter-GPU communication bandwidth

The "SXM" module looks more like a dense accelerator board that plugs into a custom NVIDIA baseboard:

```
HGX H200 system

CPU
 |
PCIe / NVLink
 |
+----------------+
| H200 SXM       |
| GPU module     |
+----------------+
 |
NVLink fabric
 |
+----------------+
| H200 SXM       |
| GPU module     |
+----------------+
```

For AI training, SXM is the serious version because:

* Higher power:

  * H200 SXM: ~700W
  * H200 PCIe: ~350W

* More memory bandwidth:

  * H200 SXM: ~4.8 TB/s HBM3e bandwidth
  * PCIe version is more limited

* Better GPU-to-GPU scaling:

  * SXM uses NVLink/NVSwitch
  * PCIe relies more on PCIe lanes

So when NVIDIA engineers say:

> "SM120"

they mean the **GPU compute architecture / streaming multiprocessor generation** (Blackwell SM version).

When they say:

> "H200 SXM"

they mean:

```
H200        = GPU product
SXM         = physical module/package
```

Similar examples:

```
A100 SXM4
A100 PCIe

H100 SXM5
H100 PCIe

H200 SXM
H200 PCIe
```

For LLM training clusters (GPT-scale), almost all serious systems use **SXM + NVLink + NVSwitch**, because communication between GPUs becomes the bottleneck.
