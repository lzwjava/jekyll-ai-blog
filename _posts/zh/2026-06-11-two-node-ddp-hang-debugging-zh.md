---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双节点DDP挂起调试
translated: true
type: note
---

**问题：** 解释这段记录中发生的情况——一个智能体（Hermes）正在调试一次卡死状态的分布式双节点 nanochat CPU 训练运行。

**回答：**

这是一次经典的 DDP（分布式数据并行）卡死调试过程。你的智能体使用 `torchrun` 并通过 **gloo** 后端（纯 CPU 通信）在两台机器（主节点 `.36` 使用以太网，工作节点 `.47` 使用 WiFi）上运行 nanochat 的 `base_train`，然后运行就卡死了。以下是详细过程：

**1. 诊断卡死：0% CPU = 阻塞在集合通信中**

```bash
top -b -n1 -p 603 | tail -3   # 主节点 PID
top -b -n1 -p 52262 | tail -3 # 工作节点 PID
```

两个进程都存活，但 CPU 使用率为 0%。这是进程阻塞在集合操作（如 `all_reduce`、`broadcast`）内部的网络 `recv()` 调用上的典型特征 — 不在计算，也没有崩溃，只是在无限等待永远不会到达的同伴。如果只是计算慢，你应该会看到大约 100% 的 CPU 使用率。尝试使用 `strace -e trace=network` 是正确的直觉（你会看到进程停在了 `recvfrom`/`poll` 上），尽管 shell 语法中 `&;` 使用有误。

**2. 第一个假设：数据分片不匹配**

主节点有 201 个 parquet 文件（`base_data_climbmix`），工作节点只有 4 个（`base_data_small`）。在 DDP 中，这是导致死锁的真正原因：每个 rank（进程）的数据加载器独立迭代，梯度通过`每个步骤`的 `all_reduce` 进行同步。如果 rank 0 认为有比 rank 1 更多的批次，那么 rank 1 会退出其循环，而 rank 0 则阻塞在 `all_reduce` 中等待同伴 — 导致永久卡死，且没有错误。因此，智能体将两者都固定到 `NANOCHAT_DATA_DIR=.../base_data_small`（值得注意的是，它在重启时仅在主节点上导出了该变量 — 值得检查工作节点是否解析到了相同的分片）。

**3. 实际发现：在 CPU 运行中自动检测到 bf16**

日志显示 `COMPUTE_DTYPE: torch.bfloat16 (auto-detected: CUDA SM 89)`。数据类型选择逻辑检查了 `torch.cuda.is_available()` — 在 `.36` 上为 true，因为 RTX 4070（SM 8.9 = Ada）物理存在 — 即使训练是使用 `--device-type cpu` 启动的。所以它为一个 CPU 运行选择了 bf16。PyTorch 的 CPU bf16 内核在没有 AMX/AVX512-BF16 支持的芯片上（大量上下转换，融合路径较少）比 fp32 慢得多。修复方法：`export NANOCHAT_DTYPE=float32`。

智能体忽略了一个小细节：bf16 速度慢和集合通信卡死是`不同`的症状（高 CPU 使用率 vs 0% CPU 使用率）。很可能两者都在起作用——例如，一个 rank 在 bf16 初始化/评估阶段缓慢爬行，而另一个 rank 则在第一个同步点处阻塞，看起来像是死锁。重启同时处理了这两个可能的原因，这很实用，但无法隔离究竟是哪个原因真正导致了卡死。

**4. 解码重启命令**

```bash
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
  --master_addr=<MASTER_IP> --master_port=29500 \
  -m scripts.base_train -- --device-type cpu --depth 4 \
  --aspect-ratio 64 --head-dim 64 --max-seq-len 512 \
  --device-batch-size 2 --total-batch-size 2048 ...
```

- `GLOO_SOCKET_IFNAME=enp4s0` / `wlp3s0` — 将 gloo 绑定到正确的网卡。没有这个，gloo 可能会绑定到 docker 网桥或虚拟接口，导致各个 rank 永远找不到彼此（另一个静默卡死的来源）。明智的包含。
- `NANOCHAT_FORCE_SDPA=1` — 跳过 FlashAttention（仅限 CUDA），使用 PyTorch SDPA。
- 模型计算：`depth=4`，`aspect_ratio=64` → d_model = 256；`head_dim=64` → 4 个头。一个大约 3-5M 参数的小模型，适合用于 CPU 连接测试。
- 批次计算：2 个 rank × batch size 2 × 序列长度 512 = 2048 个 tokens = `total_batch_size`，所以恰好是每个优化器步长对应 1 个微步长，零梯度累积 — 每一步都执行一次 all-reduce。

**一个需要注意的地方：** 工作节点通过 WiFi（`wlp3s0`）同步梯度。即使对于这个很小的模型，每一步都需要双向传输完整的梯度；在 WiFi 延迟下，这个 all-reduce 操作将主导步长时间。对于 10 次迭代的冒烟测试来说没问题，但对于任何实际运行，请让 `.47` 使用以太网 — gloo 环状 all-reduce 在 WiFi 上是瓶颈，而不是 CPU。