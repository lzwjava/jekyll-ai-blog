---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attn CUDA Build Hang Fix
translated: false
type: note
---

Question: Why does `pip install flash-attn==2.8.4` get stuck at `Building wheel for flash-attn`?

Answer:

It is not actually stuck downloading. It has moved into the **CUDA extension compilation phase**.

`flash-attn` is not a pure Python package. The line:

```
Building wheels for collected packages: flash-attn
  Building wheel for flash-attn (s/tup.py) ... \
```

means pip is running something like:

```
python setup.py bdist_wheel
```

which compiles C++/CUDA kernels.

For your environment:

* Python: 3.12 (shown by `/home/lzw/.local/lib/python3.12`)
* PyTorch CUDA: likely CUDA 13.0 packages
* GPU: RTX 4070 (Ada, sm_89)
* flash-attn: 2.8.4

the compile can take **10–60 minutes**, especially if it builds many architectures.

Check if it is really working:

```bash
top
```

or:

```bash
htop
```

Look for:

```
nvcc
g++
c++
ninja
```

CPU should be high if compiling.

Also check:

```bash
ps aux | grep nvcc
```

You may see:

```
nvcc -c flash_attn_2_cuda.cu
```

---

## Why it is slow

FlashAttention builds many CUDA kernels:

```
flash_attn/
 ├── softmax kernels
 ├── fused attention forward
 ├── fused attention backward
 ├── dropout kernels
 └── different head dimensions
```

The build matrix is large:

```
GPU architectures:
sm80  (A100)
sm86  (RTX 30)
sm89  (RTX 40)
sm90  (H100)
...
```

If it compiles everything, it wastes time.

---

## Faster build for RTX 4070

Your GPU is Ada:

```
compute capability: 8.9
```

Set:

```bash
export TORCH_CUDA_ARCH_LIST="8.9"
```

Then reinstall:

```bash
pip uninstall flash-attn -y

MAX_JOBS=8 TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

`MAX_JOBS` controls parallel compilation.

For your CPU, choose:

```bash
nproc
```

then maybe:

```bash
MAX_JOBS=$(nproc)
```

---

## Another possible problem: CUDA mismatch

Your log shows:

```
nvidia-cuda-nvrtc==13.0.88
nvidia-nvjitlink==13.0.88
```

but your previous issue mentioned:

```
Python 3.14 + CUDA 13.2 vs torch CUDA 12.8 mismatch
```

Flash-attn is sensitive to:

```
NVIDIA driver
        |
        v
CUDA runtime
        |
        v
PyTorch CUDA
        |
        v
flash-attn compiled CUDA
```

Check:

```python
import torch

print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.get_device_name())
```

Expected something like:

```
2.x.x
12.8
NVIDIA GeForce RTX 4070
```

If PyTorch says CUDA 12.8 but pip pulled CUDA 13 packages, compilation may fail later.

---

## If you just want to run experiments

You do not need flash-attn.

PyTorch SDPA:

```python
import torch.nn.functional as F

out = F.scaled_dot_product_attention(
    q, k, v,
    is_causal=True
)
```

already uses optimized kernels:

```
FlashAttention backend
        |
        +-- available? yes -> use
        |
        +-- unavailable -> memory efficient SDPA
        |
        +-- fallback -> math kernel
```

For nanoGPT/vLLM learning, SDPA is usually enough.

---

My guess from this log:

1. It is compiling, not frozen.
2. First build can easily take 20+ minutes.
3. If CPU is idle for >5 minutes, interrupt it.
4. Retry with:

```bash
MAX_JOBS=8 TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

That should reduce the build from a long generic CUDA build to an RTX 4070-specific one.