---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing FlashAttention 2 Verification
translated: false
type: note
---

Question: How does this code test whether FlashAttention 2 is working correctly?

Answer:

Your script performs **three levels of verification**:

### 1. Verify PyTorch sees the GPU

```python
import torch
print('torch:', torch.__version__)
print('GPU:', torch.cuda.get_device_name(0))
```

This confirms:

* PyTorch is installed.
* CUDA/HIP backend is working.
* The GPU is visible.

Example output:

```text
torch: 2.8.0+rocm
GPU: AMD Instinct MI300X
```

If this fails, FlashAttention cannot work because PyTorch itself cannot access the GPU.

---

### 2. Verify FlashAttention 2 imports successfully

```python
import flash_attn
print('flash_attn version:', flash_attn.__version__)

from flash_attn import flash_attn_func
print('flash_attn_func imported OK')
```

This checks:

* The FlashAttention package was installed.
* The C++/CUDA/ROCm extension compiled correctly.
* Python can load the compiled shared library.

Typical success:

```text
flash_attn version: 2.8.3
flash_attn_func imported OK
```

Typical failure:

```text
ImportError: cannot import name flash_attn_func
```

or

```text
undefined symbol ...
```

which usually indicates a build problem.

---

### 3. Execute a real FlashAttention kernel

This is the most important part.

```python
q = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

k = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

v = torch.randn(2, 1024, 12, 128,
                device='cuda',
                dtype=torch.bfloat16)

out = flash_attn_func(q, k, v, causal=True)
```

Shape meaning:

| Dimension | Value | Meaning         |
| --------- | ----- | --------------- |
| Batch     | 2     | Two sequences   |
| Seq Len   | 1024  | Context length  |
| Heads     | 12    | Attention heads |
| Head Dim  | 128   | Head size       |

FlashAttention 2 computes:

[
\text{softmax}(QK^T)V
]

using the fused kernel.

Success output:

```text
FA2 forward pass: OK, shape torch.Size([2, 1024, 12, 128])
```

This proves:

* The ROCm kernels loaded.
* The kernel executed on MI300X.
* Output shape is correct.

---

### 4. Test sliding-window attention

```python
out_sw = flash_attn_func(
    q, k, v,
    causal=True,
    window_size=(256, 0)
)
```

This verifies an additional FlashAttention feature.

Instead of attending to all 1024 tokens, each token only sees:

```text
256 tokens to the left
0 tokens to the right
```

Success:

```text
FA2 sliding window: OK, shape torch.Size([2, 1024, 12, 128])
```

This confirms:

* Windowed attention kernels work.
* NanoChat's local attention mode should work.

---

### 5. Verify NanoChat detects FlashAttention

```python
from nanochat.flash_attention import (
    flash_attn as fa,
    USE_FA2,
    HAS_FA2,
    USE_FA3
)
```

These flags determine what NanoChat will actually use.

Expected on MI300X:

```text
HAS_FA2: True
USE_FA2: True
USE_FA3: False
```

Meaning:

| Flag    | Meaning                    |
| ------- | -------------------------- |
| HAS_FA2 | FlashAttention 2 installed |
| USE_FA2 | NanoChat will use FA2      |
| USE_FA3 | FlashAttention 3 active    |

For MI300X today, seeing:

```text
HAS_FA2: True
USE_FA2: True
USE_FA3: False
```

is the ideal result.

---

### Additional benchmark (recommended)

Your test only proves correctness, not speed.

To verify that the fused kernel is actually running efficiently:

```python
import time
import torch

torch.cuda.synchronize()

start = time.time()

for _ in range(100):
    out = flash_attn_func(q, k, v, causal=True)

torch.cuda.synchronize()

elapsed = time.time() - start

print("100 iterations:", elapsed)
print("ms/iter:", elapsed * 1000 / 100)
```

Compare this with PyTorch's standard attention:

```python
torch.nn.functional.scaled_dot_product_attention
```

On an MI300X, FlashAttention 2 should generally be noticeably faster and use less memory for long sequence lengths.

---

If all of the following succeed:

```text
flash_attn_func imported OK
FA2 forward pass: OK
FA2 sliding window: OK
HAS_FA2: True
USE_FA2: True
```

then FlashAttention 2 is not merely installed—it is actually executing attention kernels successfully on your MI300X and NanoChat can use it during training.
