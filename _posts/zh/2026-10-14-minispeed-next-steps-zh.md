---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Minispeed后续步骤
translated: true
type: note
---

你的项目已经扎实且完整（minispeed —— 一个迷你 DeepSpeed，约 1600 行，测试通过）。以下是接下来可以考虑的方向，大致按收益排序：

## 功能工作（来自 README 自己的 ❌ 列表）

1. **ZeRO stage 3（参数分片）** —— 这是最大的一个。你已经掌握了难点部分（flat buffer、reduce-scatter/all-gather 管道、分片 checkpoint）；stage 3 增加了每次前向/后向的 param all-gather 以及分片 master 权重 checkpoint。将 `zero/stage_1_and_2.py` 自然扩展为 `zero/stage_3.py`。
2. **优化器/CPU offload** —— 在 CPU 分片上运行 AdamW，每步只将更新后的分片移回。比 stage 3 简单，并且与 stage 3 搭配良好。
3. **梯度压缩 / FP1 优化器** —— 锦上添花，价值较低。

## 健壮性 / 工程

4. **checkpoint 加载时重新分片** —— 目前恢复需要相同的 `world_size`；可以通过 all-gather 后重新分区，在 `world_size=M` 时加载 `world_size=N` 的 checkpoint。
5. **将通信与反向传播重叠** —— 将分桶 reduce-scatter 挂接到 `grad_acc.register_hook`，而不是在边界处一次性完成；README 已经指出 flat buffer 本身就是桶，因此已为此做好准备。
6. **更多测试 / CI** —— 一个 GitHub Actions 工作流（CPU/gloo 测试 + 多进程），覆盖跳过步的路径和边界情况。

## 生态系统

7. **真实模型基准测试** —— 运行一个小型 Transformer（例如 nanoGPT 规模），并生成一个 README 表格：stage 0 vs 1 vs 2 的内存与单步耗时，fp16 vs bf16。
8. **文档 / 教学** —— 将 "How it works" 部分扩展为更长的设计文档或博客式教程。

如果非要选一个：**ZeRO stage 3** —— 它补全了 README 所讲述的故事，也是用户会寻找的功能。第二选择是 **comm/bwd overlap**，因为它是一个真实的性能提升，且范围很小。

你感兴趣的方向是哪个？
