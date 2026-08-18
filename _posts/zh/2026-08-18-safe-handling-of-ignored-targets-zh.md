---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安全处理被忽略的目标
translated: true
type: note
---

问题：解释这段处理 `ignore_index` 目标（如 `-1`）的 PyTorch 代码路径。

答案：

核心思想是：

> **某些目标 token 是无效/被忽略的（`y < 0`），因此我们绝不能使用它们来索引 `token_bytes`。**

让我们逐行分析。

### 1. 为什么需要这种特殊情况？

假设：

```python
y = tensor([10, 20, -1, 30])
```

其中 `-1` 表示**忽略此目标**。

以及：

```python
token_bytes = tensor([...])
```

其中：

```python
token_bytes[token_id]
```

返回该 token 所表示的 UTF-8 字节数。

通常我们会这样做：

```python
num_bytes = token_bytes[y]
```

对于：

```python
y = [10, 20, 30]
```

这是没问题的。

但：

```python
y = [10, 20, -1, 30]
```

很危险，因为：

```python
token_bytes[-1]
```

在 PyTorch 中表示**最后一个元素**，而不是"无效"。

所以 `-1` 会意外地变成一个真正的 token 索引。

---

## 2. 为什么用这奇怪的第一行？

```python
if (y.int() < 0).any():
```

分解来看：

```python
y.int()
```

将 `y` 转换为 `int32`。

然后：

```python
y.int() < 0
```

生成一个布尔型张量：

```text
y              = [10, 20, -1, 30]

y.int() < 0    = [F,  F,  T,  F]
```

然后：

```python
.any()
```

询问：

> 是否存在**任意**元素满足 `< 0`？

所以：

```python
(y.int() < 0).any()
```

返回：

```text
True
```

注释中提到，这特指苹果的 **MPS 后端** 目前缺少所需的 `int64 < 0` 内核，而 `int32` 可以工作。

---

# 3. 创建有效性掩码

```python
valid = y >= 0
```

对于：

```python
y = [10, 20, -1, 30]
```

我们得到：

```text
valid = [True, True, False, True]
```

可以理解为：

```text
token 10   → 使用
token 20   → 使用
token -1   → 忽略
token 30   → 使用
```

---

# 4. 将无效索引替换为 0

这是一个重要的技巧：

```python
y_safe = torch.where(
    valid,
    y,
    torch.zeros_like(y)
)
```

`torch.where(condition, a, b)` 的含义是：

```text
if condition:
    取 a
else:
    取 b
```

因此：

```text
valid  = [T, T, F, T]
y      = [10,20,-1,30]
```

变为：

```text
y_safe = [10,20, 0,30]
```

注意：

```text
-1 → 0
```

为什么？

因为现在这样做是安全的：

```python
token_bytes[y_safe]
```

我们永远不会这样做：

```python
token_bytes[-1]
```

---

# 5. 查找字节长度

现在：

```python
token_bytes[y_safe]
```

可能会产生：

```text
token_bytes[y_safe]
    ↓
[3, 4, 1, 2]
```

但请记住：

```text
位置 2 原本是 -1
```

所以我们从：

```python
token_bytes[0]
```

得到的 `1` 是毫无意义的。

我们需要把它变回零。

这就是下面这行代码的作用：

```python
num_bytes2d = torch.where(
    valid,
    token_bytes[y_safe],
    torch.zeros_like(y, dtype=token_bytes.dtype)
)
```

结果：

```text
valid                 [T, T, F, T]
token_bytes[y_safe]   [3, 4, 1, 2]
                         ↓
num_bytes2d            [3, 4, 0, 2]
```

因此被忽略的 token 贡献了**零字节**。

---

# 6. 同时忽略其损失

然后：

```python
total_nats += (loss2d * (num_bytes2d > 0)).sum()
```

假设：

```text
loss2d       = [0.5, 1.2, 9.8, 0.7]
num_bytes2d  = [3,   4,   0,   2]
```

那么：

```python
num_bytes2d > 0
```

得到：

```text
[True, True, False, True]
```

所以：

```python
loss2d * (num_bytes2d > 0)
```

变为：

```text
[0.5, 1.2, 0.0, 0.7]
```

被忽略目标的损失被去除了。

因此：

```text
total_nats = 0.5 + 1.2 + 0.7
```

---

# 7. 只计算有效字节

最后：

```python
total_bytes += num_bytes2d.sum()
```

对于：

```text
num_bytes2d = [3, 4, 0, 2]
```

我们得到：

```text
total_bytes += 9
```

被忽略的 token 贡献：

```text
0 字节
```

---

## 整体流程

你可以在脑子里将整个代码块简化为：

```python
y = [10, 20, -1, 30]

# -1 表示"忽略"
```

### 步骤 1 —— 识别有效目标

```text
valid:
[ True, True, False, True ]
```

### 步骤 2 —— 使索引安全

```text
y:
[10, 20, -1, 30]

y_safe:
[10, 20,  0, 30]
```

### 步骤 3 —— 查找字节长度

```text
token_bytes[y_safe]:
[3, 4, 1, 2]
```

### 步骤 4 —— 抹去被忽略 token 的虚假查找结果

```text
num_bytes2d:
[3, 4, 0, 2]
```

### 步骤 5 —— 对损失使用相同的掩码

```text
loss2d:
[0.5, 1.2, 9.8, 0.7]

mask:
[1, 1, 0, 1]

effective loss:
[0.5, 1.2, 0, 0.7]
```

因此不变的原则是：

```text
y < 0
  ↓
无效目标
  ↓
不要用它索引
  ↓
替换为安全索引 0
  ↓
将其字节数设为 0
  ↓
其损失被忽略
```

### 为什么不直接这样做？

你可能会想，为什么不直接写：

```python
num_bytes2d = token_bytes[y]
```

然后再应用掩码。

因为**索引操作发生在掩码之前**：

```python
token_bytes[-1]
```

已经执行了。

因此关键的模式是：

```python
y_safe = torch.where(y >= 0, y, 0)

lookup = token_bytes[y_safe]

result = torch.where(
    y >= 0,
    lookup,
    0
)
```

这是一种非常常见的 GPU 编程模式：

> **先净化索引 → 执行 gather/indexing → 之后再掩码无效结果。**

一个细微之处：`loss2d * (num_bytes2d > 0)` 在这里实际上充当了忽略掩码，因为有效的 token 具有正的字节长度。实际语义上的真实来源是 `valid`；使用 `num_bytes2d > 0` 之所以有效，是因为 `num_bytes2d` 被构造为对于被忽略的目标恰好为零。
