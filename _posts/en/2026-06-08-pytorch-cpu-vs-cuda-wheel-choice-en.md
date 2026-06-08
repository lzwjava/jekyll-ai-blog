---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch CPU vs CUDA Wheel Choice
translated: false
type: note
---

**Question:** How does PyTorch distribute CPU-only vs CUDA wheels, and which one should I install on Windows?

## Answer

PyTorch distributes **separate wheels** because CUDA binaries are massive and optional. The CPU wheel (`~200 MB`) contains only:
- PyTorch runtime code
- CPU kernels (BLAS, MKL-DNN)
- Python bindings

The CUDA wheel (`2-3 GB`) bundles:
- Everything from CPU wheel
- NVIDIA CUDA runtime libraries (cudart, cublas, cunn, etc.)
- cuDNN (deep learning primitives)
- compiled GPU kernels for your CUDA version

**Why?** Users running inference on CPU-only systems don't need 2GB of unused CUDA binaries. Wheels with bundled CUDA also lock you to a specific CUDA version—if you upgrade CUDA later, a bundled wheel won't match.

### Installation on Windows

**CPU-only** (fastest install, no GPU):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**CUDA 12.4** (most common, requires NVIDIA GPU + CUDA 12.4 installed):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

**CUDA 11.8**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

The `--index-url` flag tells pip to fetch from PyTorch's wheel repository instead of PyPI (which only hosts CPU wheels by default).

### Verify what you got

```python
import torch
print(torch.cuda.is_available())  # True if CUDA wheel installed correctly
print(torch.__version__)
print(torch.version.cuda)  # None if CPU, "12.4" if CUDA 12.4, etc
```

### Key details

- **You need CUDA runtime installed separately** — the wheel bundles cuBLAS/cuDNN but still needs NVIDIA drivers + CUDA toolkit. Check: `nvidia-smi` should work.
- **CUDA 12.4 wheel works with CUDA 12.1+** (forward-compatible within major version).
- **RTX 4070** on your workstation needs CUDA 12.x. Grab the cu124 wheel.
- **Install once, use everywhere** — after `pip install`, you just `import torch` and pick device: `torch.device('cuda')` vs `torch.device('cpu')`.

If you're doing serious training on your 4070, don't skip the CUDA wheel. CPU training on a GPU-capable machine is painful.