---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地 FLUX.1-schnell GGUF GPU优化
translated: true
type: note
---

## 综合总结

### 初始目标

用户希望使用**量化后的 GGUF 模型**在本地运行 **FLUX.1-schnell**（一个 12B 参数的文生图模型），具体是来自 [Hugging Face](https://huggingface.co/aifoundry-org/FLUX.1-schnell-Quantized) 的 `flux1-schnell-Q4_0.gguf`。在 CPU 上首次推理生成一张 1024×1024 的图像耗时 **526 秒（约 8 分 47 秒）**。目标是将此运行在用户的 **RTX 4070（12 GB VRAM）** GPU 上。

---

### 逐步工作

#### 1. 环境发现

- 工作目录：`/mnt/data/zz/flux/`
- 已有资源：
  - `models/` — 已包含 `flux1-schnell-Q4_0.gguf`（1.5 GB）、`ae.safetensors`、`clip_l.safetensors`、`t5xxl_fp16.safetensors`
  - `sd_cpp/` — 克隆的 [`stable-diffusion.cpp`](https://github.com/leejet/stable-diffusion.cpp)（sd.cpp），GGUF 原生推理引擎
  - `run_flux_schnell.py` — 基于 diffusers 的 Python 脚本（未使用，因为我们用的是 GGUF 而非完整的 safetensors 模型）

#### 2. 下载脚本

编写了 `download_model.sh` —— 一个独立的 bash 脚本，使用 `curl`/`wget` 下载 GGUF 模型。模型已存在，因此脚本会自动跳过。

#### 3. 首次 CPU 运行与瓶颈分析

在 CPU 上运行 `sd-cli`，结果如下：

| 阶段 | 时间 | 详情 |
| ------ | :----: | ------ |
| 文本编码（CLIP） | 2.2s | 极小，可忽略 |
| Flux 变换器（57 个块，16384 个 token） | ~487s | **主要瓶颈** — 12B 参数 × 4 步 |
| VAE 解码 | 37s | 模型小（95 MB）但激活值巨大（6.6 GB） |
| **总计** | **526s** | 8 分 47 秒 |

核心问题：即使经过 Q4 量化，Flux 变换器仍然是巨大的计算负载。RTX 4070 闲置，而 CPU 在艰难处理。

#### 4. CUDA 重新编译

发现系统具备：

- **NVIDIA RTX 4070**（12 GB VRAM，计算能力 8.9）
- **CUDA 13.2** 工具包及 `nvcc`
- `sd_cpp` 最初是**仅 CPU** 编译

重新编译：

```bash
cmake -S . -B build -DSD_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

验证二进制文件链接了 `libcudart`、`libcublas` 和 `libcuda`。

#### 5. VRAM 争用与解决

**首次尝试**（`--backend cuda`）：Flux 变换器加载到 GPU（6389 MB），但 VAE 计算缓冲区（6657 MB）无法分配 —— `cudaMalloc: out of memory`。

**根本原因**：`llama-server` 占用了约 5.9 GB VRAM，仅剩约 4 GB 可用。

**已应用的修复**：

1. **终止 `llama-server`** 以释放 VRAM（现在约 9.8 GB 可用）
2. **后端拆分** —— `--backend "diffusion=cuda,clip=cpu,vae=cpu,t5xxl=cpu"` 将 Flux 放在 GPU，其余放在 CPU
3. 成功：Flux 扩散在 GPU 上耗时 **12.8s**，VAE 解码在 CPU 上耗时 **35.4s** → 总计 **48.6s**

**第二次优化** —— `--vae-tiling`：将 VAE 解码分块处理，计算缓冲区从 **6.6 GB 降至 416 MB**。这使得 VAE 也能在 GPU 上运行：

```
VAE 解码：  35.4s（CPU） →  2.7s（GPU，分块）
总计：       48.6s        →  15.8s
```

#### 6. 运行脚本

编写了 `run.sh` —— 一个完善的 bash 脚本，包含：

- 自动模型文件验证
- 按模块分配的 CUDA 后端
- 启用 VAE 分块
- `--max-vram 10` 预留空间
- 清晰的嵌入文档及性能分析
- 支持传递额外的 `sd-cli` 参数

#### 7. 版本控制

已提交并推送所有更改：

```
fb4093d  Add download and run scripts for FLUX.1-schnell Q4_0 GGUF
f778e25  Rebuild sd_cpp with CUDA, update run.sh for GPU inference (33x speedup)
```

---

### 最终性能

| 指标 | CPU | GPU（此配置） | 加速比 |
| ------ | :---: | :-------------: | :------: |
| Flux 扩散 | 487s | **12.8s** | **38×** |
| VAE 解码 | 37s | **2.7s** | **14×** |
| 文本编码 | 2.2s | **0.3s** | **7×** |
| **端到端** | **526s** | **~16s** | **33×** |

内存：**约 8.8 GB VRAM** 使用量（Flux 6.4 GB + VAE 分块 0.4 GB + 计算约 2.4 GB），可轻松容纳在 12 GB RTX 4070 中。

### 已知问题

`t5xxl_fp16.safetensors` 报告某个张量存在 `data offsets out of bounds`。模型在缺少 T5 的情况下仍可工作（但提示遵循度降低）。从 [comfyanonymous/flux_text_encoders](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp16.safetensors) 重新下载即可修复。

### 最终文件

| 文件 | 用途 |
| ------ | ------ |
| `download_model.sh` | 下载 GGUF 模型 |
| `run.sh` | 完整的 GPU 加速生成脚本 |
| `sd_cpp/build/bin/sd-cli` | 启用 CUDA 的推理二进制文件 |
