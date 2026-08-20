---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch 原地 lerp 解释
translated: true
type: note
---

问题：`lerp_` 是什么意思？

答案：`lerp_` 是一种**原地线性插值**操作，常见于 PyTorch 等框架中。

- `lerp` 代表**线性插值**——根据权重参数 `t` 计算两个点之间的值：

```
result = start + t * (end - start)
```

- 末尾的**下划线 `_`** 是一种约定（尤其在 PyTorch 中），表示该操作是**原地执行**的，即直接修改张量本身而不是返回新张量。

因此 `tensor.lerp_(end, weight)` 等价于：

```
tensor = tensor + weight * (end - tensor)
```

其中 `weight` 是 0.0 到 1.0 之间的标量：

- `weight = 0.0` → 结果等于原张量
- `weight = 1.0` → 结果等于 `end`
- `weight = 0.5` → 结果为中点值

常见用途包括平滑动画、模型权重混合以及基于梯度的优化。

参考资料：

- [PyTorch torch.lerp 文档](https://pytorch.org/docs/stable/generated/torch.lerp.html)
- [线性插值 — 维基百科](https://en.wikipedia.org/wiki/Linear_interpolation)
