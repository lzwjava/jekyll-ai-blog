---
audio: false
generated: true
image: false
lang: zh
layout: post
title: F.嵌入是功能嵌入
translated: true
type: note
---

问题：当通过 `import torch.nn.functional as F` 导入时，`F.embedding` 是否指向 `torch.nn.functional.embedding`？

答案：是的。`F.embedding(input, weight, ...)` 是 `nn.Embedding` 的函数形式。它仅仅是对权重矩阵的索引/聚集查找——本身没有可学习的状态，你需要传入权重张量。

```python
import torch
import torch.nn.functional as F

weight = torch.randn(10, 4)  # vocab_size=10, embed_dim=4
input_ids = torch.tensor([1, 3, 5])

out = F.embedding(input_ids, weight)
# 等价于: weight[input_ids]
print(out.shape)  # torch.Size([3, 4])
```

`nn.Embedding` 只是一个轻量级的模块封装，它将 `weight` 存储为 `nn.Parameter`，并在其 `forward` 方法内部调用 `F.embedding`：

```python
class Embedding(nn.Module):
    def forward(self, input):
        return F.embedding(input, self.weight, self.padding_idx, ...)
```

签名：`F.embedding(input, weight, padding_idx=None, max_norm=None, norm_type=2.0, scale_grad_by_freq=False, sparse=False)`。底层实现是 `torch.embedding`，一个执行 index_select 风格聚集的 C++/CUDA 操作——不是矩阵乘法，因为输入是 token 索引而非 one-hot 向量。

参考：
- [torch.nn.functional.embedding — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.embedding.html)
- [torch.nn.Embedding — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)