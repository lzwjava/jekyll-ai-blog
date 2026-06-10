---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch DDP：数据并行性解析
translated: true
type: note
---

**问题：** 在PyTorch分布式训练中，数据并行是否意味着将训练数据拆分到两个GPU上，每个GPU持有相同的模型，并且它们同步参数更新？

**回答：**

是的——您描述的是**数据并行（DDP）**，也是最常见的形式。但您的理解模型需要一点修正：GPU并不"共享"模型更新——它们各自计算自己的梯度，然后通过**全规约**平均梯度，之后每个GPU再独立应用相同的更新。让我们精确地梳理一遍。

## DDP的逐步机制

假设有2个GPU，每个GPU的批次大小为32：

1. **复制**：每个GPU持有模型的完整副本，初始化参数一致（启动时rank 0广播权重）。
2. **数据分片**：`DistributedSampler`对数据集进行分区，使每个rank看到互不重叠的数据切片。有效全局批次 = 32 × 2 = 64。
3. **独立前向+反向传播**：每个GPU在自己的微批次上计算损失并执行反向传播。此时GPU间的梯度*不同*（因为数据不同！）。
4. **梯度全规约**：NCCL在rank间对梯度进行平均。这是关键的同步点：`g = (g_0 + g_1) / 2`。此后，每个rank持有*完全相同的*梯度。
5. **本地优化器步骤**：每个rank在自己的模型副本上执行`optimizer.step()`。由于权重、梯度和优化器状态相同，模型从此保持同步——第一步之后无需再广播参数。

数学原理：对分片上的梯度进行平均，等价于计算完整64个样本批次上平均损失的梯度（假设损失函数采用平均归约）。因此，使用N个GPU进行DDP训练，近似于单GPU训练时将批次大小扩大N倍——这也是为什么需要相应调整学习率的原因。

## 最小化DDP实现（这正是nanoGPT所做的）

```python
# torchrun --nproc_per_node=2 train.py
import os, torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

dist.init_process_group(backend="nccl")
rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(rank)

model = MyModel().cuda(rank)
model = DDP(model, device_ids=[rank])

sampler = DistributedSampler(train_ds)          # 每个rank获得互斥的数据分片
loader = DataLoader(train_ds, batch_size=32, sampler=sampler)

opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

for epoch in range(epochs):
    sampler.set_epoch(epoch)                    # 每个epoch重新打乱数据分片
    for x, y in loader:
        x, y = x.cuda(rank), y.cuda(rank)
        loss = model(x, y)
        loss.backward()                          # 全规约在此处发生，
        opt.step()                               # 与反向传播重叠执行
        opt.zero_grad()

dist.destroy_process_group()
```

两个值得注意的非直观细节：

- **梯度全规约与反向传播重叠执行。** DDP注册了自动求导钩子，并将梯度分组打包（默认25MB）。一旦某个分组的梯度就绪，NCCL会异步触发全规约，同时反向传播继续计算更早层的梯度。这就是DDP扩展性好的原因——通信被计算所掩盖。
- **`set_epoch`很重要。** 如果不设置，每个epoch都会看到相同的数据分片顺序。

既然您曾在MI300X上训练过GPT-2 760M——可以查看nanoGPT的`train.py`：它在DDP基础上增加了梯度累积，仅在最后一个微步时通过`model.require_backward_grad_sync = (micro_step == grad_accum_steps - 1)`进行同步，以避免不必要的全规约。

## 模型无法容纳时的情况

DDP要求每个GPU上都存放*完整的模型+梯度+优化器状态*。混合精度训练下，AdamW每个参数约需16字节（2权重+2梯度+4+4优化器动量+4主权重），因此70亿参数的模型需要约112GB显存——在12GB的4070上根本无法运行。这时就需要其他并行策略：

- **FSDP / ZeRO**：仍然是数据并行，但将参数/梯度/优化器状态分片到多个GPU上，在前向/反向传播过程中即时全收集各层参数。以通信换内存。
- **张量并行**：将单个矩阵乘法拆分到多个GPU上（例如，注意力头分散到不同设备）。需要高速互连（NVLink）。
- **流水线并行**：将各层拆分到多个GPU上，微批次在流水线阶段间流动。
- **专家并行**：用于MoE（与您对DeepSeek v4的兴趣相关）——不同专家位于不同GPU上，令牌通过all-to-all通信进行路由。

前沿训练（DeepSeek-V3技术报告是最佳的公开参考资料）会组合使用所有这些策略：DP × PP × EP同时进行。

因此，您的总结对于DDP本身是正确的：所有模型相同，数据拆分，同步更新——需要精确指出的是，同步发生在*梯度*层面（通过全规约），而不是共享更新本身。
