---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix CUDA Version Mismatch for llama.cpp
translated: false
type: note
---

Question: What is the best approach to resolve the CUDA driver/runtime version mismatch where the driver supports CUDA 12.8 but the installed toolkit is CUDA 13.2, in order to run llama.cpp with GPU acceleration?

Answer:Question: How should the CUDA driver/runtime mismatch be resolved when the NVIDIA driver 570 (supporting CUDA 12.8) is installed but llama.cpp was compiled against CUDA toolkit 13.2, causing GPU offload to fail and fall back to CPU-only inference?

Answer:

## Root Cause Analysis

The core problem is a **forward-incompatibility violation**: CUDA 13.0 requires driver 580+, CUDA 12.9 requires 575+, and CUDA 12.8 is paired with driver 570. Your driver 570 (CUDA 12.8) simply cannot run a binary linked against the CUDA 13.2 runtime. The runtime fails at `ggml_cuda_init` before any inference even begins.

---

## Solutions (Best → Fallback)

### ✅ Option 1: Upgrade the NVIDIA Driver (Recommended — Clean Fix)

This is the correct, permanent solution. CUDA 13.x support requires driver 580+. Ubuntu already supports this:

```bash
# Add NVIDIA's official repo and upgrade
sudo apt update
sudo apt install nvidia-driver-580
sudo reboot
```

After reboot, verify:
```bash
nvidia-smi   # Should now show CUDA 13.x
```

Then rebuild llama.cpp normally with your existing CUDA 13.2 toolkit — no changes needed.

> **Why this works:** Your CUDA toolkit version should match or be slightly lower than your nvidia-smi CUDA version. Upgrading the driver to 580 closes the gap.

---

### ✅ Option 2: Install CUDA 12.8 Toolkit + Rebuild (Alternative)

If you cannot or do not want to upgrade the driver, install the matching toolkit:

```bash
# Install CUDA 12.8 toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-8
```

Then rebuild llama.cpp pointing cmake at the 12.8 toolkit:

```bash
cmake -B build \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.8/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES="native"
cmake --build build --config Release -j$(nproc)
```

---

### ⚠️ Option 3: CUDA Forward Compatibility Package (Advanced)

NVIDIA provides forward compatibility packages (`cuda-compat-*`) that install newer GPU driver libraries alongside an older kernel driver, allowing newer CUDA runtimes to work with older drivers.

```bash
sudo apt install cuda-compat-12-8
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/compat:$LD_LIBRARY_PATH
```

However, applications requiring PTX JIT compilation support have feature restrictions with the forward compatibility approach, so this is less reliable for llama.cpp.

---

### ❌ Why Your Current Approach (Link Trick) Won't Work

Trying to link the nvcc 13.2-compiled binary against the CUDA 12.2 runtime libraries (`libcudart.so.12`) will fail because:

- The binary's internal CUDA API calls reference symbols from the 13.x runtime ABI
- The 12.x runtime does not have these symbols
- The mismatch happens at the **runtime ABI level**, not just the driver check

---

## Recommended Action Plan

```
Driver 570 (CUDA 12.8) + Toolkit 13.2 → BROKEN
        ↓
Option A: Upgrade driver to 580 → WORKS with toolkit 13.2
Option B: Keep driver 570, rebuild llama.cpp with toolkit 12.8 → WORKS
```

**Option A is faster and cleaner** — a single `apt install nvidia-driver-580 && reboot` and you're done with zero llama.cpp rebuild needed.

References:

- [NVIDIA CUDA Compatibility Documentation](https://docs.nvidia.com/deploy/pdf/CUDA_Compatibility.pdf)
- [Ubuntu Added NVIDIA 580 Driver Support](https://ubuntuhandbook.org/index.php/2025/09/ubuntu-added-nvidia-580-driver/)
- [Beginner's Guide: Setting up llama.cpp for Local LLM Experiments (GPU Optimized)](https://balaakshay.medium.com/beginners-guide-setting-up-llama-cpp-for-local-llm-experiments-gpu-optimized-291adc5b7ba2)