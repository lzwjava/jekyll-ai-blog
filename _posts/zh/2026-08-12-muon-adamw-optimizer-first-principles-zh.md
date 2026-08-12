---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muon-AdamW优化器第一性原理
translated: true
type: note
---

问题：**如何从基本原理理解这个 Muon + AdamW 优化器的实现？**

答案：

最简单的方法**不是把这当作 600 行 PyTorch 代码来读**。把它缩减成一幅概念图：

```text
                   梯度 g
                       │
             ┌─────────┴─────────┐
             │                   │
        embedding/标量          2-D 矩阵
             │                   │
           AdamW                 Muon
             │                   │
             │         动量 / Nesterov
             │                   │
             │             正交化
             │                   │
             │         方差归一化
             │                   │
             └─────────┬─────────┘
                       │
                 更新参数
```

核心思想是：

> **AdamW 主要按元素逐个处理参数张量。Muon 将 2-D 权重矩阵视为几何对象，并改变其更新的*形状/方向*。**

源码本身也说明，这个组合优化器对 embedding/标量使用 AdamW，对矩阵参数使用 Muon。

---

## 1. 从普通梯度下降开始

假设神经网络权重矩阵为

[
W \in \mathbb{R}^{768\times3072}
]

反向传播得到

[
G=\frac{\partial L}{\partial W}.
]

最简单的优化器是：

[
W \leftarrow W-\eta G
]

其中：

* (W) = 当前权重
* (G) = 梯度
* (\eta) = 学习率

这个文件中的所有内容最终都基于这个基本方程。

---

# 2. AdamW 的思想

AdamW 维护两个记忆：

[
m_t \approx \text{平均梯度}
]

和

[
v_t \approx \text{平均梯度平方}.
]

代码中：

```python
exp_avg32.lerp_(grad32, 1 - beta1_t)
exp_avg_sq32.lerp_(grad32.square(), 1 - beta2_t)
```

数学上近似为：

[
m_t=\beta_1m_{t-1}+(1-\beta_1)G_t
]

[
v_t=\beta_2v_{t-1}+(1-\beta_2)G_t^2.
]

然后：

[
\Delta W
========

-\eta
\frac{m_t}{\sqrt{v_t}+\epsilon}.
]

这就是 Adam 的基本思想。

该实现还应用了解耦权重衰减：

[
W\leftarrow (1-\eta\lambda)W.
]

这正是第 48–59 行做的事。

---

# 3. Muon 的起点不同

Muon 的有趣之处在于它说：

> 如果 (G) 是一个矩阵，不一定要直接用原始矩阵 (G) 作为更新。

假设

[
G=
\begin{bmatrix}
1 & 0\\
0 & 0.01
\end{bmatrix}.
]

标准 SGD 会给出：

[
\Delta W=-\eta
\begin{bmatrix}
1&0\\
0&0.01
\end{bmatrix}.
]

因此一个方向得到的更新比另一个方向大 100 倍。

Muon 则尝试**重塑/正交化更新**。

---

# 4. Muon 最重要的概念：正交化

这是文件的核心。

代码中说：

```python
X = g

...

X = X / (X.norm(...) * 1.01 + 1e-6)

A = X.mT @ X
B = b * A + c * (A @ A)
X = a * X + X @ B
```

这是对**极分解**的迭代近似。

对于矩阵

[
G=U\Sigma V^T,
]

Muon 想要得到近似

[
UV^T.
]

注意发生了什么：

[
G=U\Sigma V^T
]

包含奇异值

[
\Sigma=
\begin{bmatrix}
\sigma_1&&\\
&\sigma_2&\\
&&\cdots
\end{bmatrix}.
]

极因子

[
UV^T
]

实际上**去掉了奇异值的缩放**。

源码明确描述这是将更新替换为最近的正交矩阵。

---

# 5. 为什么这很有趣？

将矩阵梯度视为包含两种信息：

```text
G
│
├── 方向 / 朝向
│
└── 奇异值大小
```

SVD：

[
G=U\Sigma V^T
]

Muon 大致将其变换为：

[
G
\rightarrow
UV^T.
]

所以它在说：

> “我关心这次更新的有用几何方向，但我不希望它的奇异值完全决定更新幅度。”

这就是与 AdamW 的概念差异。

---

# 6. 一个非常小的例子

假设

[
G=
\begin{bmatrix}
10&0\\
0&1
\end{bmatrix}.
]

SVD 给出：

[
U=I,\quad
\Sigma=
\begin{bmatrix}
10&0\\
0&1
\end{bmatrix},
\quad
V=I.
]

因此

[
UV^T=I.
]

