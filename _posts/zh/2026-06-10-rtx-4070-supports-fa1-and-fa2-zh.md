---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 支持 FA1 和 FA2
translated: true
type: note
---

**问题：** RTX 4070 能否运行 FlashAttention 1 或 2？

**回答：**

能——两者都行。RTX 4070 属于 Ada Lovelace 架构，计算能力为 **sm_89**，而 FlashAttention-2 官方支持 Ampere（sm_80/86）、Ada（sm_89）和 Hopper（sm_90）。只有 FlashAttention-**3** 无法使用（仅限 Hopper，需用到 TMA/WGMMA，Ada 不具备）。

针对你的 nanochat 设置，有两个重要细节：

**1. 你可能已经在运行 FA2 而无需额外安装。** PyTorch 的 SDPA（`F.scaled_dot_product_attention`）内置了 FlashAttention-2 内核。日志中显示“SDPA fallback”消息仅意味着未安装 `flash-attn` *包*——但如果条件满足（fp16/bf16、head_dim ≤ 256、CUDA tensor、无不兼容的 mask），SDPA 仍会调度到其内部的 FA2 内核。你可以通过以下代码验证实际使用的内核：

```python
import torch
from torch.nn.attention import SDPBackend, sdpa_kernel

q = torch.randn(1, 6, 1024, 128, device="cuda", dtype=torch.bfloat16)  # (B, H, T, hd) — d12: 768/6 = 128
with sdpa_kernel([SDPBackend.FLASH_ATTENTION]):
    out = torch.nn.functional.scaled_dot_product_attention(q, q, q, is_causal=True)
print("FA2 kernel works on this GPU:", out.shape)
```

如果这段代码运行无误，说明你已经在使用 flash attention。如果你的模型跑在 fp32 上，那才是真正的阻碍——改为 bf16（autocast）即可，你本来也需要用它来提升训练吞吐量。

**2. 安装独立的 `flash-attn` 包**（提供 `flash_attn_func`、变长支持、稍新的内核）：

```bash
# 避免耗时数小时的源码编译——使用预编译 wheel
pip install flash-attn --no-build-isolation

# 如果尝试从源码编译且内存有限：
MAX_JOBS=4 pip install flash-attn --no-build-isolation
```

从源码编译需要 `nvcc`（与你的 PyTorch CUDA 版本匹配的 CUDA 工具包），可能耗时 30 分钟以上并占用数十 GB 内存（你的 62 GB 内存可以承受，但最好先检查是否有匹配的预编译 wheel——它们根据 torch 版本、CUDA 版本、cxx11abi 和 Python 版本进行区分）。

然后在 nanochat 风格的代码中：

```python
from flash_attn import flash_attn_func
# q, k, v: (B, T, H, head_dim) —— 注意布局与 SDPA 的 (B, H, T, hd) 不同
out = flash_attn_func(q, k, v, causal=True)
```

**针对你 d12 运行的实际建议：** 在 286M 规模、T≈1024–2048 的情况下，PyTorch SDPA 内部 FA2 与独立包之间的差距很小（几个百分点）。更大的收益来自 bf16 autocast + `torch.compile`。建议先确认 SDPA 确实调度到了 flash 后端（上面的代码段），如果尚未使用 bf16 则开启，只有在 profile 后发现 attention 是真正的瓶颈时，再费心安装 `flash-attn`。

一个注意事项：FA1/FA2 的 head_dim 必须 ≤ 256（在某些较老的 FA1 版本中，sm_89 反向传播时 head_dim 需 ≤ 128）。你的 d12 配置（768 dim / 6 heads = 128 head_dim）完全没问题。