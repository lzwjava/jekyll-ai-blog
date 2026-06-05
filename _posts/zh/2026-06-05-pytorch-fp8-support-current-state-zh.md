---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch FP8 支持现状
translated: true
type: note
---

问题：PyTorch 对 FP8 的支持情况如何？

答案：

PyTorch 在最新版本中已提供**原生 FP8 支持**，但仍在不断完善中。以下是当前状态：

**已有功能**

PyTorch 通过 `torch.float8_e4m3fn` 和 `torch.float8_e5m2` 数据类型支持 FP8。关键 API 如下：

```python
import torch

# 转换为 FP8
x_fp8 = x.to(torch.float8_e4m3fn)  # E4M3：精度更高，适用于权重/激活
x_fp8 = x.to(torch.float8_e5m2)    # E5M2：范围更广，适用于梯度

# 检查可用性
print(torch.cuda.is_bf16_supported())  # 在 RTX 4070 上返回 True
```

**torch.float8_experimental**

主要 FP8 训练路径通过 `torch.float8_experimental` 实现：

```python
from torchao.float8 import convert_to_float8_training

# 将模型转换为 FP8
model = convert_to_float8_training(model)

# 或使用上下文管理器
with torch.autocast("cuda", dtype=torch.float8_e4m3fn):
    output = model(input)
```

**使用 torchao 进行 FP8 训练**

目前最实用的方式：

```bash
pip install torchao
```

```python
from torchao.float8 import convert_to_float8_training

model = YourModel()
model = convert_to_float8_training(model)

# 训练循环照常运行
optimizer = torch.optim.AdamW(model.parameters())
for batch in dataloader:
    loss = model(batch).sum()
    loss.backward()
    optimizer.step()
```

**当前限制**

1. **硬件支持**：FP8 需要 Ada Lovelace（RTX 4090+）或 Hopper（H100）架构。RTX 4070 拥有 Tensor Core，但 PyTorch 的 FP8 内核尚未针对其完全优化。

2. **内核成熟度**：FP8 内核主要在 H100/RTX 4090 上测试。在 RTX 4070 上的性能表现不稳定。

3. **梯度累积**：FP8 梯度需要谨慎处理——使用 FP16/BF16 梯度的混合精度更稳定。

4. **torch.compile 兼容性**：FP8 与 `torch.compile()` 配合使用可实现内核融合，但编译开销可能会抵消小型模型的增益。

**当前运行良好的场景**

对于您的 RTX 4070 + nanoGPT 配置：

```python
# 最佳方式：BF16 混合精度
scaler = torch.amp.GradScaler()
with torch.amp.autocast("cuda", dtype=torch.bfloat16):
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
```

**真实情况**

PyTorch 的 FP8 支持在 **H100 上已可用于生产环境**，在 **RTX 4090 上仍处于实验阶段**，在 **RTX 4070 上并不可靠**。生态发展迅速——`torchao` 和 `torch.float8_experimental` 是值得关注的方向。

对于您当前的工作负载：**坚持使用 BF16**。在 RTX 4070 上使用 FP8 目前还不值得投入调试时间。

参考：

- [PyTorch FP8 RFC](https://github.com/pytorch/pytorch/issues/89364)
- [torchao FP8 文档](https://github.com/pytorch/ao)
- [torch.float8_experimental](https://github.com/pytorch-labs/torchao-experimental)