Muon 将近似

[
\begin{bmatrix}
10&0\\
0&1
\end{bmatrix}
]

变为

[
\begin{bmatrix}
1&0\\
0&1
\end{bmatrix}.
]

所以它不再说：

```text
方向 1: 10
方向 2: 1
```

而是近似说：

```text
方向 1: 1
方向 2: 1
```

这就是几何直觉。

---

# 7. 但它们并没有真正计算 SVD

这一点很重要。

你可能会认为实现会做：

```python
U, S, V = torch.linalg.svd(G)
G = U @ V.T
```

但并没有。

那样做代价太高。

相反，它使用了 **Newton-Schulz / Polar Express 迭代**。

文件中有五个系数元组：

```python
polar_express_coeffs = [
    (...),
    (...),
    (...),
    (...),
    (...),
]
```

然后执行五次迭代。

源码明确说明：

> “Newton-Schulz 迭代，用于计算 G 的零次幂 / 正交化。”

所以概念上：

```text
G
 ↓
归一化
 ↓
迭代 1
 ↓
迭代 2
 ↓
迭代 3
 ↓
迭代 4
 ↓
迭代 5
 ↓
近似 polar(G)
```

巧妙之处在于这些操作主要是矩阵乘法，而 GPU 非常擅长这个。

---

# 8. 为什么是 `X.T @ X`？

假设

[
X\in\mathbb R^{m\times n}.
]

那么

[
X^TX\in\mathbb R^{n\times n}.
]

如果 (X) 在适当意义上是完全正交的，那么

[
X^TX\approx I.
]

所以迭代本质上是在尝试将 (X) 的奇异值推向 1。

这就是为什么这是一个**正交化过程**。

对于另一种形状，它使用

[
XX^T
]

代替：

```python
if g.size(-2) > g.size(-1):
    A = X.mT @ X
else:
    A = X @ X.mT
```

它选择较小一侧的 Gram 矩阵以降低计算成本。

---

# 9. 然后还有动量

Muon 并不直接正交化原始梯度。

首先：

```python
momentum_buffer.lerp_(stacked_grads, 1 - momentum)
g = stacked_grads.lerp_(momentum_buffer, momentum)
```

概念上：

[
M_t=\beta M_{t-1}+(1-\beta)G_t
]

然后一个 Nesterov 风格的组合产生有效梯度。

所以：

```text
原始梯度
     ↓
动量
     ↓
有效梯度
     ↓
正交化
```

源码将 Muon 描述为内部运行标准 SGD-动量，然后应用正交化后处理步骤。

---

# 10. 为什么只针对 2-D 矩阵？

因为这个几何思想自然适用于矩阵。

例如 Transformer：

```text
Wq : [hidden_size, hidden_size]
Wk : [hidden_size, hidden_size]
Wv : [hidden_size, hidden_size]
Wo : [hidden_size, hidden_size]
```

这些自然是矩阵。

Muon 说：

```text
2-D 矩阵
    ↓
将梯度视为矩阵
    ↓
正交化矩阵更新
```

但 embedding 表或标量不一定受益于这种处理。

因此：

```text
embedding
bias
标量
最终全连接层
        ↓
      AdamW
```

而：

```text
大型 2-D 权重矩阵
        ↓
      Muon
```

实现明确警告不要对 embedding、最终全连接层以及 0-D/1-D 参数使用 Muon。

---

# 11. 整个 Muon 更新

你可以在心里将整个 100 行的 `muon_step_fused()` 压缩为：

[
G_t
]

↓

### 动量

[
G'_t=\text{Momentum}(G_t)
]

↓

### 正交化

