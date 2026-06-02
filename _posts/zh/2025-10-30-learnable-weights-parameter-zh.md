---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: PyTorch可学习权重参数
translated: true
type: note
---

`torch.nn.Parameter` 是 PyTorch 中 `torch.Tensor` 的一个子类，专门用于表示神经网络模块中的可学习参数。其主要作用是在将张量作为属性分配给 `torch.nn.Module` 时，自动将其注册为模块参数，从而可以通过 `module.parameters()` 或 `module.named_parameters()` 等方法进行访问。这有助于区分可训练权重（例如各层的权重）与常规张量，避免临时计算张量（如 RNN 中的缓存状态）被错误地视作参数。

### 核心特性

- **自动注册**：当将 `Parameter` 分配给模块时（例如在自定义模块的 `__init__` 中执行 `self.weight = nn.Parameter(torch.randn(3, 3))`），它会自动添加到模块的参数列表中，无需额外代码。
- **梯度追踪**：默认设置 `requires_grad=True`，因此会参与反向传播。即使在 `torch.no_grad()` 上下文中也是如此——如需更精细控制，可使用 autograd 的局部禁用功能。
- **属性**：它继承所有 `Tensor` 属性，除特殊的模块行为外不添加新属性。

### 基础用法

以下是一个自定义模块中的简单示例：

```python
import torch
import torch.nn as nn

class MyModule(nn.Module):
    def __init__(self):
        super().__init__()
        # 该张量会自动注册为参数
        self.weight = nn.Parameter(torch.randn(2, 3))
        # 普通张量不会被注册
        self.bias = torch.zeros(3)

    def forward(self, x):
        return x @ self.weight + self.bias

model = MyModule()
print(list(model.parameters()))  # 输出: [Parameter containing: tensor(...)]
```

更多细节请参阅官方文档：[Parameter — PyTorch 2.9 documentation](https://pytorch.org/docs/stable/generated/torch.nn.parameter.Parameter.html)
