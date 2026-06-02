---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch正交化μ子优化器
translated: true
type: note
---

明白了——这里有一个简洁的 PyTorch 参考实现，你可以直接用于项目。它包含：

* 一个小型的 Newton–Schulz 逆平方根方法，用于正交化二维更新
* 一个 `Muon` 优化器（AdamW 风格的权重衰减、动量，可选 RMS 缩放）
* 对一维张量（偏置、LayerNorm 权重）的回退处理
* 一个最小训练示例

---

### 1) 矩阵正交化辅助函数

```python
# muon_utils.py
import torch

@torch.no_grad()
def orthogonalize_by_svd(G: torch.Tensor) -> torch.Tensor:
    """
    最近正交矩阵（Procrustes）：Q = U @ Vh，其中 G = U S Vh。
    精确但在大矩阵上可能较慢。
    """
    U, _, Vh = torch.linalg.svd(G, full_matrices=False)
    return U @ Vh

@torch.no_grad()
def inv_sqrt_newton_schulz(A: torch.Tensor, iters: int = 5, eps: float = 1e-6) -> torch.Tensor:
    """
    使用 Newton–Schulz 迭代计算对称正定矩阵 A 的 A^{-1/2}。
    假设 A 是对称正定的（例如 G^T G + eps I）。
    """
    # 归一化以改善收敛性
    trace = A.diagonal(offset=0, dim1=-2, dim2=-1).sum(-1, keepdim=True).unsqueeze(-1)  # (...,1,1)
    A_norm = A / (trace + eps)

    I = torch.eye(A.size(-1), device=A.device, dtype=A.dtype).expand_as(A)
    Y = A_norm.clone()
    Z = I.clone()

    for _ in range(iters):
        T = 0.5 * (3*I - Z @ Y)
        Y = Y @ T
        Z = T @ Z

    # A^{-1/2} ≈ Z / sqrt(trace)
    return Z / torch.sqrt(trace + eps)

@torch.no_grad()
def orthogonalize_by_newton_schulz(G: torch.Tensor, iters: int = 5, eps: float = 1e-6) -> torch.Tensor:
    """
    Q ≈ G (G^T G)^{-1/2}，使用 Newton–Schulz 迭代计算逆平方根。
    """
    # 构造对称正定矩阵；添加 eps*I 保证数值稳定性
    S = G.transpose(-1, -2) @ G
    n = S.size(-1)
    S = S + eps * torch.eye(n, device=S.device, dtype=S.dtype)
    S_inv_sqrt = inv_sqrt_newton_schulz(S, iters=iters, eps=eps)
    return G @ S_inv_sqrt
```

---

### 2) Muon 优化器

