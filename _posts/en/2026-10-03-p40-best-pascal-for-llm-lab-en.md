---
audio: false
generated: true
image: false
lang: en
layout: post
title: "P40: Best Pascal for LLM Lab"
translated: false
type: note
---

Question: **How good is the Tesla P40, especially compared with M40 and P100 for your LLM/GPU lab?**

Answer: **P40 24GB is probably the most interesting Pascal card for your use case.** It is essentially the **24GB successor to the M40**, designed specifically for inference. NVIDIA specifies 3,840 CUDA cores, 24GB GDDR5, 346 GB/s bandwidth, 12 TFLOPS FP32, and 250W. ([NVIDIA][1])

### P40 in one picture

```text
Tesla M40
  Maxwell
  3,072 CUDA
  24GB GDDR5
  288 GB/s
  ~7 TFLOPS FP32
  CC 5.2
       ↓
Tesla P40
  Pascal
  3,840 CUDA
  24GB GDDR5
  346 GB/s
  12 TFLOPS FP32
  CC 6.1
       ↓
Tesla P100
  Pascal
  3,584 CUDA
  16GB HBM2
  732 GB/s
  9.3 TFLOPS FP32
  CC 6.0
```

The P40's **24GB capacity is the big attraction**. NVIDIA explicitly positioned it as an inference accelerator, with INT8 support and 47 TOPS INT8. ([NVIDIA][1])

### P40 vs P100

This is an interesting tradeoff:

|                   |           P40 |      P100 PCIe |
| ----------------- | ------------: | -------------: |
| Architecture      |        Pascal |         Pascal |
| CUDA cores        |     **3,840** |          3,584 |
| VRAM              |      **24GB** |           16GB |
| Memory            |         GDDR5 |       **HBM2** |
| Bandwidth         |      346 GB/s |   **732 GB/s** |
| FP32              | **12 TFLOPS** |     9.3 TFLOPS |
| FP64              |  ~0.37 TFLOPS | **4.7 TFLOPS** |
| CC                |           6.1 |            6.0 |
| TDP               |          250W |           250W |
| Intended workload | **Inference** |   HPC/training |

So:

```text
LLM where model fits in 16GB
        → P100's 732 GB/s is very attractive

LLM where you need 20–24GB
        → P40 wins simply because P100 cannot fit it

HPC / FP64
        → P100

cheap 24GB LLM inference
        → P40
```

The P100's HBM2 bandwidth is more than **2×** the P40's GDDR5 bandwidth, while the P40 has 50% more VRAM. The published specifications confirm this distinction. ([Center for High Performance Computing][2])

### P40 vs M40

Here the P40 is a straightforward generational improvement:

```text
                 M40          P40
--------------------------------------
CUDA cores       3072         3840
VRAM             24GB         24GB
Bandwidth        288          346 GB/s
FP32             ~7           12 TFLOPS
Architecture     Maxwell      Pascal
CC               5.2          6.1
INT8             --           47 TOPS
```

NVIDIA's own launch material specifically positioned P40 against M40 and reported substantially higher inference throughput in its benchmark workloads. ([NVIDIA][1])

So if you see:

```text
M40 24GB  vs  P40 24GB
```

and the prices aren't dramatically different, **P40 is the much more interesting card for an LLM lab**.

### The catch: Pascal is now old

This matters more than the raw specifications.

P40 is:

```text
GP102
  ↓
Pascal
  ↓
sm_61
```

Modern CUDA support has moved beyond Pascal. CUDA 12.7 dropped native Pascal support, so contemporary software stacks can require pinning/patching/building from source. ([GPU Database][3])

Interestingly, people are still running **P40 + llama.cpp in 2026**, including CUDA 12.9-era setups, but these setups require some extra work. One recent tested setup reports P40 + CUDA 12.9 + llama.cpp under WSL2, specifically targeting `sm_61`. ([GitHub][4])

That is very relevant to you because you're already comfortable building CUDA/LLM software yourself.

### For your cheap GPU collection

I'd think about these cards like this:

```text
                    VRAM       BW        CUDA generation

M40                 24GB      288       Maxwell 5.2
                    ↓
P40                 24GB      346       Pascal 6.1
                    ↓
P100                16GB      732       Pascal 6.0
                    ↓
T10 24GB            24GB      ~624      Turing 7.x
                    ↓
RTX 3090            24GB      936       Ampere 8.6
```

For **LLM experimentation**, I'd personally find the following especially interesting:

**P40 24GB:** cheap 24GB Pascal → great hacking/legacy CUDA/llama.cpp card.

**P100 16GB:** phenomenal memory bandwidth → interesting if you find one extremely cheap.

**T10 24GB:** much more modern architecture → potentially the sweet spot if the particular T10 listing really is the 24GB Turing variant.

**3090 24GB:** completely different performance class, but usually much more expensive.

And there's a fun detail for your GPU-repair experiments: **P40 is passive-cooled and rated at 250W**, so don't treat it like a normal desktop GPU. It expects substantial chassis airflow. NVIDIA's product brief explicitly specifies active airflow for thermal operation. ([NVIDIA Images][5])

**Bottom line:** if you find a **P40 24GB around the same used price as an M40 24GB, I'd investigate the P40 first.** If a **P100 16GB is substantially cheaper**, it becomes an interesting bandwidth-per-yuan experiment. If the **T10 24GB** you're looking at is genuinely Turing, I'd investigate that before either Pascal card because the newer CUDA architecture matters increasingly in 2026.

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/184427-Tesla-P40-Datasheet-NV-Final-Letter-Web.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P4"
[2]: https://www.chpc.utah.edu/documentation/guides/gpus-hardware.php?utm_source=chatgpt.com "GPUS and Accelerators at CHPC - Center for High Performance Computing - The University of Utah"
[3]: https://gpus.axiomgaming.net/gpu/tesla-p40?utm_source=chatgpt.com "Tesla P40 Specifications - NVIDIA GPU Database"
[4]: https://github.com/schmared/tesla-p40-wsl2-cuda-llamacpp?utm_source=chatgpt.com "GitHub - schmared/tesla-p40-wsl2-cuda-llamacpp: Run a Tesla P40 (Pascal, sm_61) under WSL2 for local LLM serving: MCDM driver model, CUDA 12.9, Docker GPU passthrough, and llama.cpp built for sm_61. Benchmarked on Qwen3.6-35B-A3B at ~51 tok/s with 128K context. · GitHub"
[5]: https://images.nvidia.com/content/tesla/pdf/Tesla-P40-Product-Brief.pdf?utm_source=chatgpt.com "OVERVIEW

The NVIDIA® Tesla® P40 GPU Accelerator i"
