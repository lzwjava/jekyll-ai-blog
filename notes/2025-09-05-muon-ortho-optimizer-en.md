---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muon Optimizer with Orthogonalization for PyTorch
translated: false
type: note
---

Got it—here’s a clean PyTorch reference implementation you can drop into a project. It includes:

* A tiny Newton–Schulz inverse–square-root to orthogonalize 2-D updates
* A `Muon` optimizer (AdamW-style weight decay, momentum, optional RMS scaling)
* A fallback for 1-D tensors (bias, LayerNorm weights)
* A minimal training example

---

### 1) Matrix orthogonalization helpers

```python
# muon_utils.py
import torch

@torch.no_grad()
def orthogonalize_by_svd(G: torch.Tensor) -> torch.Tensor:
    """
    Nearest orthogonal (Procrustes): Q = U @ Vh, where G = U S Vh.
    Exact but can be slower on large mats.
    """
    U, _, Vh = torch.linalg.svd(G, full_matrices=False)
    return U @ Vh

@torch.no_grad()
def inv_sqrt_newton_schulz(A: torch.Tensor, iters: int = 5, eps: float = 1e-6) -> torch.Tensor:
    """
    Compute A^{-1/2} for SPD A using Newton–Schulz.
    Assumes A is symmetric positive definite (e.g., G^T G + eps I).
    """
    # Normalize for better convergence
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
    Q ≈ G (G^T G)^{-1/2}, using Newton–Schulz for the inverse square root.
    """
    # Make SPD; add eps*I for numerical stability
    S = G.transpose(-1, -2) @ G
    n = S.size(-1)
    S = S + eps * torch.eye(n, device=S.device, dtype=S.dtype)
    S_inv_sqrt = inv_sqrt_newton_schulz(S, iters=iters, eps=eps)
    return G @ S_inv_sqrt
```

---

### 2) Muon optimizer

```python
# muon.py
from torch.optim.optimizer import Optimizer
import torch
from muon_utils import orthogonalize_by_newton_schulz, orthogonalize_by_svd

class Muon(Optimizer):
    r"""
    Muon: structure-aware, matrix-orthogonalizing optimizer.
    - Momentum on grads
    - Decoupled weight decay (AdamW-style)
    - For 2D params: orthogonalize the momentum-avg update (Newton–Schulz or SVD)
    - For 1D/other shapes: RMS scaling on momentum like Adam (no orthogonalization)

    Args:
        params: iterable of parameters
        lr (float): learning rate
        beta (float): momentum factor (default 0.9)
        weight_decay (float): decoupled weight decay (default 0.01)
        eps (float): numerical eps (default 1e-8)
        ns_iters (int): Newton–Schulz iterations for orthogonalization (default 5)
        method (str): 'ns' for Newton–Schulz (default), or 'svd'
        rms_scale (bool): apply per-tensor RMS normalization to momentum for non-2D tensors (default True)
        clip_grad_norm (float|None): if set, clip momentum update by L2 norm before applying (default None)
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

                # Momentum buffer
                if "momentum" not in state:
                    state["momentum"] = torch.zeros_like(p, memory_format=torch.preserve_format)
                m = state["momentum"]

                # m_t = beta*m_{t-1} + (1-beta)*g_t
                m.mul_(beta).add_(grad, alpha=(1.0 - beta))

                # Optional global clip on the update direction (momentum)
                if clip_gn is not None:
                    gnorm = m.norm()
                    if gnorm > clip_gn:
                        m.mul_(clip_gn / (gnorm + 1e-12))

                # Decoupled weight decay on parameters
                if wd != 0.0:
                    p.mul_(1.0 - lr * wd)

                # Compute update direction U
                if p.ndim == 2:
                    # Orthogonalize the matrix update
                    if method == "svd":
                        U = orthogonalize_by_svd(m)
                    else:
                        U = orthogonalize_by_newton_schulz(m, iters=ns_iters, eps=eps)
                else:
                    # Non-matrix tensors: RMS scaling (Adam-like) to keep step sizes balanced
                    if rms_scale:
                        rms = torch.sqrt(m.pow(2).mean() + eps)
                        U = m / rms
                    else:
                        U = m

                # Parameter update
                p.add_(U, alpha=-lr)

        return loss
```

---

### 3) Minimal usage example

```python
# demo_muon.py
import torch
from torch import nn
from muon import Muon

# Toy model
model = nn.Sequential(
    nn.Linear(256, 512),
    nn.ReLU(),
    nn.Linear(512, 256),
)

x = torch.randn(32, 256)
y = torch.randn(32, 256)

criterion = nn.MSELoss()

# Try Newton–Schulz orthogonalization (fast & scalable). Use method='svd' for exact.
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

### Notes & tips

* For very large weight matrices, `method="ns"` avoids SVD and is typically much faster. If you’re validating correctness on small layers, compare with `method="svd"` to sanity-check.
* `ns_iters=3..6` is a good practical range. Fewer iterations = faster but slightly less precise orthogonalization.
* Keep a small `weight_decay` (decoupled) and a moderate `beta` (e.g., 0.9). Learning rate around `1e-3` to `3e-4` is a reasonable starting point for transformers/MLPs.
* If training gets spiky, enable `clip_grad_norm` (e.g., `1.0–5.0`) in the constructor.

If you want, I can adapt this to your exact model setup (e.g., torch.compile, FSDP/ZeRO, MoE layers, custom per-param configs).
