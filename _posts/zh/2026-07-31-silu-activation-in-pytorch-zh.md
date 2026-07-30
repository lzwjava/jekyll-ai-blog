---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中的SiLU激活
translated: true
type: note
---

问题：在PyTorch中，`F.silu(x)` 是什么意思？

回答：

SiLU（Sigmoid Linear Unit，即 Swish）：

```
silu(x) = x * sigmoid(x) = x / (1 + exp(-x))
```

```python
import torch
import torch.nn.functional as F

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
print(F.silu(x))
# tensor([-0.2384, -0.2689,  0.0000,  0.7311,  1.7616])

# 手动等效实现
def silu(x):
    return x * torch.sigmoid(x)

print(silu(x))  # 结果相同
```

形状：当 `x < 0` 时，它会略微下降到负值（最小值约 -0.278，出现在 x ≈ -1.278 处），然后上升，这与 ReLU 的硬零不同。函数平滑、非单调、处处可微——在零附近比 ReLU 有更好的梯度流动，没有神经元死亡问题。

导数：

```
silu'(x) = sigmoid(x) + x * sigmoid(x) * (1 - sigmoid(x))
         = silu(x) + sigmoid(x) * (1 - silu(x))
```

实际应用场景：SwiGLU 出现在 LLaMA / Mistral / Qwen 的 MLP 模块中——

```python
def swiglu(x, W, V, W2):
    return (F.silu(x @ W) * (x @ V)) @ W2
```

这就是为什么它对你很重要——你在 MI300X 上训练的每一个现代 Transformer MLP 都使用这个，而不是普通的 GELU-MLP。`F.silu` 字面意义上就是那个模块中的门控激活函数。

参考资料：

- [torch.nn.functional.silu 文档](https://pytorch.org/docs/stable/generated/torch.nn.functional.silu.html)
- [SwiGLU 论文 —— Shazeer, GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202)
