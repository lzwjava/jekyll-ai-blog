---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 独热Softmax梯度问题
translated: true
type: note
---

**问题：** 在未缩放的注意力机制中，"独热软最大化"是什么意思？为什么会导致梯度问题？

**答案：**

独热向量是指一个向量中某个元素（接近）为1，其余元素（接近）为0。

在未缩放的注意力机制中：

- 点积取值范围为[-500, 500]（数值较大）
- `softmax(z) = exp(z) / sum(exp(z))` 会呈指数级放大这些差异
- 某个词元的注意力权重将接近0.99999，其余词元接近0.00001

**导致梯度消失的原因：**

Softmax 梯度计算如下：

```
dL/dq_i = dL/d(softmax) * d(softmax)/dq_i
```

对于 Softmax，每个元素的雅可比矩阵为：

```
∂softmax_j / ∂z_i = softmax_j * (δ_ij - softmax_i)
```

当 Softmax 呈独热状态时（例如 softmax_j ≈ 1，其余 ≈ 0）：

- 对于主导位置：`∂softmax_j / ∂z_j = 1 * (1 - 1) = 0`
- 对于其他位置：`∂softmax_k / ∂z_i ≈ 0 * (0 - 1) ≈ 0`

**结果：** 所有梯度趋近于0。查询、键和值的投影层都将获得消失梯度。

**缩放机制如何解决该问题：**

使用 `scale = 1/√d_k` 时：

- 点积取值范围变为[-2, 2]（Softmax 保持"柔化"）
- 多个词元可获得非零的注意力权重
- 梯度能够流经所有位置

```python
# 未缩放：attention_weights ≈ [0.99999, 0.00001, 0.00000]
# 各维度的 dL/dq 均收缩至接近零

# 缩放后：attention_weights ≈ [0.68, 0.24, 0.08]
# dL/dq 可通过多条路径实现非零传播
```

这就是Transformer论文采用`d_k = 64`并缩放`1/√64 = 0.125`的原因——使点积保持在[−√d_k, √d_k]范围内，从而确保Softmax保持可微性。
