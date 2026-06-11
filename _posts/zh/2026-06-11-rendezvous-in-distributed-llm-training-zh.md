---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式大语言模型训练中的会合
translated: true
type: note
---

**问题：** 在计算领域，尤其是分布式大语言模型训练中，“rendezvous”是什么意思？

**回答：**

## 核心概念

“Rendezvous”（法语原意“会合点”）在计算领域中指：**多个独立进程约定好会合、同步并交换信息，然后再一同继续前进。** 在所有预期参与者都到达之前，不会有任何进程向前推进。

## 在分布式大语言模型训练中（你关心的含义）

当你使用 `torchrun` 启动多 GPU / 多节点训练时，**rendezvous** 是所有工作节点启动的引导阶段：

1. **互相发现** —— 每个进程联系一个已知端点（rendezvous 后端，通常是主节点上的 TCPStore）
2. **确认成员资格** —— 确保恰好有 `world_size` 个工作节点存在
3. **分配 rank** —— 每个进程获得唯一的 `rank`（0..N-1）和 `local_rank`
4. **建立通信组** —— rendezvous 之后，创建 NCCL/Gloo 进程组，以便执行 `all_reduce`、`all_gather` 等操作

这就是每个分布式 PyTorch 脚本都以如下代码开头的原因：

```python
import torch.distributed as dist

# 这个调用会阻塞，直到所有 world_size 个进程完成 rendezvous
dist.init_process_group(
    backend="nccl",
    init_method="env://",   # 读取 MASTER_ADDR、MASTER_PORT、RANK、WORLD_SIZE
)
rank = dist.get_rank()
world_size = dist.get_world_size()
```

在启动器一侧，rendezvous 相关的参数是显式指定的：

```bash
# 节点 0（主节点）
torchrun \
  --nnodes=2 --nproc_per_node=8 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=<IP_ADDRESS>:29500 \
  --rdzv_id=my_job_42 \
  train.py

# 节点 1 —— 相同的命令，相同的 rdzv_endpoint
```

- `--rdzv_backend=c10d`：PyTorch 内置的基于 TCPStore 的 rendezvous（无需 etcd）
- `--rdzv_endpoint`：会合点 —— 所有节点连接的 host:port
- `--rdzv_id`：作业 ID，防止同一集群上的两个作业意外互相加入

## 底层工作原理（c10d 后端）

主节点运行一个 `TCPStore`。每个工作节点大致执行以下操作：

```python
# 简化版的 init_process_group 内部心理模型
store = TCPStore(master_addr, master_port, world_size, is_master=(rank == 0))
store.set(f"worker_{rank}", my_nccl_info)      # 宣告自己的存在
store.wait([f"worker_{r}" for r in range(world_size)])  # 阻塞直到所有人都到达
# rank 0 生成 NCCL 唯一 ID，其他节点从 store 中读取
# → 构建 NCCL 通信器，开始训练
```

这个阻塞的 `wait` **就是** rendezvous。如果一个节点启动缓慢，所有节点都会等待。如果它从未到达，你会在 `--rdzv_timeout`（默认 600 秒）之后看到经典的 `timeout in rendezvous` 错误。

## Elastic rendezvous

`torchrun`（TorchElastic）对此进行了扩展：当工作节点崩溃或加入时，rendezvous 可以**重新运行**。使用 `--nnodes=2:4`（最小值:最大值），如果一个节点崩溃，幸存的工作节点会重新 rendezvous、重新分配 rank、从检查点恢复并继续。此时 rendezvous 不再是一次性引导，而是一个重复进行的共识轮次。这就是容错的大规模训练（以及 DeepSeek 风格的上千 GPU 运行）能够在硬件故障时无需重启整个作业而存活的方式。

## 该词出现的其他场景

- **Rendezvous hashing (HRW)**：一致性哈希的替代方案 —— 每个节点计算 `hash(key, node)` 得分，最高分胜出。用于 KV 缓存分片和推理集群中的请求分发。
- **Ada/CSP rendezvous**：同步消息传递，发送方和接收方必须同时到达后才能传输数据（与异步队列相对）。
- **Kubernetes/Slurm ML 作业**：rendezvous 端点就是你的作业配置中无头服务或 `MASTER_ADDR` 环境变量所指向的位置。

## 在你的 RTX 4070 机器上快速实验

单机单 GPU，但你仍然可以通过两个 CPU 进程观察 rendezvous 的发生：

```bash
torchrun --nproc_per_node=2 --rdzv_backend=c10d \
  --rdzv_endpoint=localhost:29500 - <<'EOF'
import os, torch.distributed as dist
dist.init_process_group("gloo")
print(f"rank {dist.get_rank()}/{dist.get_world_size()} rendezvoused, pid={os.getpid()}")
dist.barrier()  # 另一个微型 rendezvous：所有 rank 在这里会合
dist.destroy_process_group()
EOF
```

中途杀掉一个进程，你就会看到 rendezvous/timeout 机制被触发 —— 这在将 nanoGPT 扩展到 MI300X 云上的多节点训练之前，是一种有用的直觉培养。

**参考资料：**

- [PyTorch Elastic Rendezvous 文档](https://pytorch.org/docs/stable/elastic/rendezvous.html)
- [torchrun 文档](https://pytorch.org/docs/stable/elastic/run.html)
- [Rendezvous hashing (Wikipedia)](https://en.wikipedia.org/wiki/Rendezvous_hashing)