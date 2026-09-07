---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解Triton的cdiv
translated: true
type: note
---

问题：`triton.cdiv` 是什么意思？

答案：`triton.cdiv` 在 Triton 中表示**向上取整除法**。

```python
triton.cdiv(x, y)
```

计算：

$$
\left\lceil \frac{x}{y} \right\rceil
$$

等效 Python 代码：

```python
(x + y - 1) // y
```

### 示例

```python
triton.cdiv(100, 32)
# 4
```

因为：

$$
100 / 32 = 3.125 \rightarrow \lceil3.125\rceil = 4
$$

这在 GPU 内核中计算**需要多少个 block/warp** 时极为常见：

```python
BLOCK_SIZE = 256
num_blocks = triton.cdiv(n, BLOCK_SIZE)
```

如果 `n = 1000`：

```text
1000 个元素
÷ 256 元素/block
= 3.90625 blocks
→ 4 blocks
```

关键区别：

```python
n // BLOCK_SIZE       # 向下取整除法 → 可能太小
triton.cdiv(n, BLOCK_SIZE)  # 向上取整除法 → 覆盖所有
```

在 LLM/Triton 代码中，你会在诸如**序列长度、token、行数和 tile** 等场景中频繁看到它。

我也可以带你深入一个真实的 Triton 内核，精确展示为什么 `cdiv` 会出现在网格计算中。