[
G''_t\approx \operatorname{polar}(G'_t)
]

↓

### 归一化更新尺度

↓

### 谨慎的权重衰减

↓

[
W_{t+1}
=======

W_t-\eta G''_t-\text{权重衰减}.
]

实际代码按以下阶段执行：

```python
# Nesterov 动量
...

# MuonEq
...

# Polar Express
...

# Muon+
...

# 方差缩减
...

# 权重衰减 + 更新
...
```

这就是你应该记在脑子里的结构。

---

# 12. `MuonEq` 在做什么？

这部分：

```python
target = X.float().norm(dim=(-2, -1), keepdim=True) / (X.size(-2) ** 0.5)

row_norm = X.float().norm(dim=-1, keepdim=True)

X = X * (target / row_norm)
```

基本上就是：

> 在正交化之前，让不同行具有可比较的范数。

想象一下：

```text
row 0  ███████████████
row 1  ██
row 2  █████████
row 3  █
```

MuonEq 试图在运行极迭代之前让行的尺度不那么病态。

源码将其描述为**行均衡**，以改善条件数。

---

# 13. `Muon+` 是什么？

正交化之后：

```python
target_norm = min(m, n) ** 0.5
current_norm = g.norm(...)
g = g * (target_norm / current_norm)
```

一个精确的半正交矩阵的 Frobenius 范数大约为

[
\sqrt{\min(m,n)}.
]

所以它们强制更新回到该范数。

换句话说：

```text
正交化
       ↓
可能尺度略有偏差
       ↓
重新归一化 Frobenius 范数
```

源码称此为 **Muon+ 重归一化**。

---

# 14. 然后是方差缩减

这部分更微妙：

```python
v_mean = g.float().square().mean(...)
second_momentum_buffer.lerp_(...)
step_size = second_momentum_buffer.clamp_min(...).rsqrt()
...
g = g * final_scale
```

思想大致是：

> 在强制更新具有受控的矩阵几何之后，仍然使用二阶矩估计来调整其尺度。

所以 Muon 并不仅仅是：

[
G\rightarrow UV^T.
]

它更像是：

[
G
\rightarrow
\text{动量}
\rightarrow
\text{正交化}
\rightarrow
\text{方差归一化}
\rightarrow
\Delta W.
\]

---

# 15. 分布式部分完全是另一个问题

一旦你理解了以上内容，先忽略第 325 行之后。

那一部分基本上是在回答：

> “如何让同一个优化器在 8 个 GPU 上工作，而不需要复制所有优化器状态？”

例如，对于 8 个 GPU：

```text
                  梯度
                      │
                reduce_scatter
                      │
          ┌───────┬───┴───┬───────┐
          GPU0   GPU1     ...     GPU7
           │      │                │
         更新    更新           更新
           │      │                │
          └───────┴───┬───────────┘
                   all_gather
                       │
                 更新后的参数
```

对于 AdamW，大参数被切分到多个 GPU 上，优化器状态被分片。

对于 Muon，参数被堆叠：

```python
stacked_grads = torch.stack([p.grad for p in params])
```

并且不同的 GPU 拥有不同的矩阵。

所以实际上有两层思想：

```text
算法层
──────────────────────────
AdamW
Muon
动量
极正交化
方差归一化


系统层
──────────────────────────
堆叠
reduce_scatter
all_gather
异步通信
优化器状态分片
```

学习代码时不要把这两层混在一起。

---

# 16. 最有用的心智模型

考虑到你最近关于 Q/K/V 矩阵的问题，你可以这样理解 Muon：

假设一个 Transformer 有

[
W_Q\in\mathbb R^{4096\times4096}.
]

反向传播得到

[
G_Q=\frac{\partial L}{\partial W_Q}.
]

AdamW 基本上说：

> “对于 (G_Q) 中的每个元素，用一阶和二阶矩估计其有用的尺度。”

Muon 说：

> “这不仅仅是 1600 万个独立数字。它是一个 **4096×4096 的线性变换**。将它的梯度视为一个矩阵，并归一化其几何结构。”

这就是重要的概念跳跃。

所以：

```text
AdamW

G[i,j]
 ↓
逐元素自适应缩放
 ↓
ΔW[i,j]


Muon

G                    ← 矩阵
│
├── 动量
│
├── 奇异方向
│
├── 正交化
│
└── 受控的矩阵范数
        ↓
      ΔW
```

因此，如果你已经理解了 **SVD + 奇异值 + 正交矩阵 + 矩阵乘法**，那么 Muon 的论文/代码会更容易理解。

---

## 如果你想真正理解代码

我建议完全按这个顺序学习：

```text
1. SGD
   W ← W - ηG

2. 动量
   m ← βm + (1-β)G

3. Adam
   m, v → m / sqrt(v)

4. SVD
   G = UΣVᵀ

5. 极分解
   G ≈ UΣVᵀ
   polar(G) = UVᵀ

6. Newton-Schulz
   在不做 SVD 的情况下近似 UVᵀ

7. Muon
   动量 → polar(G) → 缩放 → W 更新

8. 分布式 Muon
   reduce_scatter → 局部 Muon → all_gather
```

**要内化的唯一最重要的方程是：**

[
\boxed{
G=U\Sigma V^T
\quad\longrightarrow\quad
UV^T
}
]

这就是看似吓人的 `Polar Express` 代码背后的概念核心。其余部分主要是**让这个操作更快、数值更稳定、尺度可控、并且支持分布式**。

参考文献：

* [源码：MuonAdamW / DistMuonAdamW 实现]
* [Muon 背景与正交化]