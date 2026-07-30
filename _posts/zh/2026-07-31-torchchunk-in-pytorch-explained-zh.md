---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中torch.chunk详解
translated: true
type: note
---

问题：PyTorch中 `torch.chunk` 的作用是什么？

回答：沿给定维度将张量分割成指定数量的块。如果维度大小无法均匀分割，则所有块大小相等，最后一个块较小。

```python
import torch

x = torch.arange(10)
chunks = torch.chunk(x, 3)  # 沿 dim=0 分割成3块
for c in chunks:
    print(c, c.shape)

# tensor([0, 1, 2, 3]) torch.Size([4])
# tensor([4, 5, 6, 7]) torch.Size([4])
# tensor([8, 9])       torch.Size([2])   <- 最后一个块较小，不相等
```

关键签名：

```python
torch.chunk(input, chunks, dim=0)
```

- `chunks`：请求的块数量。如果维度大小太小，实际得到的块数可能**少于**这个值（永远不会更多）。
- 与 `torch.split` 不同，这里指定的是块的*数量*，而非每个块的*大小*。
- 返回视图元组（尽可能不复制）——使用相同的底层存储，因此如果数据是连续的且共享内存，原地修改一个块可能会改变原始张量。

在实际 Transformer 代码中你会遇到的用法——分割 QKV 投影：

```python
qkv = torch.randn(2, 10, 3 * 768)  # (batch, seq, 3*d_model)
q, k, v = qkv.chunk(3, dim=-1)     # 每个 (2, 10, 768)
```

这是注意力机制实现中的标准模式（例如 GPT-2 的 `c_attn` 输出）——一次大的线性投影，然后通过 `chunk(3, dim=-1)` 分割成 Q、K、V，而不是使用三个独立的线性层。

注意事项：如果 `dim_size % chunks != 0`，则块大小不均匀（基于向上取整），而 `torch.split(x, size)` 允许你控制每个分割的确切大小，`torch.tensor_split` 则保证在无法均匀分割时也能恰好得到 `n` 个块（将剩余部分重新分配到前几个块中，而不是全部堆积在最后一个块中）。

参考资料：

- [torch.chunk — PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.chunk.html)
- [torch.tensor_split — PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.tensor_split.html)
