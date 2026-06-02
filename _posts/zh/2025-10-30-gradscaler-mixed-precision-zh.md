---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 混合精度训练中的梯度缩放器
translated: true
type: note
---

`torch.cuda.amp.GradScaler` 是 PyTorch 的一个工具类，旨在使用**自动混合精度（AMP）**进行混合精度训练时**自动缩放梯度**。它有助于防止使用 `float16`（半精度）张量时梯度下溢，否则梯度可能变得过小而无法精确表示。

---

### 为什么使用 `GradScaler`？

在混合精度训练中：
- **前向/反向传播**使用 `float16` 以节省速度和内存。
- 用 `float16` 计算的梯度可能变得非常小 → **下溢为零**。
- `GradScaler` 在反向传播之前将**损失**按一个因子（例如 2¹⁵ = 32768）进行缩放。
- 梯度按比例缩放 → 保持在可表示的范围内。
- 在优化器步骤之前，梯度被**反缩放**回正常范围。

---

### 基本用法

```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters())
scaler = GradScaler()  # 默认 init_scale=2**16

for data, target in dataloader:
    optimizer.zero_grad()

    # 1. 使用 autocast 进行前向传播
    with autocast():
        output = model(data)
        loss = loss_fn(output, target)

    # 2. 缩放损失并执行反向传播
    scaler.scale(loss).backward()

    # 3. 反缩放 + 优化器步骤
    scaler.step(optimizer)

    # 4. 更新缩放因子以备下一次迭代
    scaler.update()
```

---

### 关键方法

| 方法 | 用途 |
|-------|--------|
| `scaler.scale(loss)` | 在 `.backward()` 之前缩放损失 |
| `scaler.step(optimizer)` | 反缩放梯度并调用 `optimizer.step()` |
| `scaler.update()` | 为下一次迭代调整缩放因子 |
| `scaler.unscale_(optimizer)` | 手动反缩放梯度（很少需要） |
| `scaler.get_scale()` | 返回当前缩放因子 |

---

### 缩放工作原理（内部）

1. **初始缩放因子**：通常为 `2**16 = 65536`
2. 在 `backward()` 之后，检查梯度中是否存在 **inf/NaN**。
3. 如果**没有 inf/NaN** → 下次缩放因子可能**增加**（例如 ×2）。
4. 如果**发现 inf/NaN** → 跳过 `optimizer.step()`，**减小缩放因子**（例如 ÷2），并在稍后重试。

这使得训练对偶尔的溢出具有**鲁棒性**。

---

### 常用参数

```python
scaler = GradScaler(
    init_scale=2.**16,     # 起始缩放因子
    growth_factor=2.0,     # 无 inf 时倍增
    backoff_factor=0.5,    # 有 inf 时折半
    growth_interval=2000,  # 增长前的步数
    enabled=True
)
```

---

### 梯度裁剪示例

```python
scaler.scale(loss).backward()
scaler.unscale_(optimizer)  # 裁剪前需要反缩放
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
scaler.step(optimizer)
scaler.update()
```

> **注意**：在裁剪或检查梯度之前，务必先进行 `unscale_`。

---

### 最佳实践

- 与 `torch.cuda.amp.autocast()` 配合使用
- 仅在**前向传播 + 损失计算**时使用 `autocast()`
- **每次迭代**都调用 `scaler.update()`
- 使用 `torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction=True` 以提升速度

---

### 不适用的场景

- 纯 `float32` 训练
- CPU 训练
- 手动处理缩放的自定义训练循环

---

### 官方文档

[https://pytorch.org/docs/stable/amp.html#torch.cuda.amp.GradScaler](https://pytorch.org/docs/stable/amp.html#torch.cuda.amp.GradScaler)

---

如果需要完整的训练循环示例或与手动缩放的比较，请告诉我！
