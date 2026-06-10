---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 三台CPU笔记本电脑上的DDP
translated: true
type: note
---

**问题：** 只用三台仅有 CPU 的 Ubuntu 笔记本电脑会怎样？

**答案：**

与两台的情况相同：吞吐量略有提升，其他方面则稍逊一筹。代码除了 `--nnodes=3` 之外无需任何改动——DDP 不在意节点数或是否为 2 的幂。真正有趣的是数学层面的变化。

**通信成本呈亚线性增长——环形 all-reduce 公式：**

环形 all-reduce 在每个 rank 上移动 `2(N-1)/N × D` 字节，其中 `D` 为梯度大小：

| N | 负载系数 | GPT-2 124M（496 MB 梯度）在千兆以太网上 |
|---|----------|----------------------------------------|
| 2 | 1.00×    | ~4.5 s                                 |
| 3 | 1.33×    | ~6.0 s                                 |
| ∞ | 2.00×（渐近线） | ~9 s 上限                          |

CPU 反向传播仍需约 15–30 秒，因此通信开销仍被隐藏。预期加速比：**约 2.6–2.8 倍于单台笔记本电脑**。all-reduce 成本收敛于与 N 无关的常数 2× 负载，这正是数据并行能扩展到数千 GPU 的原因——你在玩具规模上看到了相同的渐近线。

一个拓扑注意事项：所有三台机器都连接到同一个千兆**交换机**（你路由器的 LAN 口也算）。每个环形链路都是一个独立的全双工端口到端口路径，因此交换机不会成为瓶颈。不要串联连接或混入 WiFi。

**启动——同一脚本，三个命令：**

```bash
# 笔记本电脑 A（rank 0，主节点）
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=0 --nproc_per_node=1 \
  --master_addr=<LAPTOP_A_LAN_IP> --master_port=29500 dist_train.py
# 笔记本电脑 B
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=1 ... # 相同标志
# 笔记本电脑 C
OMP_NUM_THREADS=$(nproc) torchrun --nnodes=3 --node_rank=2 ... # 相同标志
```

**在 N=3 时，有三件事开始显现，而 N=2 时它们并不明显：**

1. **Straggler tail statistics.** 每一步都等待 `max(t_1, t_2, t_3)`。在相同硬件上，每步时间是步骤时间分布中 N 个样本的*最大值*——而这个最大值随 N 增长。如果某台笔记本电脑在持续 AVX 负载下发生热降频（这是笔记本电脑的典型行为），整个任务就会被拖慢。缓解措施：`cpupower frequency-set -g performance`，垫高/散热笔记本电脑，在每个节点上运行 `watch -n1 'grep MHz /proc/cpuinfo'`。

2. **容错现在是个真正的问题。** 合上盖子、WiFi 省电模式启动、某个 rank 挂掉→其他两个 rank 会在下一次 all-reduce 时永久挂起（gloo 默认没有心跳）。两种修复方式：

```bash
# (a) 超时，使挂起变成错误
torchrun ... --rdzv_backend=c10d --rdzv_endpoint=<LAPTOP_A_LAN_IP>:29500
# 在代码中：dist.init_process_group("gloo", timeout=datetime.timedelta(seconds=120))

# (b) 弹性训练——可容忍节点丢失，重新缩放 world_size
torchrun --nnodes=1:3 --max_restarts=3 \
  --rdzv_backend=c10d --rdzv_endpoint=<LAPTOP_A_LAN_IP>:29500 dist_train.py
```

   弹性训练（`--nnodes=min:max`）值得在这套设备上尝试一次——它是容错集群作业背后的机制，你为其编写的 checkpoint/resume 逻辑可以直接迁移到真正的训练任务中。

3. **全局批次大小与 LR 缩放规则。** 假设每个 rank 的批大小为 32，那么在整个实验中你的全局批次大小从 32 变为 64 再变为 96。相同的超参数 ≠ 相同的训练动力学。标准配方（Goyal 等人，"Accurate, Large Minibatch SGD"）：将学习率与全局批次大小线性缩放，并包含预热阶段：

```python
base_lr = 3e-4          # 在全局批次为 32 时调参得到
lr = base_lr * (dist.get_world_size() * per_rank_bs) / 32
# + 在前约 200-500 步进行线性预热
```

   在 N=3、模型很小的情况下你几乎不会注意到差异，但当人们发现一个在 1 节点上收敛的任务在 8 节点上莫名其妙地发散时，往往就是忘记了这个旋钮。

**收益递减检查：** 1 台笔记本 = 1.0×，2 台 ≈ 1.9×，3 台 ≈ 2.7×，而且每增加一台笔记本也会增加一张 straggler 彩票和一个故障点。与此同时，4070 仍然是整个三人组的 15–20 倍。所以诚实的表述和之前一样：这是一个**分布式系统实验室，而非计算策略**——而且是一个真正的好实验室。一个 3 节点弹性 gloo 集群能够锻炼 rendezvous、环形集合、straggler、故障恢复和批次大小缩放——这些正是 512-GPU 任务的精确故障模式，而且零成本。在上边跑 nanoGPT shakespeare-char，中途杀掉一个节点，观察弹性恢复，然后去租用 MI300X 来做真正的工作。