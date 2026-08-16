---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang Docker 文件详解
translated: true
type: note
---

该仓库中每个Docker文件的作用如下。它们都位于 `docker/` 目录下（另有一个在 `.devcontainer/` 中）：

## 主 GPU 镜像（NVIDIA CUDA）

**`docker/Dockerfile`** — 用于 NVIDIA GPU 的主要 SGLang 镜像。多阶段构建，具备并行构建器：
- `framework` 阶段：完整的开发镜像（包含 vim/tmux/gdb/nsight、oh-my-zsh、clangd 等）
- `runtime` 阶段：**生产**镜像 — 更小，无开发工具，但保留 CUDA 工具链，以便 FP8/microscaling 内核能在运行时 JIT 编译（DeepGEMM、Triton、FlashInfer）
- 安装 sgl-kernel、FlashInfer、DeepEP、Mooncake、MSCCL++、GDRCopy、gateway 二进制文件
- `--build-arg CUDA_VERSION` 支持 12.6.3 / 12.9.2 / 13.0.3

## 硬件特定镜像

| 文件 | 用途 |
|---|---|
| `rocm.Dockerfile` | **AMD GPU**（MI300X gfx942、MI350X gfx950），ROCm 7.0/7.2。构建参数：`GPU_ARCH`、`ENABLE_MORI`、`ENABLE_NIXL` |
| `npu.Dockerfile` | **Ascend NPU**（华为），基于 CANN 9.0.0、torch_npu |
| `xpu.Dockerfile` | **Intel XPU**（例如 Arc B580），基于 Intel deep-learning-essentials |
| `xeon.Dockerfile` | **纯 CPU** 推理，基于 Intel Xeon（`SGLANG_USE_CPU_ENGINE=1`，CPU torch） |
| `arm64.Dockerfile` | **ARM64 纯 CPU** — 与 xeon 思路相同，但架构为 aarch64 |

## 辅助服务

| 文件 | 用途 |
|---|---|
| `sgl-router.Dockerfile` | **sgl-router** — 基于 Rust 的请求路由器，用于多节点/多 worker 部署（位于 `experimental/sgl-router`）。采用 Distroless 运行时，小于 100 MB |
| `gateway.Dockerfile` | **sgl-model-gateway** — 兼容 OpenAI 的 API 网关（认证、API 密钥、速率限制），位于 `sgl-model-gateway/` |
| `sagemaker.Dockerfile` | 包装主镜像，用于 **AWS SageMaker** 部署（添加了 `serve` 入口脚本） |

## Wheel 构建器（仅 CI 使用）

| 文件 | 用途 |
|---|---|
| `sgl-deep-ep.Dockerfile` | 构建 **sgl-deep-ep** pip wheel（DeepEP for CUDA 13，manylinux，包含 GDRCopy） |
| `sgl-deep-gemm.Dockerfile` | 构建 **sgl-deep-gemm** pip wheel |
| `kimi_k3/kimi_k3_cu12.Dockerfile`、`kimi_k3_cu13.Dockerfile` | 用于 **Kimi-K3 模型** 的服务镜像（aarch64，sm_90/100a/103a）：修补 DeepEP（topk 16，SWITCH_HIDDEN += 3584），升级 DeepGEMM，在基础 `lmsysorg/sglang:v0.5.16` 之上添加 Kimi-K3 SGLang 代码 |

## 开发工具

| 文件 | 用途 |
|---|---|
| `.devcontainer/Dockerfile` | **VS Code Dev Container** — 扩展自 `lmsysorg/sglang:dev`，添加了与主机 UID/GID 匹配的非 root 用户 `devuser`，以便在 VS Code 中打开此仓库时文件所有权正确 |

此外还有 `docker/compose.yaml`（用于服务的 docker-compose）和 `docker/serve`（SageMaker 镜像使用的入口脚本）。

### 如何构建主镜像
```bash
# 生产运行时镜像，CUDA 13.0
docker build -f docker/Dockerfile --target runtime \
    --build-arg CUDA_VERSION=13.0.3 -t sglang:runtime .

# 完整开发镜像
docker build -f docker/Dockerfile --target framework -t sglang:dev .
```

**简而言之：** 如果你要在 NVIDIA GPU 上部署 SGLang → 使用 `Dockerfile`（生产环境使用 `runtime` 目标）。其他镜像适用于 AMD/Intel/Ascend/CPU 硬件、router/gateway 辅助服务、AWS 以及 CI wheel 构建。