```python
# muon.py
from torch.optim.optimizer import Optimizer
import torch
from muon_utils import orthogonalize_by_newton_schulz, orthogonalize_by_svd

class Muon(Optimizer):
    r"""
    Muon：结构感知、矩阵正交化优化器。
    - 梯度动量
    - 解耦权重衰减（AdamW 风格）
    - 对二维参数：正交化动量平均更新（Newton–Schulz 或 SVD）
    - 对一维/其他形状参数：像 Adam 一样对动量进行 RMS 缩放（无正交化）

    参数：
        params: 可迭代的参数
        lr (float): 学习率
        beta (float): 动量因子（默认 0.9）
        weight_decay (float): 解耦权重衰减（默认 0.01）
        eps (float): 数值 epsilon（默认 1e-8）
        ns_iters (int): 正交化的 Newton–Schulz 迭代次数（默认 5）
        method (str): 正交化方法，'ns' 表示 Newton–Schulz（默认），或 'svd'
        rms_scale (bool): 对非二维张量应用逐张量的 RMS 归一化到动量（默认 True）
        clip_grad_norm (float|None): 如果设置，在应用前按 L2 范数裁剪动量更新（默认 None）
    """
    def __init__(
        self,
        params,
        lr: float,
        beta: float = 0.9,
        weight_decay: float = 0.01,
        eps: float = 1e-8,
        ns_iters: int = 5,
        method: str = "ns",
        rms_scale: bool = True,
        clip_grad_norm: float | None = None,
    ):
        if lr <= 0:
            raise ValueError("Invalid learning rate")
        if not 0.0 <= beta < 1.0:
            raise ValueError("Invalid beta")
        defaults = dict(
            lr=lr,
            beta=beta,
            weight_decay=weight_decay,
            eps=eps,
            ns_iters=ns_iters,
            method=method,
            rms_scale=rms_scale,
            clip_grad_norm=clip_grad_norm,
        )
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            lr = group["lr"]
            beta = group["beta"]
            wd = group["weight_decay"]
            eps = group["eps"]
            ns_iters = group["ns_iters"]
            method = group["method"]
            rms_scale = group["rms_scale"]
            clip_gn = group["clip_grad_norm"]

            for p in group["params"]:
                if p.grad is None:
                    continue

                grad = p.grad
                state = self.state[p]

                # 动量缓冲区
                if "momentum" not in state:
                    state["momentum"] = torch.zeros_like(p, memory_format=torch.preserve_format)
                m = state["momentum"]

                # m_t = beta*m_{t-1} + (1-beta)*g_t
                m.mul_(beta).add_(grad, alpha=(1.0 - beta))

                # 可选的全局裁剪更新方向（动量）
                if clip_gn is not None:
                    gnorm = m.norm()
                    if gnorm > clip_gn:
                        m.mul_(clip_gn / (gnorm + 1e-12))

                # 对参数进行解耦权重衰减
                if wd != 0.0:
                    p.mul_(1.0 - lr * wd)

                # 计算更新方向 U
                if p.ndim == 2:
                    # 正交化矩阵更新
                    if method == "svd":
                        U = orthogonalize_by_svd(m)
                    else:
                        U = orthogonalize_by_newton_schulz(m, iters=ns_iters, eps=eps)
                else:
                    # 非矩阵张量：RMS 缩放（类似 Adam）以保持步长平衡
                    if rms_scale:
                        rms = torch.sqrt(m.pow(2).mean() + eps)
                        U = m / rms
                    else:
                        U = m

                # 参数更新
                p.add_(U, alpha=-lr)

        return loss
```

---

### 3) 最小使用示例

```python
# demo_muon.py
import torch
from torch import nn
from muon import Muon

# 玩具模型
model = nn.Sequential(
    nn.Linear(256, 512),
    nn.ReLU(),
    nn.Linear(512, 256),
)

x = torch.randn(32, 256)
y = torch.randn(32, 256)

criterion = nn.MSELoss()

# 尝试 Newton–Schulz 正交化（快速且可扩展）。使用方法 'svd' 进行精确正交化。
optimizer = Muon(model.parameters(), lr=3e-4, beta=0.9, weight_decay=0.02, ns_iters=5, method="ns")

for step in range(200):
    optimizer.zero_grad(set_to_none=True)
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()

    if (step + 1) % 20 == 0:
        print(f"step {step+1:03d} | loss = {loss.item():.4f}")
```

---

### 注意事项与提示

* 对于非常大的权重矩阵，`method="ns"` 避免了 SVD，通常更快。如果你在小层上验证正确性，可以与 `method="svd"` 进行比较以进行健全性检查。
* `ns_iters=3..6` 是一个较好的实用范围。迭代次数越少 = 越快但正交化精度稍低。
* 保持较小的 `weight_decay`（解耦）和适中的 `beta`（例如 0.9）。对于 transformers/MLPs，学习率在 `1e-3` 到 `3e-4` 左右是一个合理的起点。
* 如果训练出现尖峰，在构造函数中启用 `clip_grad_norm`（例如 `1.0–5.0`）。

如果你需要，我可以根据你的具体模型设置（例如 torch.compile、FSDP/ZeRO、MoE 层、自定义每参数配置）进行调整。
