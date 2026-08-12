---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中的连续内存
translated: true
type: note
---

问题：在 PyTorch 中，`contiguous` 是什么意思？

答案：

在 PyTorch 中，**contiguous** 意味着张量的元素按照其**逻辑顺序存储在连续的内存块中**。

张量包含：

1. **shape** —— 数据的视图方式
2. **stride** —— PyTorch 在内存中跳跃访问元素的方式
3. **storage** —— 实际的内存缓冲区

示例：

```python
import torch

x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])

print(x.stride())
print(x.is_contiguous())
```

输出：

```
(3, 1)
True
```

内存布局：

```
memory:
[1][2][3][4][5][6]

row 0: start + 0,1,2
row 1: start + 3,4,5
```

步长 `(3,1)` 表示：

* 移动一列 → 跳过 1 个元素
* 移动一行 → 跳过 3 个元素

这是常见的 C 风格行优先布局。

---

关键情形出现在使用 `transpose` 时：

```python
x = torch.tensor([[1,2,3],
                  [4,5,6]])

y = x.T

print(y)
print(y.stride())
print(y.is_contiguous())
```

输出：

```
tensor([[1,4],
        [2,5],
        [3,6]])

stride: (1,3)
contiguous: False
```

为什么？

`y` 并未被复制。PyTorch 只改变了**视图**：

原始内存：

```
[1][2][3][4][5][6]
```

`x`：

```
1 2 3
4 5 6
```

`y = x.T`：

```
1 4
2 5
3 6
```

要按行读取 `y`：

```
1 -> 跳过 3 -> 4
2 -> 跳过 3 -> 5
3 -> 跳过 3 -> 6
```

内存顺序与张量顺序不匹配，因此是非 contiguous 的。

---

某些操作需要 contiguous 内存。

示例：

```python
y = x.T

y.view(-1)
```

可能会失败：

```
RuntimeError: view size is not compatible with input tensor's size and stride
```

因为 `view()` 仅在现有内存布局能表示新形状时才有效。

解决方法：

```python
y = x.T.contiguous()

z = y.view(-1)
```

`contiguous()` 会进行真正的复制：

之前：

```
x storage:
[1][2][3][4][5][6]

y:
1 4
2 5
3 6

（无新内存）
```

之后：

```
new storage:
[1][4][2][5][3][6]
```

现在张量顺序与内存顺序一致。

---

在 Transformer 代码中经常出现：

```python
q = q.transpose(1, 2)
q = q.contiguous()
q = q.view(batch, seq, hidden)
```

典型流程：

```
(B, heads, seq, head_dim)
        |
        transpose
        v
(B, seq, heads, head_dim)
        |
        contiguous
        |
        view
        v
(B, seq, hidden)
```

`transpose()` 改变步长而不复制；`contiguous()` 重新排列内存，以便后续 `view()` 或 CUDA 内核能高效运行。

一个有用的思维模型：

```
view()
  = 改变对内存的解释方式

transpose()
  = 改变步长（通常不复制）

contiguous()
  = 创建与当前视图匹配的新内存布局
```

在现代 PyTorch 中，许多操作会自动处理非 contiguous 张量，但对性能敏感的内核（尤其是注意力、matmul、融合操作中的 CUDA 内核）通常更偏好 contiguous 布局。
