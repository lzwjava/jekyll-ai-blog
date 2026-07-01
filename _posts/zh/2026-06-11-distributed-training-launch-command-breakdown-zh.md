---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式训练启动命令解析
translated: true
type: note
---

**问题：** 解释这个 SSH + tmux + torchrun 命令中的每个参数，该命令用于启动 nanochat 的 2 节点分布式 CPU 训练运行的 master 节点。

**回答：**

这是一个分层命令：`ssh → tmux → shell → torchrun → base_train`。逐层分解。

## 第 1 层 — SSH 封装

```bash
ssh lzw@<WORKSTATION_IP> "..."
```

在您的 Ubuntu 工作站上以远程 shell 命令的形式执行引号内的字符串。末尾的 `&& echo OK` 仅在 tmux 会话创建成功时打印 `OK` —— 向您的 Mac 发送一个简单的成功信号。最后的 `0.6` 不是命令的一部分 —— 看起来是一个粘贴时残留的额外字符（可能是 Warp 时间标注或 shell 历史片段）。如果它在引号内，shell 会将其视为 `echo OK` 的一个参数；根据现有写法，它位于结束引号之后，因此 `ssh` 实际上会将其作为附加的远程命令文本（以空格连接）发送，即远程会执行 `... && echo OK 0.6`。无害，但应删除。

## 第 2 层 — tmux 会话管理

```bash
tmux kill-session -t dist-master 2>/dev/null
```

幂等性：终止任何先前名为 `dist-master` 的会话，以便重新运行命令时不会因“重复会话”而失败。`2>/dev/null` 在首次运行时吞掉“会话未找到”的错误。

```bash
tmux new-session -d -s dist-master '...'
```

- `-d` — 分离模式：创建会话但不附加终端。这很关键，因为 SSH 会断开连接；tmux 会保持训练进程存活（即使 SSH 会话结束也不受影响）。
- `-s dist-master` — 会话名称，方便您稍后使用 `tmux attach -t dist-master` 查看实时输出。
- 引号内的字符串是会话要运行的命令。当命令退出时，会话结束 —— 因此末尾的 `sleep 600` 可以在训练结束后保持窗格存活 10 分钟，以便您附加后查看最终的输出/错误信息，然后 tmux 才会回收它。

```bash
2>&1 | tee /tmp/dist_master.log
```

将标准错误合并到标准输出（torchrun 和 PyTorch 大量记录日志到标准错误），然后 `tee` 将数据流复制到 tmux 窗格和日志文件中，您可以从另一个 SSH 会话中使用 `tail -f` 查看该日志。

## 第 3 层 — 环境变量

| 变量 | 目的 |
| --- | --- |
| `NANOCHAT_BASE_DIR=~/.cache/nanochat` | nanochat 的根目录，用于存放分词器、检查点、评估包 |
| `NANOCHAT_DATA_DIR=.../base_data_small` | 将预训练指向您的 FineWeb 小分片子集，而不是完整数据集 |
| `NANOCHAT_FORCE_SDPA=1` | 强制 PyTorch 使用 `scaled_dot_product_attention` 而非 FlashAttention —— 在 CPU 上是必要的，因为那里没有 FA 内核 |
| `OMP_NUM_THREADS=8` | 限制每个进程用于 CPU 矩阵乘法的 OpenMP 线程数。没有这个限制，每个 rank 都会尝试占用所有核心；在 2 节点 × 每节点 1 进程的情况下，8 个线程可以避免过度订阅 |
| `PYTHONUNBUFFERED=1` | 禁用 Python 的标准输出缓冲，以便 `tee` 和日志文件能实时获取行，而不是按 8KB 块输出 |
| `GLOO_SOCKET_IFNAME=enp4s0` | 告诉 Gloo 后端（CPU 集合通信后端）绑定到哪个网络接口。缺少此设置，Gloo 可能选择 `lo` 或 Docker 网桥，导致 rank 1 无法连接 |
| `NCCL_SOCKET_IFNAME=enp4s0` | 对 NCCL 做相同设置 —— 这里无害，因为 CPU 训练使用 Gloo，但如果您切换为 GPU，这可以作为廉价保险 |

