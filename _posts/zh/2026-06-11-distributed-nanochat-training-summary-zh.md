---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式NanoChat训练总结
translated: true
type: note
---

以下是完整情况。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NANOCHAT 2节点 CPU DDP — 综合总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

架构
  协议：PyTorch DDP (DistributedDataParallel) 通过 Gloo 后端
  传输：TCP（静态 rendezvous，无 Etcd/C10d）
  Rendezvous：master:29500 (TCPStore)
  数据传输：Gloo 通过以太网（临时端口，双向）

机器
  MASTER — lzw@192.168.1.36
    操作系统：Ubuntu 24.04 (MSI MS-7E01)
    CPU：i9（多核，约62 GB 内存）
    GPU：RTX 4070 12 GB（未使用 — 仅 CPU 训练）
    角色：rank 0，在 :29500 上托管 TCPStore，运行 MLflow tracker
    接口：enp4s0
    tmux：nanochat-master
    脚本：/mnt/data/nanochat/run_dist_cpu_master.sh

  WORKER — xiaoxin@192.168.1.28
    操作系统：Linux Mint（USB 以太网适配器）
    内存：约16 GB
    角色：rank 1，连接到 master 的 TCPStore
    接口：enx00e04c362f89
    tmux：nanochat-worker（空窗格 — 输出进入后台进程）
    脚本：~/projects/nanochat/run_dist_cpu_worker.sh
    防火墙：用户开放了端口（之前阻止了 Gloo 临时端口）

模型
  名称：d8（nanochat 架构）
  参数：125,829,354（总共约126M，并非标注的80M）
  分解：
    wte（词嵌入）：16.8M
    value_embeds：67.1M  ← 参数量主体
    lm_head：16.8M
    transformer_matrices：25.2M
    scalars：42
  配置：
    sequence_len：1024
    vocab_size：32,768
    n_layer：8
    n_head：4
    n_kv_head：4
    n_embd：512
    window_pattern：SSSL（滑动窗口，PyTorch SDPA 回退 — 无 flash-attn）

训练配置
  设备：CPU（float32，NANOCHAT_DTYPE=float32）
  批次：2（设备）× 1024（序列）× 2（rank）= 4,096 tokens/步
  梯度累积：1（无需累积）
  迭代次数：5,000
  总 tokens：20,480,000（约20.5M）
  每个参数的 tokens：0.16（比例非常低 — 预期欠拟合）
  FLOPs 估算：5.6 × 10^15
  OMP 线程：8（master），4（worker）

超参数（自动缩放）
  学习率缩放：批次4096时 ×0.0884（参考524,288）
  权重衰减：0.064965（从0.28缩放，深度8）
  AdamW 学习率缩放：×1.224745（∝ 1/√(512/768)）
  追踪器：MLflow（仅 master），实验名称 "nanochat-d8"

当前状态（截至本次快照）
  步数：4 / 5,000（0.08%）
  损失：10.392623（从步0的10.398023下降）
  验证 bpb：3.209475（步0）
  速度：55-57 tok/s
  每步时间：约72-73秒
  预计完成：5000 × 72s ≈ 98-100小时 ≈ 4.1天

遇到的问题及解决
  1. EADDRINUSE（端口29500）— 之前尝试的残留进程占用了端口。
     修复：fuser -k 29500/tcp + pkill
  2. Gloo 连接超时 — master→worker 的临时端口被 worker 防火墙阻止。Worker 没有 sudo 权限。
     修复：用户开放了防火墙。
  3. 残留孤儿进程 — 旧的后台运行留下了孤立的 base_train 进程（PPID=1）。
     修复：按 PID 执行 kill -9。
  4. 日志捕获 — script/tee 缓冲隐藏了 stderr 输出。使用 tmux capture-pane 替代。

已知限制
  - PyTorch SDPA 回退（无 flash-attn）— 不支持滑动窗口
  - 仅 CPU — 57 tok/s 对比单节点约60 tok/s（并行化增益极小）
  - Gloo 通过以太网的 all-reduce 是瓶颈，而非计算
  - Worker tmux 窗格无输出（后台进程）
  - 每个参数的 tokens 比 0.16 非常低 — 模型将欠拟合

监控
  最新步：
    ssh lzw@192.168.1.36 "tmux capture-pane -t nanochat-master -p | tail -3"
  附着 master：
    ssh -t lzw@192.168.1.36 "tmux attach -t nanochat-master"
  MLflow UI：
    http://192.168.1.36:5000
  停止训练：
    ssh lzw@192.168.1.36 "tmux kill-session -t nanochat-master"
    ssh lzw@192.168.1.36 "ssh xiaoxin@192.168.1.28 'tmux kill-session -t nanochat-worker'"