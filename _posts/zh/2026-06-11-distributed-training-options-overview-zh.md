---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式训练选项概述
translated: true
type: note
---

机器比较
==================

192.168.1.47（xiaoxin@xx）
  CPU：Intel i5-12450H，8核/12线程
  内存：16 GB
  GPU：Intel UHD Graphics（集成，无CUDA）
  Torch：2.12.0+cpu

192.168.1.36（lzw@）
  CPU：Intel i9-13900KF，24核/32线程
  内存：62 GB
  GPU：RTX 4070 12GB（支持CUDA）
  Torch：2.9.1+cu128

nanochat 已内置 DDP 支持（torchrun，NCCL 后端）。

关键限制：nanochat 的 compute_init() 使用 NCCL 后端进行 DDP，这需要 CUDA。1.47 机器完全没有 CUDA。因此，在现有代码下，这两台机器之间真正的多节点 DDP 并不直接可行。

以下是从最简单到最具学习价值的选项：

选项1：在1.36上使用单节点多进程 CPU DDP（最简单，最具学习价值）

i9-13900KF 有 24 核。你可以使用 Gloo 后端启动多个 CPU 工作进程：

bash
在 192.168.1.36 上，你需要修改 compute_init() 以在 device=cpu 时使用 Gloo
然后运行：
torchrun --nproc_per_node=4 --master_addr=127.0.0.1 --master_port=29500 \
    -m scripts.base_train --device-type=cpu --depth=4 --max-seq-len=512 \
    --device-batch-size=1 --total-batch-size=512 --num-iterations=20

但当前代码在 device_type != "cuda" 时会跳过 DDP 初始化（compute_init 中的代码行：if is_ddp_requested and device_type == "cuda"）。需要一个小补丁。

选项2：跨两台机器的多节点 CPU DDP（最具“分布式”学习特性）

需要修改 nanochat 以支持用于 CPU DDP 的 Gloo 后端，然后在两台机器上使用 rendezvous 启动 torchrun。

选项3：直接在1.36上使用单 GPU DDP 的 RTX 4070（实用）

bash
ssh lzw@192.168.1.36
cd /mnt/data/nanochat
source .venv/bin/activate
torchrun --nproc_per_node=1 -m scripts.base_train --depth=8 ...

这就是现有的 run_rtx4070.sh 已经实现的功能。