`IFNAME` 配对是多节点设置中最容易出错的部分。错误的接口会导致 rendezvous 在“等待 workers”阶段永远挂起。

## 第 4 层 — torchrun（启动器）

```bash
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
  --master_addr=<WORKSTATION_IP> --master_port=29500 \
  -m scripts.base_train -- ...
```

- `--nnodes=2` — 世界中包含 2 台机器。torchrun 会阻塞，直到两个节点完成 rendezvous。
- `--nproc_per_node=1` — 每台机器 1 个工作进程（每个 CPU rank 一个）。总世界大小 = 2 × 1 = 2。
- `--node_rank=0` — 本机是 master（rank-0 主机）。您的第二台机器将运行相同的命令，但使用 `--node_rank=1`。
- `--master_addr` / `--master_port=29500` — TCP rendezvous 点。Rank 0 在此监听；rank 1 连接到此地址。两个节点必须传递相同的地址/端口。
- `-m scripts.base_train` — 将训练脚本作为模块运行（以便 `scripts/` 包的导入从 nanochat 仓库根目录解析，这就是前面 `cd` 命令重要的原因）。
- `--` — 分隔符：之后的所有内容都将传递给 `base_train` 的参数解析器，而非 torchrun。

torchrun 会在每个生成进程中设置 `RANK`、`LOCAL_RANK`、`WORLD_SIZE`、`MASTER_ADDR`、`MASTER_PORT` 环境变量；`base_train` 在其 `dist.init_process_group()` 调用中读取这些变量。

## 第 5 层 — base_train 参数（模型和运行配置）

- `--device-type cpu` — 使用 Gloo 后端，不使用 CUDA。这是分布式训练的基础设施测试，而非真正运行。
- `--depth 4` — 4 个 transformer 层。nanochat 从深度推导架构的其余部分：
- `--aspect-ratio 64` — `model_dim = depth × aspect_ratio = 4 × 64 = 256`。因此是一个 256 维模型。
- `--head-dim 64` — 对于 `model_dim=256`，即 `256/64 = 4` 个注意力头。
- `--max-seq-len 512` — 上下文长度为 512 个 token（使注意力计算在 CPU 上的成本保持很低）。
- `--device-batch-size 2` — 每个 rank 每次前向传播的微批次：2 个序列 × 512 个 token = 每步每 rank 1,024 个 token。
- `--total-batch-size 2048` — 每次优化器步骤的目标 token 数。梯度累积由此推导：`2048 / (2 ranks × 1024 tokens) = 1` 个累积步骤。因此每个优化器步骤正好是每个 rank 进行一次前向/反向传播，然后执行一次 Gloo all-reduce。
- `--num-iterations 10` — 仅 10 个优化器步骤。纯粹的冒烟测试。
- `--eval-every 5` — 在第 5 步和第 10 步运行验证损失。
- `--eval-tokens 2048` — 仅对 2,048 个 token 进行评估（一个很小的验证批次）。
- `--core-metric-every -1` — 完全禁用 CORE 基准评估（`-1` = 从不）。对于一个 10 步的 CPU 运行来说，它过于昂贵。
- `--sample-every 10` — 在第 10 步生成示例文本，以便您可以目测输出（在这个规模下会是胡言乱语）。
- `--tracker none` — 不使用 wandb/日志后端。
- `--run dist-cpu-2node` — 运行名称，用于检查点/日志目录命名。

## 思维模型

整个命令的存在是为了回答一个问题：*我的 2 节点 Gloo rendezvous 和梯度 all-reduce 能否在局域网内工作？* 每个模型超参数都被压缩到接近零（深度 4，维度 256，10 步），因此运行在几分钟内完成，任何失败都是网络问题，而非计算问题。一旦打印出 `OK` 并且日志显示两个 rank 同步前进，您就可以交换 `--device-type`、IFNAME 后端和模型大小，进行真正的运行。

需要验证的一点：rank 1 的命令必须在 `--nnodes`、`--master_addr`、`--master_port`、总批次大小和所有模型参数上匹配 —— torchrun 不会捕获超参数不匹配的问题，而 rank 之间配置不一致会导致静默的形状错误或在第一次集合通信时挂起。
