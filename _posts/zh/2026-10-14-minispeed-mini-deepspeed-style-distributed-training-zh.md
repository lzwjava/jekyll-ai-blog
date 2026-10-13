---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Minispeed: 迷你DeepSpeed风格的分布式训练'
translated: true
type: note
---

完成。**minispeed** — 一个 mini DeepSpeed 风格的分布式训练框架 — 已实现、测试并提交（`9c2bc67`，26 个文件，约 3000 行）。

## 构建内容

```
minispeed/
├── engine.py                  DeepSpeedEngine：backward() / step() / 累积边界
├── config.py                  DeepSpeed JSON 配置解析 + 校验（fail-fast）
├── comm.py                    后端/设备选择，collective 封装（单进程 no-op）
├── flat.py                    FlatParamGroup：params → 连续的 fp32 master buffers
├── precision.py               DynamicLossScaler + inf/nan 检测
├── zero/stage_1_and_2.py      reduction、sharding、all-gather（阶段 0/1/2）
├── optim/adam.py              在 flat buffers 上执行 AdamW，state 仅存在于本 rank 的 shard
├── optim/scheduler.py         WarmupLR / WarmupDecayLR（DeepSpeed schema）
├── checkpoint.py              sharded save/load（global_stepN/ + latest pointer）
└── activation_checkpointing.py
examples/train_lm.py           小型 char-GPT，支持单 GPU 或 torchrun 运行
tests/                         36 通过，2 跳过（NCCL 需要 ≥2 GPUs）
```

## 关键特性

- **ZeRO 0/1/2**：all-reduce vs reduce-scatter 梯度，optimizer state 分片，每步 all-gather 参数；在 stage 2 下通过分区的平方和保持全局梯度范数精确
- **fp16** 搭配 fp32 master weights + 动态 loss scaling（window growth，∞/NaN → 跳过 + 减半），**bf16** 无需 scaling
- **梯度累积**、全局裁剪、`train_batch_size` 校验、warmup/decay LR
- **自动后端**：当 `world ≤ #GPUs` 时使用 NCCL，否则在 CUDA tensors 上使用 gloo（因此 `torchrun --nproc_per_node=2` 可以在这台单 GPU 机器上运行）
- DeepSpeed 风格 API：`engine, opt, _, sched = ms.initialize(model=..., config="ds_config.json")`

## 已验证

- 引擎训练轨迹**与普通 `torch.optim.AdamW` 匹配**到 1e-4；`gas=2` 累积 ≡ 一个大 batch
- 2-rank 运行（gloo/CPU 和 gloo/CUDA，fp32+fp16，stages 0/1/2）**与在 union batch 上的单进程运行匹配**；optimizer state 可证明地被分区
- fp16 GPU：强制 ∞ 梯度 → 跳过该步、权重不变、scale 减半、然后恢复
- Checkpoint 恢复能精确复现训练轨迹；错误的 `world_size` 会被拒绝

```bash
python examples/train_lm.py --dtype fp16 --zero 2            # 1 GPU: loss 83 → 2.3
torchrun --nproc_per_node=2 examples/train_lm.py --zero 2    # 2 ranks
python -m pytest tests/ -q                                   # 36 通过，2 跳过
```
