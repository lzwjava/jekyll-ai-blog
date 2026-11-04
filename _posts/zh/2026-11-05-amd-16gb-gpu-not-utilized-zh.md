---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD 16GB GPU未被利用
translated: true
type: note
---

## GPU / VRAM

**无 NVIDIA GPU** — `nvidia-smi` 失败（"无法与驱动程序通信"），因此这里无法使用 CUDA。

**通过 ROCm 的 AMD GPU**（你询问的那个）：

| 项目 | 值 |
|---|---|
| 设备 | `0000:03:00.0`, DID `0x6861` (Vega 10 / Radeon Instinct MI25 级别), 子系统 `0x0c1e` |
| ROCm 名称 | **AMD Radeon Pro WX 9100** (gfx900, Vega 10) |
| **VRAM 总计** | **17,163,091,968 B = 15.98 GiB (16 GB HBM2)** |
| VRAM 已用 | 8,318,976 B ≈ **7.9 MiB**（基本处于空闲状态） |
| GTT/可见堆 | 16,760,832 KB（由 rocminfo 报告） |
| VBIOS | 113-D0510100-110 |
| 功率上限 | 170 W（当前功耗 6 W） |
| 温度 | 41 °C edge / 42 °C junction/mem |
| 最大核心时钟 | 1500 MHz（当前 852 MHz，0% 负载） |

存在的其他 GPU：Intel HD 530 iGPU（`0x8086:0x1912`，`card1`）— 无专用显存，共享系统内存。

系统：i5-6500，总计 **11 GiB RAM**（已使用 4.0 GiB，可用约 7.1 GiB），4 GiB 交换空间。

### 与此仓库相关
你的 `build/CMakeCache.txt` 包含：
```
GGML_HIP=OFF
SD_HIPBLAS=OFF
SD_CUDA=OFF
```
因此当前构建是 **仅限 CPU** 的，不会使用 16 GB 的 AMD 显卡。要使用它，你需要一个针对 `gfx900` 的 HIP 构建，例如 `-DGGML_HIP=ON -DSD_HIPBLAS=ON -DAMDGPU_TARGETS=gfx900`（注：gfx900 没有 matrix cores，因此其吞吐量大致相当于 Vega 级别——并且 11 GB 的系统 RAM 是模型加载的更严格的限制）。