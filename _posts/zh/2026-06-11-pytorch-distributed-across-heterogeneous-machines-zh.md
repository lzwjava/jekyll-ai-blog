---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch跨异构机器的分布式
translated: true
type: note
---

**问题：** PyTorch 分布式训练能否在两台异构机器上运行——一台运行 macOS（Apple Silicon）的机器和一台搭载 RTX 4070 的 Ubuntu 机器？

**答案：**

能运行——但只能使用 **gloo** 后端，并且存在实际限制，使其更像一次学习练习而非性能提升。首先有三个硬性约束：

1. **NCCL 不可用。** NCCL 要求每个 rank 都有 CUDA。你的 Mac 没有 CUDA，因此整个任务必须使用 `gloo`（基于 TCP 的 CPU 集合通信）。这意味着即便是 4070 的梯度也要通过 CPU 内存进行 all-reduce。
2. **MPS ≠ 神经引擎，且 gloo 不支持 MPS。** PyTorch 的 `mps` 后端运行在 M2 的 *Metal GPU* 上——Apple 神经引擎（ANE）完全无法用于 PyTorch 训练（只能通过 Core ML 进行推理）。而 `gloo` 的集合操作只接受 CPU（以及 CUDA）张量，因此 Mac 上的 rank 要么在 CPU 上训练，要么在 MPS 上训练并手动进行 MPS→CPU→all-reduce→MPS 的梯度复制。
3. **DDP 是同步的。** 每一步都会受最慢 rank 的限制。在 GPT-2 级别的正向/反向传播中，你的 M2 可能比 4070 慢 5-10 倍，因此 4070 大部分时间处于空闲状态。

最小化可行设置，手动 all-reduce 以便 Mac 上使用 MPS：

```python
# dist_train.py —— 两台机器上使用相同文件
import os, torch, torch.distributed as dist
import torch.nn as nn

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if torch.backends.mps.is_available(): return "mps"
    return "cpu"

def allreduce_grads(model, world_size, device):
    # gloo 只处理 CPU 张量 -> 通过 CPU 中转梯度
    for p in model.parameters():
        if p.grad is None: continue
        g = p.grad.detach().to("cpu")
        dist.all_reduce(g, op=dist.ReduceOp.SUM)
        p.grad.copy_((g / world_size).to(device))

def main():
    dist.init_process_group(backend="gloo")  # 此处无法使用 NCCL
    rank, ws = dist.get_rank(), dist.get_world_size()
    device = pick_device()
    torch.manual_seed(42)  # 所有 rank 使用相同初始化（或广播 rank0 的权重）

    model = nn.Sequential(nn.Linear(768, 3072), nn.GELU(), nn.Linear(3072, 768)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    for step in range(100):
        x = torch.randn(32, 768, device=device)
        loss = model(x).pow(2).mean()
        opt.zero_grad(); loss.backward()
        allreduce_grads(model, ws, device)
        opt.step()
        if rank == 0 and step % 10 == 0:
            print(f"step {step} loss {loss.item():.4f} [{device}]")

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

启动命令（Ubuntu 机器为 rank 0 / rendezvous 主节点）：

```bash
# Ubuntu + 4070
torchrun --nnodes=2 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<UBUNTU_LAN_IP> --master_port=29500 dist_train.py

# MacBook Air M2
torchrun --nnodes=2 --node_rank=1 --nproc_per_node=1 \
  --master_addr=<UBUNTU_LAN_IP> --master_port=29500 dist_train.py
```

如果两个 rank 都在 CPU 上运行，可以直接使用内置的 `DistributedDataParallel(model)` —— DDP+gloo+CPU 完全受支持，并且可以通过分桶机制将 all-reduce 与反向传播重叠。DDP **不支持** MPS 模块，因此才有了上述手动实现的版本。

**为什么它不会比单独使用 4070 更快——带宽计算：**

对于 GPT-2 124M 的 fp32 模型，梯度约为 496 MB 每步。环状 all-reduce 每个 rank 需要传输 `2(N-1)/N ≈ 1×` 的数据量，因此每步约 500 MB 的数据在 LAN 上传输。千兆以太网的实际吞吐量约为 117 MB/s → **每步纯通信时间约 4-5 秒**，还不包括 M2 慢速节点的拖累以及 MPS↔CPU 的拷贝开销。单独使用 4070 在不到一秒内即可完成一个 124M 参数的步骤。WiFi 会使情况更糟。

**如果你仍然想尝试，可以采取的缓解措施（值得做一次以深入理解机制）：**

- **每个 rank 使用不等的批次大小**——例如 4070 使用 batch 48，M2 使用 batch 16，然后按样本数量加权梯度求和，而不是除以 `world_size`。这是经典的异构 DDP 技巧。
- **在 all-reduce 之前使用 bf16 梯度压缩**，可将网络传输量减半（`g.to(torch.bfloat16)` → all_reduce → 升回原精度）。
- **批量合并拷贝**——将所有梯度展平为一个连续的 CPU 张量（`torch._utils._flatten_dense_tensors`），然后执行单个 all-reduce，而不是逐个参数调用；逐张量的 gloo 调用会带来巨大的延迟开销。

**对你当前设置的实用结论：** 用这个双节点配置来学习 `torchrun`、rendezvous、rank 和集合通信语义——这与多节点 NCCL 在 MI300X 机器上的思维模型相同，只是更慢。就实际训练吞吐量而言，单独使用 4070 胜过这两台机器的组合，而 MI300X 大约 2 美元/小时，相比你所有的硬件在性价比上更优。这个练习的真正价值在于，当你迁移到 8×MI300X 并配合 RCCL 时，除了 `backend="nccl"` 和 `--nproc_per_node=8` 之外，代码几乎无需改动。