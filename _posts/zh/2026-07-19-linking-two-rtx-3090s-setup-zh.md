---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双RTX 3090连接设置
translated: true
type: note
---

问题：如何物理和逻辑地连接两块RTX 3090——同一主板、NVLink或通过网络——用于训练/推理？

回答：

**1. 同一主板，无NVLink（通过CPU/芯片组的PCIe P2P）**

只需两个PCIe x16插槽（理想情况下至少x8/x8电气，如果你的CPU有足够通道则x16/x16——例如Threadripper/EPYC/HEDT，而非消费级i5/i7/Ryzen，它们总共只有20-24通道）。

检查拓扑：
```bash
nvidia-smi topo -m
```
输出矩阵显示 `PIX`（同一PCIe交换机）、`PXB`（多个交换机）、`PHB`（主机桥接器/CPU）、`SYS`（跨NUMA/QPI）——越往下性能越差。消费级主板通常在两个GPU位于不同CPU连接的插槽时显示 `PHB`。

此处的带宽取决于你的PCIe代数和通道数（PCIe 4.0 x16 每个方向约32GB/s），除非启用P2P，否则无直接GPU到GPU的DMA：
```bash
# 检查P2P能力
nvidia-smi topo -p2p r
```

**2. NVLink桥接器（RTX 3090专用）**

3090是*最后*一款支持NVLink的消费级显卡（4090完全取消了该功能）。你需要：
- 一个物理NVLink桥接器（3槽间距，“RTX NVLink Bridge”而非旧的SLI HB桥接器——检查槽间距是否与你的主板匹配）
- 两块3090安装在恰好相隔3个槽位的插槽中（因主板而异）

可实现约56GB/s单向 / 112GB/s双向，直接GPU到GPU通信，完全绕过CPU/PCIe。

验证是否激活：
```bash
nvidia-smi nvlink -s
nvidia-smi nvlink -c
```

注意：消费级3090的NVLink**不同于**数据中心NVSwitch（A100/H100）——它是点对点连接，仅连接一对GPU，无交换结构，PyTorch/NCCL仅将其视为更快的P2P链接，而非特殊拓扑。

**3. 两台独立工作站通过以太网连接**

无物理GPU链接——通过网络栈进行分布式训练。NCCL over TCP：

```bash
# 节点0（主节点）
NCCL_SOCKET_IFNAME=eth0 \
torchrun --nproc_per_node=1 --nnodes=2 --node_rank=0 \
  --master_addr=<MASTER_IP> --master_port=29500 train.py

# 节点1
NCCL_SOCKET_IFNAME=eth0 \
torchrun --nproc_per_node=1 --nnodes=2 --node_rank=1 \
  --master_addr=<MASTER_IP> --master_port=29500 train.py
```

普通的1GbE/10GbE会严重限制梯度的All-Reduce操作，仅适用于小模型——这就是为什么真正的集群使用InfiniBand（100-400Gb/s）或至少RoCE（融合以太网上的RDMA）。对于两台3090机器通过普通以太网连接，预计仅适用于同步频率较低的数据并行（例如大量梯度累积，或跨网络传输小激活值的流水线并行），而非每一步紧密同步。

**对你的设置的实际建议：**

如果是单机推理/训练：除非你正在进行张量并行（将单个模型的层拆分到两个GPU上）——此时互连带宽确实重要（例如`vllm`或`deepspeed`的张量并行），否则可以跳过NVLink。对于数据并行（每个GPU训练完整副本，仅平均梯度），PCIe P2P通常足够，NVLink是锦上添花。

如果是两台独立机器：不要试图将其模拟成本地多GPU——将其视为多节点NCCL，设置`NCCL_IB_DISABLE=1`（如果没有InfiniBand），并调整`NCCL_SOCKET_IFNAME`指向你的网卡。首先检查实际可达到的带宽：
```bash
# 节点间快速NCCL带宽测试
git clone https://github.com/NVIDIA/nccl-tests
cd nccl-tests && make
mpirun -np 2 -H node0,node1 ./build/all_reduce_perf -b 8 -e 128M -f 2
```

参考：
- [NCCL Tests](https://github.com/NVIDIA/nccl-tests)
- [PyTorch Distributed - torchrun](https://pytorch.org/docs/stable/elastic/run.html)
- [NVIDIA NCCL Environment Variables](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)