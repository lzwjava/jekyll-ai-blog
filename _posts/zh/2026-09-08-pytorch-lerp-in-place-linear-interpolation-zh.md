---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch lerp_ 原地线性插值
translated: true
type: note
---

问题：在Python（特别是PyTorch）中，`lerp_` 是什么意思？

答案：

`lerp_` 是 `lerp`（线性插值）的**原地操作版本**。

**`lerp` 公式：**

```
result = start + weight * (end - start)
```

或者等价地：

```
result = (1 - weight) * start + weight * end
```

末尾的下划线 `_` 是 **PyTorch 的约定**，表示该操作会**原地**修改张量（不会分配新张量）。

**示例：**

```python
import torch

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([10.0, 20.0, 30.0])

# 原地操作：a 被直接修改
a.lerp_(b, weight=0.5)
# a 现在为：tensor([5.5, 11.0, 16.5])
# = 1 + 0.5*(10-1), 2 + 0.5*(20-2), 3 + 0.5*(30-3)
```

**对比非原地版本：**

```python
result = torch.lerp(a, b, weight=0.5)  # 返回新张量，a 不变
a.lerp_(b, weight=0.5)                 # 直接修改 a
```

**常见用途：**

- 平滑过渡 / 动画
- 模型权重平均（例如 EMA——指数移动平均）
- 机器学习训练循环中的数值混合

参考：

- [torch.lerp — PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.lerp.html)
