---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X Support in llama.cpp
translated: false
type: note
---

**Question:** Does llama.cpp have good support for AMD MI300X?

**Answer:**

Yes — as of late 2025, the support is genuinely good and has gone from mediocre to competitive. Here's the technical breakdown:

---

## Backend: HIP (ROCm), not CUDA

llama.cpp reaches MI300X via its HIP backend — HIP is AMD's CUDA-compatibility layer that compiles to GCN/CDNA ISA. The framework extends to AMD Instinct GPUs such as MI300X via HIP (Heterogeneous-computing Interface for Portability). The key device identifier at runtime is `gfx942` (CDNA3 architecture).

---

## The Wavefront-Size Bug (Now Fixed)

This was the root cause of historically poor AMD performance in llama.cpp. One of the main reasons earlier versions of llama.cpp did not achieve good performance on AMD Instinct GPUs is because it failed to take advantage of the higher wavefront size of AMD GPUs. Specifically, NVIDIA GPUs only have a wavefront size of 32, while AMD Instinct GPUs have a wavefront size of 64. Earlier implementations hardcoded the wavefront size to 32, making it impossible to fully utilize the compute power of AMD Instinct GPUs.

The fix was upstreamed in July 2025. This alone was a major unlock.

---

## October 2025: Grouped GEMM for MoE

AMD added support for the Grouped GEMM API in hipBLASLt to llama.cpp in the October 2025 release. Grouped GEMM kernels allow the inference engine to bundle matrix multiplications with different sizes, transposes, and scaling factors into a single kernel launch, yielding significant speedups over naive batched GEMM loops, especially for workloads like mixture-of-experts (MoE) models.

This directly benefits DeepSeek-V3, Mixtral, Kimi-K2, etc.

---

## Benchmark Numbers (Dec 2025, AMD's own testing)

With ROCm 7, AMD Instinct MI300X systems deliver industry-leading throughput, outperforming the NVIDIA H100 across multiple models and configurations. The AMD Instinct MI300X 8x GPU offers up to 76% higher inference throughput vs. NVIDIA H100 on DeepSeek-V3-671B-Q4_K_M with a prompt size of 4096, and up to 213% higher inference throughput vs. NVIDIA H100 on Meta-Llama-3.1-70B-Instruct-Q4_K_M when flash attention is enabled.

The 213% number makes sense physically — the MI300X has 192GB HBM3 (vs H100's 80GB) and ~5.3 TB/s peak bandwidth, so for memory-bandwidth-bound inference (which token generation always is), it should crush H100.

Real-world community benchmark on a single MI300X (Qwen3-8B Q4_K_M):

```
pp512  → 5839 t/s
tg128  → 161 t/s
```

Performance is in the middle between RTX 4090 and RTX 5090 for a single MI300X card — for 8-card configs the gap widens dramatically because of the unified 192GB HBM3 per card.

---

## Build Instructions

```bash
# Install ROCm 7.x first, then:
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS=gfx942 \  # MI300X target
  -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j$(nproc)

# Run with flash attention on (critical for performance)
./build/bin/llama-bench -m model.gguf -ngl 999 -fa 1
```

AMD also ships AMD-validated llama.cpp prebuilt binaries — pre-compiled stable executables (like server and llama-bench) that are ready to run on a Linux system without requiring any compilation.

---

## Summary Table

| Feature | Status |
|---|---|
| HIP/ROCm backend | ✅ First-class |
| Flash attention | ✅ Supported, recommended |
| Multi-GPU (8x MI300X) | ✅ Works |
| MoE / Grouped GEMM | ✅ Oct 2025+ |
| DeepSeek-V3 671B Q4 | ✅ Benchmarked |
| Prebuilt ROCm binaries | ✅ AMD ships them |
| vs H100 on throughput | ✅ Wins at large context/batch |

---

**Bottom line:** If you have access to MI300X (e.g., AMD Developer Cloud), llama.cpp is a legitimate top-tier inference stack for it — not a second-class citizen anymore. The 192GB HBM per card means you can fit 70B+ models fully in VRAM with room for long contexts, and the wavefront + grouped GEMM fixes mean the compute is now properly utilized. For production at scale, vLLM+ROCm is the alternative worth comparing.

**References:**

- [Accelerating llama.cpp on AMD Instinct MI300X (Dec 2025)](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp-oct2025/README.html)
- [Llama.cpp Meets Instinct: A New Era of Open-Source AI Acceleration](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html)
- [Performance of llama.cpp on AMD GPU (MI300X) — GitHub Discussion](https://github.com/ggml-org/llama.cpp/discussions/14640)
- [llama.cpp Prebuilt Binaries — ROCm Docs](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedrad/windows/llm/llamacpp.html)
