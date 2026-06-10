---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主从torchrun命令差异
translated: true
type: note
---

**问题：** 在这个双节点 CPU 分布式 nanochat 训练设置中，主节点和工作节点的 torchrun 启动命令有何区别？

**回答：**

差异对比（主 → 工作）：

```diff
- ssh lzw@<MASTER_IP>          tmux 会话: dist-master
+ ssh xiaoxin@<WORKER_IP>      tmux 会话: dist-worker

- cd /mnt/data/nanochat
+ cd ~/projects/nanochat

- export NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small
+ （工作节点未设置）

- export OMP_NUM_THREADS=8
+ export OMP_NUM_THREADS=4

- export GLOO_SOCKET_IFNAME=enp4s0    # 有线以太网
+ export GLOO_SOCKET_IFNAME=wlp3s0    # WiFi

- --node_rank=0
+ --node_rank=1

- tee /tmp/dist_master.log
+ tee /tmp/dist_worker.log
```

其余所有内容——`--nnodes=2 --nproc_per_node=1 --master_addr --master_port=29500` 以及所有训练参数（`--depth 4 --aspect-ratio 64 --head-dim 64 --max-seq-len 512 --device-batch-size 2 --total-batch-size 2048 --num-iterations 10` 等）完全相同，这是正确的：torchrun 要求匹配全局拓扑，而训练脚本要求各 rank 的超参数一致。

每项差异的含义：

1. **`--node_rank=0` vs `1`** —— 唯一必须不同的 torchrun 参数。Rank 0 在 `master_addr:29500` 上托管 rendezvous (TCPStore)；rank 1 连接到它。由于 `nproc_per_node=1`，全局 rank 变为 0 和 1。

2. **仅主节点设置 `NANOCHAT_DATA_DIR`** —— 潜在 bug。在 DDP 中，*每个* rank 加载自己的数据分片；nanochat 的数据加载器使用 `ddp_rank` 跨分片步进。如果工作节点回退到空的或不同的默认数据目录，rank 1 将因缺少文件而崩溃，或在不同数据上训练。请检查工作节点在其默认路径（通常为 `$NANOCHAT_BASE_DIR/base_data`）下是否有相同的 `base_data_small` 分片。更安全的做法：在两端明确设置该变量。

3. **`GLOO_SOCKET_IFNAME` / `NCCL_SOCKET_IFNAME`** —— 将集合通信后端固定到特定网卡。主节点使用有线（`enp4s0`），工作节点使用 WiFi（`wlp3s0`）。由于是 `--device-type cpu`，只有 Gloo 起作用；此处 `NCCL_SOCKET_IFNAME` 无效。WiFi 链路将成为梯度全规约的瓶颈——即使是一个极小的 depth-4 模型，每一步都需要同步，而 WiFi 延迟（约 2-10ms RTT，加上抖动）将主导性能。预计有线→WiFi 的跳转会将吞吐量限制在远低于任一 CPU 计算能力以下的水平。

4. **`OMP_NUM_THREADS=8` vs `4`** —— 针对每台机器的核心数进行调优。没问题，但注意 DDP 每一步都等待最慢的 rank，因此 4 线程的工作节点决定了整体速度。如果工作节点有闲置核心，提高此值可直接加速整个任务。

5. **路径/用户/会话名称** —— 外观性差异，每台主机布局不同。

下次运行前的快速检查：

```bash
# 验证工作节点是否在其期望位置有数据
ssh xiaoxin@<WORKER_IP> 'ls ~/.cache/nanochat/base_data* 2>/dev/null | head'
```

如果通过 WiFi 的梯度同步拖慢了步进时间，你可以测量它：比较单节点运行（`--nnodes=1`）在主节点上的 `tok/s` 与双节点运行的结果——差距几乎全部来自无线链路上的 Gloo 全规约。