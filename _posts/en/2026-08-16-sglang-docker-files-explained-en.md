---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Docker Files Explained
translated: false
type: note
---

Here's what each Docker file in this repo is for. They're all in `docker/` (plus one in `.devcontainer/`):

## Main GPU image (NVIDIA CUDA)

**`docker/Dockerfile`** — The primary SGLang image for NVIDIA GPUs. Multi-stage with parallel builders:

- `framework` stage: full dev image (vim/tmux/gdb/nsight, oh-my-zsh, clangd, etc.)
- `runtime` stage: **production** image — smaller, no dev tools, but keeps the CUDA toolchain so FP8/microscaling kernels can JIT-compile at runtime (DeepGEMM, Triton, FlashInfer)
- Installs sgl-kernel, FlashInfer, DeepEP, Mooncake, MSCCL++, GDRCopy, gateway binary
- `--build-arg CUDA_VERSION` supports 12.6.3 / 12.9.2 / 13.0.3

## Hardware-specific images

| File | Purpose |
| --- | --- |
| `rocm.Dockerfile` | **AMD GPUs** (MI300X gfx942, MI350X gfx950), ROCm 7.0/7.2. Build args: `GPU_ARCH`, `ENABLE_MORI`, `ENABLE_NIXL` |
| `npu.Dockerfile` | **Ascend NPUs** (Huawei), based on CANN 9.0.0, torch_npu |
| `xpu.Dockerfile` | **Intel XPU** (e.g. Arc B580), based on Intel deep-learning-essentials |
| `xeon.Dockerfile` | **CPU-only** inference on Intel Xeon (`SGLANG_USE_CPU_ENGINE=1`, CPU torch) |
| `arm64.Dockerfile` | **CPU-only for ARM64** — same idea as xeon but aarch64 |

## Sidecar services

| File | Purpose |
| --- | --- |
| `sgl-router.Dockerfile` | **sgl-router** — a Rust-based request router for multi-node/multi-worker deployments (in `experimental/sgl-router`). Distroless runtime, <100 MB |
| `gateway.Dockerfile` | **sgl-model-gateway** — the OpenAI-compatible API gateway (auth, API keys, rate limiting), in `sgl-model-gateway/` |
| `sagemaker.Dockerfile` | Wraps the main image for **AWS SageMaker** deployment (adds a `serve` entrypoint script) |

## Wheel builders (CI only)

| File | Purpose |
| --- | --- |
| `sgl-deep-ep.Dockerfile` | Builds the **sgl-deep-ep** pip wheel (DeepEP for CUDA 13, manylinux, includes GDRCopy) |
| `sgl-deep-gemm.Dockerfile` | Builds the **sgl-deep-gemm** pip wheel |
| `kimi_k3/kimi_k3_cu12.Dockerfile`, `kimi_k3_cu13.Dockerfile` | Serving image for the **Kimi-K3 model** (aarch64, sm_90/100a/103a): patches DeepEP (topk 16, SWITCH_HIDDEN += 3584), upgrades DeepGEMM, adds Kimi-K3 SGLang code on top of stock `lmsysorg/sglang:v0.5.16` |

## Dev tooling

| File | Purpose |
|---|---|
| `.devcontainer/Dockerfile` | **VS Code Dev Container** — extends `lmsysorg/sglang:dev` and adds a non-root `devuser` matching your host UID/GID, so you can open this repo in VS Code with file ownership correct |

There's also `docker/compose.yaml` (docker-compose for serving) and `docker/serve` (entrypoint script used by the SageMaker image).

### How to build the main one

```bash
# production runtime image, CUDA 13.0
docker build -f docker/Dockerfile --target runtime \
    --build-arg CUDA_VERSION=13.0.3 -t sglang:runtime .

# full dev image
docker build -f docker/Dockerfile --target framework -t sglang:dev .
```

**TL;DR:** If you're deploying SGLang on NVIDIA GPUs → `Dockerfile` (use the `runtime` target for production). The others exist for AMD/Intel/Ascend/CPU hardware, the router/gateway sidecars, AWS, and CI wheel building.
