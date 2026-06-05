---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch FP8 Support Current State
translated: false
type: note
---

Question: How's PyTorch's support of FP8?

Answer:

PyTorch has **native FP8 support** as of recent versions, but it's still maturing. Here's the current state:

**What's Available**

PyTorch supports FP8 through `torch.float8_e4m3fn` and `torch.float8_e5m2` dtypes. The key APIs:

```python
import torch

# Cast to FP8
x_fp8 = x.to(torch.float8_e4m3fn)  # E4M3: higher precision, good for weights/activations
x_fp8 = x.to(torch.float8_e5m2)    # E5M2: wider range, good for gradients

# Check availability
print(torch.cuda.is_bf16_supported())  # True on RTX 4070
```

**torch.float8_experimental**

The main FP8 training path is through `torch.float8_experimental`:

```python
from torchao.float8 import convert_to_float8_training

# Convert model to FP8
model = convert_to_float8_training(model)

# Or use the context manager
with torch.autocast("cuda", dtype=torch.float8_e4m3fn):
    output = model(input)
```

**FP8 Training with torchao**

The most practical path today:

```bash
pip install torchao
```

```python
from torchao.float8 import convert_to_float8_training

model = YourModel()
model = convert_to_float8_training(model)

# Training loop works as normal
optimizer = torch.optim.AdamW(model.parameters())
for batch in dataloader:
    loss = model(batch).sum()
    loss.backward()
    optimizer.step()
```

**Current Limitations**

1. **Hardware support**: FP8 requires Ada Lovelace (RTX 4090+) or Hopper (H100). RTX 4070 has the Tensor Cores but PyTorch's FP8 kernels aren't fully optimized for it yet.

2. **Kernel maturity**: The FP8 kernels are primarily tested on H100/RTX 4090. Performance on RTX 4070 is inconsistent.

3. **Gradient accumulation**: FP8 gradients need careful handling — mixed precision with FP16/BF16 gradients is more stable.

4. **torch.compile compatibility**: FP8 works better with `torch.compile()` for kernel fusion, but compilation overhead can negate gains on small models.

**What Works Well Today**

For your RTX 4070 + nanoGPT setup:

```python
# Best approach: BF16 mixed precision
scaler = torch.amp.GradScaler()
with torch.amp.autocast("cuda", dtype=torch.bfloat16):
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
```

**The Real Answer**

PyTorch's FP8 support is **production-ready on H100**, **experimental on RTX 4090**, and **unreliable on RTX 4070**. The ecosystem is moving fast — `torchao` and `torch.float8_experimental` are the places to watch.

For your current workload: **stick with BF16**. FP8 on RTX 4070 isn't worth the debugging time yet.

References:

- [PyTorch FP8 RFC](https://github.com/pytorch/pytorch/issues/89364)
- [torchao FP8 documentation](https://github.com/pytorch/ao)
- [torch.float8_experimental](https://github.com/pytorch-labs/torchao-experimental)
