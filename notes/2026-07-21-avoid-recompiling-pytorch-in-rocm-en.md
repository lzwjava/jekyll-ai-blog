---
audio: false
generated: true
image: false
lang: en
layout: post
title: Avoid Recompiling PyTorch in ROCm
translated: false
type: note
---

**Question: Should I avoid recompiling PyTorch in this AMD OneClick ROCm image because the friend said Torch is already built?**

**Answer: Yes.** If the image:

```
amd-oneclick-base:rocm7.2.1-py3.12-v20260416
```

already contains a PyTorch build compiled for ROCm 7.2.1, you normally **should not rebuild PyTorch**.

For AMD GPU workloads, the expensive part is not installing Python packages — it is compiling PyTorch with ROCm/HIP support:

```
PyTorch
   |
   +-- ATen kernels
   +-- CUDA/HIP backend
   +-- MIOpen
   +-- RCCL
   +-- Triton kernels
```

A prebuilt ROCm image usually already has:

```bash
python -c "import torch; print(torch.__version__)"
python -c "import torch; print(torch.version.hip)"
python -c "import torch; print(torch.cuda.is_available())"
```

Expected:

```
2.x.x
7.2.1
True
```

The naming is confusing:

* `torch.version.hip` → ROCm version (AMD kept CUDA API compatibility)
* `torch.cuda.is_available()` → still returns `True` on AMD because PyTorch uses the CUDA API abstraction layer

Check:

```bash
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("hip:", torch.version.hip)
print("gpu:", torch.cuda.get_device_name(0))
PY
```

Example:

```
torch: 2.7.0+rocm7.2
hip: 7.2.1
gpu: AMD Instinct MI300X
```

---

For your Radeon Cloud environment, the correct workflow is probably:

```bash
# don't rebuild torch
pip install transformers accelerate diffusers vllm
```

or for FLUX:

```bash
pip install diffusers transformers accelerate sentencepiece protobuf
```

Then test:

```bash
python -c "import torch; print(torch.cuda.get_device_name())"
```

Only rebuild PyTorch if:

1. You need a custom ROCm patch.
2. You need a newer unreleased commit.
3. You need special compile flags:

```bash
PYTORCH_ROCM_ARCH="gfx942"
```

for MI300X, etc.

Otherwise you are wasting hours compiling something the image author already optimized.

The friend's statement:

> torch 镜像里帮你编译好了。不要重编译了吧。

means:

> "The Torch build is already compiled inside the image. Don't compile it again."

That is the right advice.
