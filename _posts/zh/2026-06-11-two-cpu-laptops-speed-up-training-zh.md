---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双CPU笔记本电脑加速训练
translated: true
type: note
---

**问题：** 两台完全没有独立GPU的Ubuntu笔记本电脑——都只有CPU，情况如何？

**回答：**

有趣的是，这是你给出的三种配置中，**唯一一种能让分布式训练真正带来加速的情况**。原因如下：当各个rank（进程）异构（出现拖后腿的节点）或通信时间无法被计算时间隐藏时，DDP的扩展性就会下降。两台CPU笔记本是同构的，且CPU每步计算速度很慢，网络有充足的时间来隐藏all-reduce操作。矛盾的是，慢速计算反而有利于扩展效率。

**扩展性计算：**

DDP将梯度all-reduce与反向传播重叠（使用分桶策略，默认约25 MB每桶）。当`t_comm < t_backward`时，扩展性接近线性。

GPT-2 124M，fp32：每步约496 MB梯度。
- 千兆以太网：all-reduce约需4.5秒
- CPU反向传播（8核移动芯片）：约15–30秒

通信完全隐藏在反向传播之下 → 第二台笔记本带来**约1.8–1.9倍的有效加速**。对比上一个回答中的4070+CPU组合，同样的计算得到的却是*减速*。对于nanoGPT的shakespeare-char（10.65M参数，约43 MB梯度，约0.4秒通信），通信隐藏得更加轻松。

**设置——与之前相同的脚本，两个rank都在CPU上，标准DDP：**

```python
# dist_train.py
import os, torch, torch.nn as nn, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data.distributed import DistributedSampler

def main():
    dist.init_process_group(backend="gloo")
    rank, ws = dist.get_rank(), dist.get_world_size()
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "8")))

    model = DDP(nn.Sequential(nn.Linear(768, 3072), nn.GELU(), nn.Linear(3072, 768)))
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    # DistributedSampler 让每个rank获得不相交的数据分片——这正是2倍加速的来源
    ds = TensorDataset(torch.randn(4096, 768))
    dl = DataLoader(ds, batch_size=32, sampler=DistributedSampler(ds))

    for epoch in range(3):
        dl.sampler.set_epoch(epoch)
        for (x,) in dl:
            loss = model(x).pow(2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        if rank == 0:
            print(f"epoch {epoch} loss {loss.item():.4f}")

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

```bash
# 笔记本 A (rank 0)
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=2 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py

# 笔记本 B (rank 1)
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=2 --node_rank=1 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py
```

**真正重要的CPU专用调优：**

1. **每个节点一个进程，所有线程都分配给它。** PyTorch CPU操作通过OpenMP在内部并行化（操作内并行）。`nproc_per_node=2+` 配合分割线程通常会输给一个大型进程——需要进行测量，但从1×`nproc`个线程开始。
2. **将`OMP_NUM_THREADS`绑定到*物理*核心**，而非超线程。GEMM密集型工作负载会因SMT过度订阅而性能下降：`lscpu | grep -E 'Core|Socket'`。
3. **如果CPU支持AVX-512/AMX（新款Intel），使用bf16自动混合精度**——`torch.autocast("cpu", dtype=torch.bfloat16)` 可以在矩阵乘法上获得2–4倍加速。检查：`lscpu | grep -o 'avx512_bf16\|amx_bf16'`。
4. **`torch.compile(model)`**——inductor CPU后端会融合操作，在Transformer模块上通常能获得1.3–2倍加速，并且可以与DDP叠加使用。
5. **使用以太网线，而非WiFi。** WiFi延迟抖动会破坏通信/计算重叠。在两台笔记本之间（或都连接到路由器）用一根5美元网线，能保证all-reduce的确定性。
6. **电源模式：** `sudo cpupower frequency-set -g performance`——笔记本的调频器会严重限制持续AVX负载，而热节流的rank相对于其相同规格的机器就会成为拖后腿者。

**绝对数值的现实情况：** 两台笔记本 × GPT-2 124M每步约25秒 ≈ 有效每步约13秒。你的4070每步约0.25秒——一块GPU ≈ **50对这样的笔记本**。因此诚实的规模判断是：

- **shakespeare-char / 1–10M参数 nanoGPT**：确实可以在这种配置上良好训练，数分钟到数小时，且2倍加速真实有效。很好用于灵感编码循环。
- **GPT-2 124M及以上**：技术上能收敛，实际效果如同一个空间加热器。请使用4070或MI300X。

从你三种配置中得到的有趣结论：分布式效率由两个比率决定——**rank同构性**和**t_backward / t_comm**。两台弱而相同的节点扩展优美；一台强加一台弱则扩展效果不如单用那台强节点。这个直觉正是日后在集群规模上让人吃亏的地方（一块慢网卡或热节流GPU拖累其他511块），所以这套玩具配置教会了正确的道理。