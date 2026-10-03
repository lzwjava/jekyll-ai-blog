---
audio: false
generated: true
image: false
lang: en
layout: post
title: Generational GPU Comparison M40 vs 4070
translated: false
type: note
---

Question: Compare your two `nvidia-smi` snapshots — Tesla M40 vs RTX 4070.

Answer:

These are essentially two very different generations of NVIDIA GPU, and your snapshots show the expected behavior.

|                    |       **Tesla M40** |        **RTX 4070** |
| ------------------ | ------------------: | ------------------: |
| Architecture       |           Maxwell 2 |        Ada Lovelace |
| Compute capability |             **5.2** |             **8.9** |
| VRAM               | 11,520 MiB (~12 GB) | 12,282 MiB (~12 GB) |
| VRAM type          |               GDDR5 |               GDDR6 |
| Memory bandwidth   |           ~288 GB/s |           ~504 GB/s |
| CUDA cores         |               3,072 |               5,888 |
| FP32               |         ~7.0 TFLOPS |        ~29.1 TFLOPS |
| TDP                |               250 W |           200–215 W |
| Tensor Cores       |                   ❌ |                   ✅ |
| RT Cores           |                   ❌ |                   ✅ |
| NVENC              |    Older generation |          Much newer |
| Your temperature   |            **46°C** |            **40°C** |
| Your power         |            **70 W** |            **10 W** |
| Your workload      |      `llama-server` |       Desktop/GNOME |

### 1. Your M40 is actually doing real LLM work

This line is the important one:

```text
Tesla M40
Memory: 5144 MiB / 11520 MiB
Power:   70 W / 250 W

llama-server: 5137 MiB
```

So almost all of the ~5.1 GB VRAM allocation belongs to your `llama-server`.

And:

```text
GPU-Util: 0%
```

does **not** mean the model isn't loaded.

It means that at the exact instant `nvidia-smi` sampled the GPU, there was essentially no CUDA kernel executing.

For an idle llama.cpp server, this is normal:

```text
VRAM allocated
      ↓
model weights resident
      ↓
GPU utilization = 0% while waiting
      ↓
request arrives
      ↓
GPU utilization spikes
```

The **5.1 GB VRAM allocation** is much more interesting than the 0% utilization.

---

### 2. The 4070 snapshot is basically desktop idle

Your 4070 has:

```text
1180 MiB / 12282 MiB
10 W / 215 W
40°C
P8
```

The ~1.18 GB is mostly graphical desktop allocation:

```text
Xorg             757 MiB
GNOME Shell       41 MiB
Chrome/etc       ~310 MiB
```

So this is essentially:

```text
4070
 ├── Xorg
 ├── GNOME
 └── browser
```

No meaningful CUDA workload is running.

---

## 3. The really interesting comparison: M40 vs 4070 for LLMs

Your experiment demonstrates an important point.

The M40 has roughly the **same VRAM capacity** as the 4070:

```text
M40: 11.5 GiB
4070: 12.0 GiB
```

but the 4070 is vastly newer.

The rough raw FP32 difference is:

```text
4070 ≈ 29 TFLOPS
M40  ≈  7 TFLOPS
```

so about **4×** raw FP32 throughput.

But for modern LLM inference the difference can be even more significant because the 4070 has:

```text
Ada
 ├── Tensor Cores
 ├── much newer CUDA architecture
 ├── much faster FP16/BF16/TF32 paths
 └── much newer memory subsystem
```

while the M40 is:

```text
Maxwell
 └── no Tensor Cores
```

That's why the M40 is a fascinating **cheap VRAM/LLM experiment card**, but the 4070 is a vastly more capable compute GPU.

---

## 4. One particularly interesting thing about your M40

Your M40 is running:

```text
NVIDIA driver 580.178.04
CUDA 13.0
```

and `nvidia-smi` recognizes it normally.

That's useful because the M40 is a **compute capability 5.2** GPU and is quite old.

So your current setup demonstrates:

```text
Modern Linux
    ↓
580 driver
    ↓
CUDA 13 runtime/driver
    ↓
Maxwell M40
    ↓
llama.cpp / llama-server
    ↓
~5.1 GB model allocation
```

That's a pretty good old-GPU LLM laboratory.

The caveat is that **CUDA toolkit/compiler support and runtime driver support are different things**. A current NVIDIA driver recognizing the card doesn't mean every modern CUDA kernel/toolchain will still support `sm_52`.

---

### Bottom line

Your two screenshots are basically:

```text
M40:
12 GB VRAM
250 W
46°C
70 W
5.1 GB occupied
└── llama-server

4070:
12 GB VRAM
215 W
40°C
10 W
1.18 GB occupied
└── desktop
```

So **the M40 is currently being used as your LLM GPU**, while the **4070 is currently just driving your Linux desktop**.

And that's actually a useful setup for experimentation: you can run the old Maxwell card as a dedicated inference/compute device while leaving the 4070 available for newer CUDA/LLM workloads.
