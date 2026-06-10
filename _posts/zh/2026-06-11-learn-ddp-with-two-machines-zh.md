---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在两台机器上学习DDP
translated: true
type: note
---

**问题：** 我有两台机器（i9-13900KF + RTX 4070 台式机，以及一台无 CUDA 的 i5-12450H 笔记本），在三种 nanochat DDP 选项中，我应该选择哪一个才能真正*学习*分布式训练？

**回答：**

建议按 **步骤 1 → 2 循序渐进作为学习练习（一个晚上完成），然后实际训练时使用选项 3**。它们分别解决不同的问题：

- 选项 1 教您 DDP *机制*（进程组、rank、梯度 allreduce），无需任何网络变量。
- 选项 2 教您分布式训练的 *系统* 现实——会合、NIC 选择、基于以太网的 allreduce 以及落伍者问题。这些知识未来可迁移到多节点 MI300X/H100 集群。
- 选项 3 不教任何新内容（`--nproc_per_node=1` 意味着 DDP 包装单个进程；allreduce 为空操作）。它只是实际训练的正确方式。

### 步骤 1：Gloo 补丁（步骤 1 和 2 均需）

在 `nanochat/common.py` 中，`compute_init()` 函数将 DDP 限制为仅 CUDA。请改为修改后端选择：

```python
# 修改前
if is_ddp_requested and device_type == "cuda":
    init_process_group(backend="nccl")
    ...

# 修改后
if is_ddp_requested:
    backend = "nccl" if device_type == "cuda" else "gloo"
    init_process_group(backend=backend)
    if device_type == "cuda":
        torch.cuda.set_device(ddp_local_rank)
```

Gloo 是 PyTorch 的 CPU 兼容集体后端——通过 TCP 而非 NVLink/IB 实现环形 allreduce。同时确保任何 `torch.compile` 或 bf16 自动类型转换路径在 `device_type == "cpu"` 时不会假定 CUDA。

### 步骤 2：选项 1 —— 在 i9 台式机上本地运行 4 进程 CPU DDP

```bash
torchrun --nproc_per_node=4 --standalone \
    -m scripts.base_train --device-type=cpu --depth=4 --max-seq-len=512 \
    --device-batch-size=1 --total-batch-size=512 --num-iterations=20
```

验证它确实在执行 DDP：打印 `dist.get_world_size()` 并确认步骤 1 后各 rank 的损失值相同（梯度同步 → 权重相同）。然后基准测试 `--nproc_per_node=1` vs `2` vs `4` 的 tokens/sec。您可能会看到次线性扩展，因为 12450H……等等，这是 i9——您会看到良好的扩展性直到物理核心，然后趋于平缓。这条曲线*本身*就是教训。

### 步骤 3：选项 2 —— 跨局域网多节点

首先，**匹配 torch 版本**——在 2.12.0 和 2.9.1 之间使用 Gloo 很可能导致序列化/协议不匹配。将笔记本的版本固定到与工作站相同：

```bash
# 在 i5 笔记本上
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
```

然后，在 i9 台式机上（主节点）：

```bash
export GLOO_SOCKET_IFNAME=<您的以太网接口>   # 通过 ip route get <IP_ADDRESS> 检查
torchrun --nnodes=2 --node_rank=0 --nproc_per_node=2 \
    --master_addr=<主节点IP> --master_port=29500 \
    -m scripts.base_train --device-type=cpu --depth=4 ...
```

在 i5 笔记本上：

```bash
export GLOO_SOCKET_IFNAME=<您的以太网接口>
torchrun --nnodes=2 --node_rank=1 --nproc_per_node=2 \
    --master_addr=<主节点IP> --master_port=29500 \
    -m scripts.base_train --device-type=cpu --depth=4 ...
```

您会观察到两件事，都值得深入了解：

1. **落伍者问题。** DDP 是同步的——每一步都等待最慢的 rank 完成 allreduce。i5 会将 i9 拖慢到自己的速度。这正是生产集群使用同构节点的原因，也是异构环境需要流水线并行或异步方案而非普通 DDP 的原因。
2. **通信开销。** 深度为 4 的 nanochat 模型有数千万参数；allreduce 每步移动约 2×P×4 字节，在（很可能）1 GbE ≈ 125 MB/s 的网络下。计算每步预期的通信时间，然后实际测量。当测量值远大于计算值时，您就发现了分桶/延迟开销——这与您在真实集群上确定互联规模时所做的分析完全相同。

### 然后：实际训练使用选项 3

对于 Transformer 训练（张量核心 + bf16），RTX 4070 的速度将比两种 CPU 设置快 1-2 个数量级。学习练习完成后，`run_rtx4070.sh` 就是正确的工具——而您从步骤 1-2 获得的思维模型下次租用 8×MI300X 节点时可直接映射到 `--nproc_per_node=8` 的 NCCL 运行。

建议产出一个具体成果：一张 tokens/sec 对比表（{1 进程 CPU, 4 进程 CPU, 2 节点 CPU, 单 4070}），加上每步实测 allreduce 时间。这将是一篇值得写博客的基准测试，迫使您对代码进行检测而非仅仅运行。
