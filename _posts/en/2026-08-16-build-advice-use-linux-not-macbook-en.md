---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Build Advice: Use Linux, Not MacBook"
translated: false
type: note
---

Short answer: **No, you don't need to build on the 4070 machine — but a MacBook Pro is also not a good choice.** Here's the reasoning:

## What building actually requires

The build itself never touches the GPU. All the heavy steps (DeepEP, MSCCL++, HPC-ops kernels, FlashInfer cubins) are either **prebuilt wheel downloads** or **nvcc cross-compilation** — nvcc compiles CUDA kernels without a GPU present. What it *does* require:

| Requirement | Detail |
|---|---|
| **CPU architecture** | The image is `linux/amd64`. Building must produce an x86_64 image |
| **Disk** | ~40–60 GB free (this image is huge, multiple stages) |
| **RAM** | 16 GB+ recommended for the parallel BuildKit stages |
| **Host** | Linux with Docker (or Docker Desktop / buildx) |

## Why the MacBook Pro is problematic

- **Apple Silicon MacBook Pro (M-series)** = `arm64` host. Building an `amd64` image requires QEMU emulation via `buildx --platform linux/amd64`. This Dockerfile compiles a *lot* of native code — under emulation that's many hours, often hitting timeouts or OOM, and CUDA/kernel builds under emulation are flaky. Strongly discouraged.
- **Intel MacBook Pro** = `x86_64`, so architecture matches. It would *technically* work via Docker Desktop's Linux VM, but still slow, and you'd need a very beefy one. Not worth it.

## What I'd recommend instead

**Option 1 (easiest) — pull the prebuilt image.** The project publishes official images; you don't need to build at all:
```bash
docker pull lmsysorg/sglang:latest
# or a pinned release, e.g. lmsysorg/sglang:v0.5.16
```

**Option 2 — build on the 4070 machine (or any Linux x86_64 box).** Building on the machine you'll run on is fine and common — just make sure it has the disk/RAM above. Or build on any Linux x86_64 VM (cloud instance, CI), then:
```bash
docker push your-registry/sglang:runtime
# on the 4070 machine:
docker pull your-registry/sglang:runtime
```

## One thing about the RTX 4070

The 4070 is Ada Lovelace (`sm_89`). Prebuilt cubins in the image cover common datacenter archs, so some kernels (e.g. FlashInfer, DeepGEMM FP8) will **JIT-compile at first launch on the 4070**. That's exactly why the `runtime` target keeps the full CUDA toolchain (`nvcc`). Two consequences:

- Use the `runtime` target (as you planned) — the `framework` target also works but is bigger.
- First launch will be slower while JIT kernels compile; subsequent launches reuse the cache (`.cache/sglang`).

**Bottom line:** build on the 4070 machine or another Linux amd64 box; skip the MacBook unless it's a last resort, and consider just pulling `lmsysorg/sglang` if you don't need custom changes.