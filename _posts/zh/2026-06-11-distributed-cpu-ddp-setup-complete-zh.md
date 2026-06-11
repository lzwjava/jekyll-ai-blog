---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式CPU DDP设置完成
translated: true
type: note
---

最终设置总结
===================

数据：两台机器上各有 201 个 parquet 分片（共 18GB）
  1.36：~/.cache/nanochat/base_data_climbmix/（201 个文件）
  1.47：~/.cache/nanochat/base_data_climbmix/（201 个文件，已通过 rsync 同步）

启动脚本：
  1.36：/mnt/data/nanochat/run_dist_cpu_master.sh
  1.47：~/projects/nanochat/run_dist_cpu_worker.sh

运行方式：
  终端 1（主节点）：bash /mnt/data/nanochat/run_dist_cpu_master.sh
  终端 2（工作节点）：bash ~/projects/nanochat/run_dist_cpu_worker.sh

防火墙：ufw allow from 192.168.1.0/24（已应用）

环境变量（在脚本中）：
  NANOCHAT_FORCE_SDPA=1    — FA 仅支持 CUDA
  NANOCHAT_DTYPE=float32   — bf16 会自动从 GPU 检测，在 CPU 上运行缓慢
  GLOO_SOCKET_IFNAME=...   — 绑定到局域网接口

代码补丁（4 个文件）：
  common.py      — 用于 CPU DDP 的 Gloo 后端
  flash_attention.py — NANOCHAT_FORCE_SDPA 环境变量
  optim.py       — 用于 Gloo get_future() 兼容性的 _AsyncWorkWrapper
  dataset.py     — NANOCHAT_DATA_DIR 环境变量

两台机器现在拥有完全相同的完整数据集、相同的代码和可直接运行的脚本。多节点 CPU DDP 流水线已完全正常运行——Gloo 已连接，梯度已同步，检查点已保存。