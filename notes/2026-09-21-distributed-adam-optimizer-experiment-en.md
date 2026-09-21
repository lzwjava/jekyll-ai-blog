---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed Adam Optimizer Experiment
translated: false
type: note
---

**Question:** How can I verify that Adam's adaptive learning rate works in practice, and how can I run experiments using two machines each equipped with an RTX 4070?

**Answer:**

To empirically prove Adam's behavior, you'll want to compare it against other optimizers (SGD, RMSProp, AdaGrad) and observe convergence speed and loss curves. With two RTX 4070 GPUs across two machines, you can use **distributed training**.

---

## Setup: Two Machines × One RTX 4070 Each

This is a **2-node, 1-GPU-per-node** distributed setup using PyTorch's `DistributedDataParallel (DDP)`.

---

## Step 1 — Environment Setup (on both machines)

```bash
pip install torch torchvision matplotlib
```

Make sure both machines can reach each other over the network. Note the **IP address of Machine 1** (the master node).

---

## Step 2 — The Training Script (`train_adam_proof.py`)

Save this on **both machines**:

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

# ── Distributed init ──────────────────────────────────────────────────────────
def setup(rank, world_size):
    dist.init_process_group(
        backend="nccl",          # NCCL = best for GPU-to-GPU
        init_method="env://",    # reads MASTER_ADDR / MASTER_PORT from env
        rank=rank,
        world_size=world_size,
    )
    torch.cuda.set_device(0)     # each machine has only 1 GPU

def cleanup():
    dist.destroy_process_group()

# ── Simple CNN model ───────────────────────────────────────────────────────────
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

# ── Train one epoch ────────────────────────────────────────────────────────────
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

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    rank       = int(os.environ["RANK"])        # 0 = machine 1, 1 = machine 2
    world_size = int(os.environ["WORLD_SIZE"])  # 2

    setup(rank, world_size)
    device = torch.device("cuda:0")

    # Dataset
    tf = transforms.Compose([transforms.ToTensor(),
                              transforms.Normalize((0.1307,), (0.3081,))])
    dataset  = datasets.MNIST("./data", train=True, download=True, transform=tf)
    sampler  = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader   = DataLoader(dataset, batch_size=256, sampler=sampler, num_workers=4)
    criterion = nn.CrossEntropyLoss()

    EPOCHS = 20
    results = {}

    # ── Compare optimizers ─────────────────────────────────────────────────────
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
            sampler.set_epoch(epoch)   # ensures different shuffling per epoch
            loss = train_epoch(model, loader, optimizer, criterion, device)
            losses.append(loss)
            if rank == 0:
                print(f"[{name}] Epoch {epoch+1:02d}/{EPOCHS} — Loss: {loss:.4f}")

        results[name] = losses

    # ── Only master node saves & plots ────────────────────────────────────────
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

## Step 3 — Launch on Each Machine

**On Machine 1 (master, e.g. IP = `192.168.1.10`):**

```bash
MASTER_ADDR=192.168.1.10 \
MASTER_PORT=29500 \
RANK=0 \
WORLD_SIZE=2 \
python train_adam_proof.py
```

**On Machine 2:**

```bash
MASTER_ADDR=192.168.1.10 \
MASTER_PORT=29500 \
RANK=1 \
WORLD_SIZE=2 \
python train_adam_proof.py
```

Both machines must run the command **at roughly the same time** — they will handshake via the master address.

> Alternatively, use `torchrun` for cleaner launch:
>
> ```bash
> # Machine 1
> torchrun --nnodes=2 --nproc_per_node=1 \
>          --node_rank=0 --master_addr=192.168.1.10 --master_port=29500 \
>          train_adam_proof.py
>
> # Machine 2
> torchrun --nnodes=2 --nproc_per_node=1 \
>          --node_rank=1 --master_addr=192.168.1.10 --master_port=29500 \
>          train_adam_proof.py
> ```

---

## What to Expect (Proving Adam)

The output plot `optimizer_comparison.png` will show something like:

| Optimizer | Convergence speed | Notes |
| ----------- | ------------------ | ------- |
| **Adam** | ✅ Fast & stable | Best early convergence |
| SGD+momentum | Moderate | Catches up late |
| RMSProp | Similar to Adam | No bias correction |
| AdaGrad | ❌ Slow later | LR decays too aggressively |

This directly reproduces what the paper demonstrates — Adam converges faster and more reliably, especially in the early epochs.

---

## Architecture Overview

```
Machine 1 (RTX 4070)          Machine 2 (RTX 4070)
┌─────────────────────┐        ┌─────────────────────┐
│  RANK=0  (master)   │◄──────►│  RANK=1             │
│  ½ of the dataset   │  NCCL  │  ½ of the dataset   │
│  gradient sync      │  sync  │  gradient sync      │
└─────────────────────┘        └─────────────────────┘
         ↓ averaged gradients across both GPUs
         ↓ each optimizer step uses the full-batch signal
```

With DDP, gradients are **averaged across both GPUs** after each backward pass — so your effective batch size is `256 × 2 = 512`, and training is ~2× faster than single GPU.

---

**References:**

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/pdf/1412.6980)
- [PyTorch Distributed Training Docs](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [torchrun CLI reference](https://pytorch.org/docs/stable/elastic/run.html)
