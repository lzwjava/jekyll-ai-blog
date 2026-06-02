---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GradScaler for Mixed-Precision Training
translated: false
type: note
---

`torch.cuda.amp.GradScaler` is a PyTorch utility class designed to **automatically scale gradients** during mixed-precision training using **Automatic Mixed Precision (AMP)**. It helps prevent underflow in gradients when using `float16` (half-precision) tensors, which can otherwise become too small to be represented accurately.

---

### Why Use `GradScaler`?

In mixed-precision training:

- **Forward/backward passes** use `float16` for speed and memory savings.
- **Gradients** computed in `float16` may become very small → **underflow to zero**.
- `GradScaler` scales the **loss** by a factor (e.g., 2¹⁵ = 32768) before the backward pass.
- Gradients are scaled proportionally → stay in representable range.
- Before optimizer step, gradients are **unscaled** back to normal.

---

### Basic Usage

```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters())
scaler = GradScaler()  # Default init_scale=2**16

for data, target in dataloader:
    optimizer.zero_grad()

    # 1. Autocast for forward
    with autocast():
        output = model(data)
        loss = loss_fn(output, target)

    # 2. Scale loss and backward
    scaler.scale(loss).backward()

    # 3. Unscale + optimizer step
    scaler.step(optimizer)

    # 4. Update the scale for next iteration
    scaler.update()
```

---

### Key Methods

| Method | Purpose |
|-------|--------|
| `scaler.scale(loss)` | Scales the loss before `.backward()` |
| `scaler.step(optimizer)` | Unscales grads and calls `optimizer.step()` |
| `scaler.update()` | Adjusts scaling factor for next iteration |
| `scaler.unscale_(optimizer)` | Manually unscale grads (rarely needed) |
| `scaler.get_scale()` | Returns current scale factor |

---

### How Scaling Works (Internally)

1. **Initial scale**: Usually `2**16 = 65536`
2. After `backward()`, checks for **inf/NaN** in gradients.
3. If **no inf/NaN** → scale may **increase** (e.g., ×2) next time.
4. If **inf/NaN found** → skip `optimizer.step()`, **decrease scale** (e.g., ÷2), and retry later.

This makes training **robust** to occasional overflow.

---

### Common Parameters

```python
scaler = GradScaler(
    init_scale=2.**16,     # Starting scale
    growth_factor=2.0,     # Multiply when no inf
    backoff_factor=0.5,    # Divide when inf
    growth_interval=2000,  # Steps before growing scale
    enabled=True
)
```

---

### Example with Gradient Clipping

```python
scaler.scale(loss).backward()
scaler.unscale_(optimizer)  # Need to unscale before clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
scaler.step(optimizer)
scaler.update()
```

> **Note**: Always `unscale_` **before** clipping or inspecting gradients.

---

### Best Practices

- Use with `torch.cuda.amp.autocast()`
- Wrap **only forward + loss** in `autocast()`
- Call `scaler.update()` **every iteration**
- Use `torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction=True` for speed

---

### When Not to Use

- Pure `float32` training
- CPU training
- Custom training loops that manually handle scaling

---

### Official Docs

[https://pytorch.org/docs/stable/amp.html#torch.cuda.amp.GradScaler](https://pytorch.org/docs/stable/amp.html#torch.cuda.amp.GradScaler)

---

Let me know if you want a full training loop example or comparison with manual scaling!
