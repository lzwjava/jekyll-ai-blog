---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch cat 函数与数字示例
translated: true
type: note
---

问题：能否用具体数值（而非仅形状）展示 `torch.cat` 的用法？

答案：

```python
import torch

a = torch.tensor([[1., 2., 3.],
                   [4., 5., 6.]])   # 形状 (2,3)

b = torch.tensor([[7., 8., 9.],
                   [10., 11., 12.]]) # 形状 (2,3)

print(torch.cat([a, b], dim=0))
```

`dim=0` → 沿行方向拼接（行直接追加在下方）：
```
tensor([[ 1.,  2.,  3.],
        [ 4.,  5.,  6.],
        [ 7.,  8.,  9.],
        [10., 11., 12.]])   # 形状 (4, 3)
```

```python
print(torch.cat([a, b], dim=1))
```

`dim=1` → 沿列方向拼接（`a`的每一行右侧拼接`b`的对应行）：
```
tensor([[ 1.,  2.,  3.,  7.,  8.,  9.],
        [ 4.,  5.,  6., 10., 11., 12.]])   # 形状 (2, 6)
```

直观理解：`dim=0`沿第一个轴（行块索引）扩展，`dim=1`沿第二个轴（行内索引）扩展。选择的维度就是增长的维度（dim0时2+2=4，dim1时3+3=6）；其他所有维度必须事先匹配。

实际案例——KV缓存的具体实现：
```python
# k_cache: (batch=1, heads=2, seq=3, head_dim=4)
k_cache = torch.zeros(1, 2, 3, 4)
k_new   = torch.ones(1, 2, 1, 4)  # 一个新token

k_cache = torch.cat([k_cache, k_new], dim=2)  # 序列长度维度增长：3 -> 4
print(k_cache.shape)  # torch.Size([1, 2, 4, 4])
```
除`dim=2`（序列长度）外所有维度都匹配，而该维度正是你追加新token的维度。