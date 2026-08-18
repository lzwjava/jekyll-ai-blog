---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Newton-Schulz正交化用于动量
translated: true
type: note
---

问题：牛顿-舒尔茨迭代如何用于正交化动量矩阵？

答案：

**目标：** 给定一个矩阵 $G$（动量缓冲区），找到一个正交近似 $Q \approx G / \|G\|$，使得 $Q^T Q \approx I$。

---

**牛顿-舒尔茨迭代**

这是一种多项式迭代，收敛到矩阵的正交因子（来自其极分解 $G = QS$，其中 $Q$ 为正交矩阵，$S$ 为对称半正定矩阵）。

**更新规则（一步）：**

$$X_{k+1} = \frac{3}{2} X_k - \frac{1}{2} X_k X_k^T X_k$$

从 $X_0 = G / \|G\|_F$ 开始，该迭代以三次收敛速度收敛到正交因子 $Q$。

---

**代码逐步说明**

```python
import torch

def newton_schulz_orthogonalize(G, steps=5, eps=1e-7):
    """
    使用牛顿-舒尔茨迭代正交化矩阵 G。
    返回 Q ≈ G 的正交因子。
    """
    # 步骤 1：归一化，确保谱范数 < 1
    X = G / (G.norm() + eps)

    # 步骤 2：迭代
    for _ in range(steps):
        A = X @ X.T          # X X^T
        X = 1.5 * X - 0.5 * (A @ X)   # 牛顿-舒尔茨更新

    return X
```

---

**Muon 实际使用的多项式（略有不同）**

Muon 实现使用了一个五次切比雪夫风格的多项式，以实现更快的收敛：

```python
def zeropower_via_newtonschulz5(G, steps=10, eps=1e-7):
    assert G.ndim == 2
    a, b, c = (3.4445, -4.7750, 2.0315)  # 调优后的系数

    X = G / (G.norm() + eps)

    # 处理非方阵：在较小维度上操作
    if G.shape[0] > G.shape[1]:
        X = X.T

    for _ in range(steps):
        A = X.T @ X          # X^T X（对于高矩阵，为方阵）
        X = a * X + (b * X) @ A + (c * X) @ (A @ A)

    if G.shape[0] > G.shape[1]:
        X = X.T

    return X
```

---

**它如何融入 Muon**

```python
def muon_update(param, momentum_buffer, lr=0.01, steps=5):
    G = momentum_buffer          # 累积的梯度动量
    Q = zeropower_via_newtonschulz5(G, steps=steps)  # 正交化
    
    # 像 Adam 一样按 RMS 缩放，但使用正交方向
    scale = max(1, G.shape[0] / G.shape[1]) ** 0.5
    param.data -= lr * scale * Q
```

---

**直观总结**

| 步骤 | 说明 |
| --- | --- |
| 归一化 $G$ | 将谱范数调整到接近 1 |
| 迭代 $X \leftarrow f(X)$ | 将奇异值推向 1 |
| 收敛后的 $X = Q$ | 所有奇异值 = 1 → 正交矩阵 |

结果是一个更新矩阵，其中**所有梯度方向被平等对待**——没有单一方向占主导地位——从而带来更稳定的训练。

参考文献：

- [Muon 源代码 – 牛顿-舒尔茨实现](https://github.com/KellerJordan/Muon/blob/master/muon.py)
- [极分解的牛顿-舒尔茨方法 – Wikipedia](https://en.wikipedia.org/wiki/Polar_decomposition#Algorithms)
- [Keller Jordan 的 Muon 博客文章](https://kellerjordan.github.io/posts/muon/)
