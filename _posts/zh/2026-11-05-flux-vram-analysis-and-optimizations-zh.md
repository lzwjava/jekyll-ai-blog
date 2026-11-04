---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX VRAM分析与优化
translated: true
type: note
---

## 总结发现

**机器：** RTX 4070（Ada, CUDA 13, driver 580），**总计 12,282 MiB**，桌面占用约 1.35 GB → **约 10.5 GB 可用**。torch 2.10.0+cu128 且 `cuda.is_available() = True`，ffmpeg/ffprobe 已安装，diffusers 0.39.0。

**该仓库以 AMD 为目标：** `--provider local` 硬编码了 `/root/FLUX.*`（远程 ROCm 机器）。这里唯一实际起作用的 GPU 路径是 `--provider sdcpp`（位于 `/mnt/data/zz/flux` 的 stable-diffusion.cpp CUDA 构建），该路径已通过 CUDA 编译。

**我实际运行了 sd-cli 两次：**

| 尝试 | 结果 |
|---|---|
| 全部在 GPU 上（无 `--backend`） | **OOM** — 6,389 MB 的扩散模型 `cudaMalloc 失败` |
| `--backend diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu` | ✅ **可行** — 512×384, 2 步, 总计 60 秒 |

## VRAM 需求（实测，FLUX.1-schnell Q4_0 GGUF）

sd-cli 报告的权重占用：

| 组件 | 大小 | 放置位置 |
|---|---|---|
| T5-XXL fp16 | 9,318.83 MB | CPU（必须卸载） |
| FLUX Q4_0 diffusion | 6,389.02 MB | GPU |
| VAE | 160 MB | GPU |
| CLIP-L | ~246 MB（内部 text_encoders） | CPU |
| **总计** | **15,867.85 MB** | |

| 模式 | VRAM 权重 | + 激活值 @960×720 | 峰值需求 | 在此 4070 上的结论 |
|---|---|---|---|---|
| 全 GPU | 15.9 GB | ~1.5–2.5 GB | **~18 GB** | ❌ OOM（已确认） |
| T5/CLIP 在 CPU 上 | 6.55 GB | ~1.5–2 GB | **~8–8.5 GB** | ✅ 适合 10.5 GB 可用空间 |
| 全 GPU 搭配 fp8 T5 | ~11.3 GB | ~1.5–2 GB | ~13 GB | ⚠️ 仍然很紧张 |

**经验法则：**
- **最低要求：** ~7 GB VRAM + ~10 GB 系统 RAM（T5 卸载）→ 可在 8 GB 显卡上以 ≤768×576 运行。
- **此卡的舒适区：** **8–9 GB 空闲 VRAM**，`--max-vram 9`，960×720。将桌面占用保持在 ~2 GB 以下。
- **全 GPU（无卸载）：** 需要 **≥18 GB**（16 GB 显卡仍需卸载 T5；24 GB 才舒适）。
- **diffusers `local` 路径（bf16 FLUX，12B 参数）：** ~24 GB 权重 — 在 12 GB 上只能通过顺序 CPU 卸载实现，且您本地没有这些权重（只有 GGUF）。

**成本说明：** 每次 `sd-cli` 运行都会重新加载 6.4 GB 的扩散模型（60 秒中的约 50 秒）。一个 5 场景的视频约 **5 分钟**，几乎全是模型加载时间。一个持久的 `sd-server`（二进制文件就在那里）可以将每个场景的时间缩短到几秒钟。

## 应进行的更改

1. **`smoke_test.py` + `fluxreel smoke`** — 分阶段检查：deps/ffmpeg → GPU 探测（`nvidia-smi` + CUDA）→ sd-cli/模型文件 → 在 GPU 上生成一张 512×384 的小图像 → 幻灯片帧 → 3 秒 1080×1920 ffmpeg 剪辑 → ffprobe 验证。`--quick` 跳过 GPU，`--full` 运行整个 5 场景流程。
2. **离线场景规划器** — `_generate_scenes()` 目前*需要* OpenRouter；添加一个确定性的 markdown 衍生回退（`--offline`），以便烟雾测试和视频生成无需网络/成本即可工作。
3. **`sdcpp` provider → 一流的本地 GPU 后端** — 自动检测 CUDA 构建/模型，默认选择拆分后端（T5 在 CPU 上），暴露 `--width/--height/--max-vram`，并在日志中报告 GPU。可选地包装 `sd-server` 以消除每场景 50 秒的重新加载。
4. **修复 CUDA 下的 `local`（diffusers）** — 环境可配置的模型目录，`cuda` + bf16，使用 model-CPU-offload 替代仅限 ROCm 的假设，以便在您下载完整 FLUX 权重时能够工作。
5. README/pyproject 更新。

是否要我立即实现 1–3（烟雾测试 + 离线规划器 + 支持 CUDA 的 sdcpp 默认值），并将 `sd-server` 加速作为后续任务？