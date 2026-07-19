---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linking Two RTX 3090s Setup
translated: false
type: note
---

Question: How do I physically and logically link two RTX 3090s — same motherboard, NVLink, or across a network — for training/inference?

Answer:

**1. Same motherboard, no NVLink (PCIe P2P through CPU/chipset)**

Just two PCIe x16 slots (ideally x8/x8 electrical minimum, x16/x16 if your CPU has enough lanes — e.g. Threadripper/EPYC/HEDT, not consumer i5/i7/Ryzen which only give 20-24 lanes total).

Check topology:
```bash
nvidia-smi topo -m
```
Output matrix shows `PIX` (same PCIe switch), `PXB` (multiple switches), `PHB` (host bridge/CPU), `SYS` (crosses NUMA/QPI) — worse as you go down that list. Consumer boards usually show `PHB` between two GPUs on different CPU-attached slots.

Bandwidth here: whatever your PCIe gen/lanes give you (PCIe 4.0 x16 ≈ 32GB/s each way), no direct GPU-to-GPU DMA unless P2P is enabled:
```bash
# check P2P capability
nvidia-smi topo -p2p r
```

**2. NVLink bridge (RTX 3090 specific)**

3090 is the *last* consumer card with NVLink (4090 dropped it entirely). You need:
- A physical NVLink bridge (3-slot spacing, "RTX NVLink Bridge" not the old SLI HB one — check slot spacing matches your board)
- Two 3090s in slots exactly 3-slots apart (varies by board)

Gives you ~56GB/s unidirectional / ~112GB/s bidirectional, direct GPU-to-GPU, bypassing CPU/PCIe entirely for that pair.

Verify it's active:
```bash
nvidia-smi nvlink -s
nvidia-smi nvlink -c
```

Caveat: consumer NVLink on 3090 is **not** the same as datacenter NVSwitch (A100/H100) — it's point-to-point, only connects that one pair, no fabric, and PyTorch/NCCL treat it just as a faster P2P link, not a special topology.

**3. Two separate workstations over Ethernet**

No physical GPU link — you're doing distributed training over the network stack. NCCL over TCP:

```bash
# node 0 (master)
NCCL_SOCKET_IFNAME=eth0 \
torchrun --nproc_per_node=1 --nnodes=2 --node_rank=0 \
  --master_addr=<MASTER_IP> --master_port=29500 train.py

# node 1
NCCL_SOCKET_IFNAME=eth0 \
torchrun --nproc_per_node=1 --nnodes=2 --node_rank=1 \
  --master_addr=<MASTER_IP> --master_port=29500 train.py
```

Plain 1GbE/10GbE will bottleneck gradient all-reduce badly for anything beyond small models — this is why real clusters use InfiniBand (100-400Gb/s) or at minimum RoCE (RDMA over Converged Ethernet). For two 3090 boxes on regular Ethernet, expect this to only make sense for data-parallel with infrequent sync (e.g. gradient accumulation heavy, or pipeline parallel with small activations crossing the wire), not tight sync every step.

**Practical recommendation for your setup:**

If it's inference/training on one box: skip NVLink unless you're doing tensor-parallel (splitting a single model's layers across both GPUs) — for that, the interconnect bandwidth actually matters (e.g. `vllm` or `deepspeed` tensor parallelism). For data-parallel (each GPU trains a full replica, just averaging grads), PCIe P2P is usually fine, NVLink is a nice-to-have.

If it's two separate boxes: don't bother trying to make it look like local multi-GPU — treat it as multi-node NCCL with `NCCL_IB_DISABLE=1` (if no InfiniBand) and tune `NCCL_SOCKET_IFNAME` to your NIC. Check actual achievable bandwidth first:
```bash
# quick NCCL bandwidth test between nodes
git clone https://github.com/NVIDIA/nccl-tests
cd nccl-tests && make
mpirun -np 2 -H node0,node1 ./build/all_reduce_perf -b 8 -e 128M -f 2
```

References:
- [NCCL Tests](https://github.com/NVIDIA/nccl-tests)
- [PyTorch Distributed - torchrun](https://pytorch.org/docs/stable/elastic/run.html)
- [NVIDIA NCCL Environment Variables](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)
