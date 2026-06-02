---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving CUDA Version Mismatch
translated: false
type: note
---

## 🦞 Driver Upgrade Review: 570 → 580

### Problem
llama.cpp compiled against CUDA 13.2 toolkit, but driver 570 only supports CUDA 12.8. Every GPU init call failed with:
```
ggml_cuda_init: failed to initialize CUDA: CUDA driver version is insufficient for CUDA runtime version
```

### What I Did

**1. Diagnosed the mismatch**
- `nvidia-smi` → driver 570.211.01, CUDA 12.8
- `nvcc --version` → CUDA 13.2.51
- The runtime (`libcudart.so.13`) checks driver version at `cuInit()` and bails because driver 570's `libcuda.so` doesn't support the 13.x ABI

**2. Attempted link-time workarounds (failed)**
- **LD_PRELOAD** with CUDA 12.2's `libcudart.so.12` — didn't work because the `libggml-cuda.so` has hardcoded `NEEDED` entries for `libcudart.so.13`, `libcublas.so.13`, `libcublasLt.so.13`. The dynamic linker resolves those before checking LD_PRELOAD
- **patchelf** to swap `*.so.13` → `*.so.12` — got past the soname check but hit `version 'libcudart.so.13' not found` because the binary has symbol version bindings from the 13.x ABI that don't exist in 12.x. Compile-time ABI mismatch, can't be shimmed

**3. Clean fix: upgrade the driver**
- Checked `apt-cache search` — `nvidia-driver-580` available in the repo
- Dry-run showed clean upgrade path replacing all 570 packages
- Hit one file conflict: `libnvidia-extra-570` owned `/usr/lib/x86_64-linux-gnu/gbm/nvidia-drm_gbm.so` which 580's `libnvidia-gl-580` also wanted. Purged the leftover 570 package, ran `apt install -f` to complete
- DKMS built kernel modules for 6.8.0-107

**4. Ready for reboot**
- Driver 580 supports CUDA 13.x → no more version mismatch
- llama.cpp needs a clean rebuild after reboot (cmake configure is already done)
- Single `make -j$(nproc) llama-server` and launch with `-ngl 99`

### Why 580 Instead of Rebuilding with CUDA 12?
- CUDA 12.2 runtime libs were present but **no nvcc 12.2 compiler** — only nvcc 13.2 installed
- Installing nvcc 12.2 would require `cuda-nvcc-12-2` package + full rebuild, and we'd still be on an older toolkit long-term
- Driver upgrade is a one-time fix that makes the existing CUDA 13.2 toolkit work permanently

### Current State

| Item | Status |
|------|--------|
| nvidia-driver-580 packages | ✅ Installed |
| DKMS modules (6.8.0-107) | ✅ Built |
| CMake configure | ✅ Done |
| Kernel module loaded | ⏳ Needs reboot |
| llama-server built | ⏳ After reboot |
| GPU inference | ⏳ After reboot |
