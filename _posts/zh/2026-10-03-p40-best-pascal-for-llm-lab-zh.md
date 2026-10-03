---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P40：LLM实验室的最佳帕斯卡
translated: true
type: note
---

问题：**在你的 LLM/GPU 实验室里，Tesla P40 与其他型号相比，特别是与 M40 和 P100 相比，表现究竟如何？**

回答：**针对你的用例，P40 24GB 可能是最值得关注的 Pascal 架构显卡。** 它本质上是 **M40 的 24GB 继任者**，专门为推理 (inference) 设计。NVIDIA 官方公布的规格为 3,840 个 CUDA 核心、24GB GDDR5 显存、346 GB/s 带宽、12 TFLOPS FP32 以及 250W 功耗。([NVIDIA][1])

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

P40 的 **24GB 显存容量是其主要吸引力**。NVIDIA 明确将其定位为一款推理加速器 (inference accelerator)，支持 INT8 并拥有 47 TOPS INT8 的性能。([NVIDIA][1])

### P40 vs P100

这是一个很有意思的权衡：

| 项目              |           P40 |      P100 PCIe |
| ----------------- | ------------: | -------------: |
| 架构              |        Pascal |         Pascal |
| CUDA 核心         |     **3,840** |          3,584 |
| 显存容量          |      **24GB** |           16GB |
| 显存类型          |         GDDR5 |       **HBM2** |
| 带宽              |      346 GB/s |   **732 GB/s** |
| FP32              | **12 TFLOPS** |     9.3 TFLOPS |
| FP64              |  ~0.37 TFLOPS | **4.7 TFLOPS** |
| 计算能力 (CC)     |           6.1 |            6.0 |
| TDP               |          250W |           250W |
| 预期工作负载      | **推理 (Inference)** |   HPC/训练 (Training) |

所以：

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

P100 的 HBM2 带宽是 P40 的 GDDR5 带宽的 **2 倍以上**，而 P40 的显存则多出 50%。官方公布的规格参数也证实了这一点。([Center for High Performance Computing][2])

### P40 vs M40

在这里，P40 是纯粹的代际改进：

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

NVIDIA 当时的官方发布材料特别将 P40 与 M40 进行了对比，并报告了 P40 在其基准测试工作负载中实现了大幅更高的推理吞吐量。([NVIDIA][1])

因此，如果你看到下面这样的对比：

```text
M40 24GB  vs  P40 24GB
```

并且价格相差不大，那么对于 LLM 实验室来说，**P40 是更有意思的选择**。

### The catch: Pascal is now old

这比原始规格参数更重要。

P40 的架构路径：

```text
GP102
  ↓
Pascal
  ↓
sm_61
```

现代 CUDA 的支持范围早已超越了 Pascal。CUDA 12.7 已放弃对 Pascal 架构的本地支持。因此，使用最新的软件栈很可能需要固定 CUDA 版本、应用特定补丁或直接从源码编译。([GPU Database][3])

有趣的是，直到 2026 年仍有人在运行 **P40 + llama.cpp** 的组合，甚至包括了 CUDA 12.9 时代的配置，但这需要额外进行一些工作。最近一个经过验证的配置报告显示，在 WSL2 下成功运行了 P40 + CUDA 12.9 + llama.cpp，并特别针对 `sm_61` 进行了编译。([GitHub][4])

这对你来说尤其相关，因为你已经很熟悉如何自行构建 CUDA/LLM 软件。

### For your cheap GPU collection

我大致是这么看待这些显卡的：

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

对于 **LLM 实验**，我个人认为以下显卡尤其值得关注：

**P40 24GB：** 价格便宜的 24GB Pascal 架构显卡 → 非常适合搞机、折腾旧版 CUDA 和运行 llama.cpp。

**P100 16GB：** 显存带宽惊人 → 如果能以极低的价格找到一块，会非常有趣。

**T10 24GB：** 架构要新得多 → 如果你看到的那款 T10 真的是 24GB 的 Turing 架构变体，它可能是一个最佳选择。

**3090 24GB：** 完全不同的性能等级，但价格通常要贵得多。

此外，对于你的 GPU 修复实验来说，还有一个有趣的细节：**P40 采用被动散热，功耗为 250W**，所以不要把它当作普通的桌面 GPU 来对待。它需要足够强的机箱风道。NVIDIA 的官方产品简介明确要求必须使用主动式机箱气流来保证散热。([NVIDIA Images][5])

**总结一下：** 如果你发现 **P40 24GB 与 M40 24GB 二手价格差不多，我会优先研究 P40**。如果 **P100 16GB 便宜得多**，它会成为一个有趣的“每元带宽” (bandwidth-per-yuan) 实验。如果你看中的 **T10 24GB** 确实是真正的 Turing 架构，我会在考虑上述两款 Pascal 架构显卡之前优先研究它，因为更新的 CUDA 架构在 2026 年变得越来越重要。

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/184427-Tesla-P40-Datasheet-NV-Final-Letter-Web.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P4"
[2]: https://www.chpc.utah.edu/documentation/guides/gpus-hardware.php?utm_source=chatgpt.com "GPUS and Accelerators at CHPC - Center for High Performance Computing - The University of Utah"
[3]: https://gpus.axiomgaming.net/gpu/tesla-p40?utm_source=chatgpt.com "Tesla P40 Specifications - NVIDIA GPU Database"
[4]: https://github.com/schmared/tesla-p40-wsl2-cuda-llamacpp?utm_source=chatgpt.com "GitHub - schmared/tesla-p40-wsl2-cuda-llamacpp: Run a Tesla P40 (Pascal, sm_61) under WSL2 for local LLM serving: MCDM driver model, CUDA 12.9, Docker GPU passthrough, and llama.cpp built for sm_61. Benchmarked on Qwen3.6-35B-A3B at ~51 tok/s with 128K context. · GitHub"
[5]: https://images.nvidia.com/content/tesla/pdf/Tesla-P40-Product-Brief.pdf?utm_source=chatgpt.com "OVERVIEW

The NVIDIA® Tesla® P40 GPU Accelerator i"