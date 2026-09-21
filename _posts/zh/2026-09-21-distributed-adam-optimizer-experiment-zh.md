---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式Adam优化器实验
translated: true
type: note
---

**问题：** 如何验证Adam自适应学习率在实际中有效，以及如何利用两台各配备RTX 4070的机器运行实验？

**回答：**

要实证Adam的行为，您需要将其与其他优化器（SGD、RMSProp、AdaGrad）进行比较，并观察收敛速度和损失曲线。在两台各配备RTX 4070 GPU的机器上，您可以使用**分布式训练**。

---

## 设置：两台机器 × 每台一个RTX 4070

这是一个使用PyTorch `DistributedDataParallel (DDP)`的**2节点、每节点1 GPU**分布式设置。

---

## 步骤1 — 环境设置（两台机器上）

```bash
pip install torch torchvision matplotlib
```

确保两台机器可以通过网络相互访问。记下**机器1的IP地址**（主节点）。

---

## 步骤2 — 训练脚本（`train_adam_proof.py`）

将此脚本保存在**两台机器**上：

```python
import os
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import json

# ── 分布式初始化 ──────────────────────────────────────────────────────────
def setup(rank, world_size):
    dist.init_process_group(
        backend="nccl",          # NCCL = 最适合GPU到GPU通信
        init_method="env://",    # 从环境变量读取MASTER_ADDR / MASTER_PORT
        rank=rank,
        world_size=world_size,
    )
    torch.cuda.set_device(0)     # 每台机器只有1个GPU

def cleanup():
    dist.destroy_process_group()

# ── 简单CNN模型 ───────────────────────────────────────────────────────────
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 256), nn.ReLU(),
            nn.Linear(256, 10),
        )
    def forward(self, x):
        return self.net(x)

# ── 训练一个epoch ────────────────────────────────────────────────────────────
def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        loss = criterion(model(imgs), labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

# ── 主函数 ───────────────────────────────────────────────────────────────
def main():
    rank       = int(os.environ["RANK"])        # 0 = 机器1, 1 = 机器2
    world_size = int(os.environ["WORLD_SIZE"])  # 2

    setup(rank, world_size)
    device = torch.device("cuda:0")

    # 数据集
    tf = transforms.Compose([transforms.ToTensor(),
                              transforms.Normalize((0.1307,), (0.3081,))])
    dataset  = datasets.MNIST("./data", train=True, download=True, transform=tf)
    sampler  = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader   = DataLoader(dataset, batch_size=256, sampler=sampler, num_workers=4)
    criterion = nn.CrossEntropyLoss()

    EPOCHS = 20
    results = {}

    # ── 比较优化器 ─────────────────────────────────────────────────────────
    optimizers = {
        "Adam":    lambda p: torch.optim.Adam(p, lr=1e-3, betas=(0.9, 0.999)),
        "SGD":     lambda p: torch.optim.SGD(p,  lr=1e-2, momentum=0.9),
        "RMSProp": lambda p: torch.optim.RMSprop(p, lr=1e-3),
        "AdaGrad": lambda p: torch.optim.Adagrad(p, lr=1e-2),
    }

    for name, opt_fn in optimizers.items():
        model     = SimpleCNN().to(device)
        model     = DDP(model, device_ids=[0])
        optimizer = opt_fn(model.parameters())
        losses    = []

        for epoch in range(EPOCHS):
            sampler.set_epoch(epoch)   # 确保每个epoch有不同的数据shuffling
            loss = train_epoch(model, loader, optimizer, criterion, device)
            losses.append(loss)
            if rank == 0:
                print(f"[{name}] Epoch {epoch+1:02d}/{EPOCHS} — Loss: {loss:.4f}")

        results[name] = losses

    # ── 仅主节点保存和绘图 ────────────────────────────────────────────────
    if rank == 0:
        with open("results.json", "w") as f:
            json.dump(results, f)

        plt.figure(figsize=(10, 6))
        for name, losses in results.items():
            plt.plot(losses, label=name, linewidth=2)
        plt.xlabel("Epoch")
        plt.ylabel("Training Loss")
        plt.title("Adam vs Other Optimizers (Distributed: 2×RTX 4070)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("optimizer_comparison.png", dpi=150)
        print("✅ Saved: optimizer_comparison.png")

    cleanup()

if __name__ == "__main__":
    main()
```

---

## 步骤3 — 在每台机器上启动

**在机器1（主节点，例如IP = `192.168.1.10`）：**
```bash
MASTER_ADDR=192.168.1.10 \
MASTER_PORT=29500 \
RANK=0 \
WORLD_SIZE=2 \
python train_adam_proof.py
```

**在机器2上：**
```bash
MASTER_ADDR=192.168.1.10 \
MASTER_PORT=29500 \
RANK=1 \
WORLD_SIZE=2 \
python train_adam_proof.py
```

两台机器需要**大致同时**运行命令 — 它们将通过主地址进行握手。

> 或者，使用`torchrun`进行更简洁的启动：
> ```bash
> # 机器1
> torchrun --nnodes=2 --nproc_per_node=1 \
>          --node_rank=0 --master_addr=192.168.1.10 --master_port=29500 \
>          train_adam_proof.py
>
> # 机器2
> torchrun --nnodes=2 --nproc_per_node=1 \
>          --node_rank=1 --master_addr=192.168.1.10 --master_port=29500 \
>          train_adam_proof.py
> ```

---

## 预期结果（验证Adam）

输出图`optimizer_comparison.png`将显示如下内容：

| 优化器 | 收敛速度 | 备注 |
|-----------|------------------|-------|
| **Adam** | ✅ 快速且稳定 | 初期收敛最佳 |
| SGD+momentum | 中等 | 后期追赶 |
| RMSProp | 类似于Adam | 无偏差校正 |
| AdaGrad | ❌ 后期慢 | 学习率衰减过激 |

这直接重现了论文中展示的内容 — Adam收敛更快、更可靠，尤其是在早期epoch中。

---

## 架构概览

```
机器1 (RTX 4070)              机器2 (RTX 4070)
┌─────────────────────┐        ┌─────────────────────┐
│  RANK=0  (master)   │◄──────►│  RANK=1             │
│  ½ of the dataset   │  NCCL  │  ½ of the dataset   │
│  gradient sync      │  sync  │  gradient sync      │
└─────────────────────┘        └─────────────────────┘
         ↓ 两块GPU上的梯度平均
         ↓ 每个优化器步骤使用全批次信号
```

使用DDP，梯度在每次反向传播后**在两块GPU之间进行平均** — 因此您的有效批大小为`256 × 2 = 512`，训练速度比单GPU快约2倍。

---

**参考文献：**
- [Adam: A Method for Stochastic Optimization](https://arxiv.org/pdf/1412.6980)
- [PyTorch Distributed Training Docs](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [torchrun CLI reference](https://pytorch.org/docs/stable/elastic/run.html)