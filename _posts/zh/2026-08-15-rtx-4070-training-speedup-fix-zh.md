---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070训练加速修复
translated: true
type: note
---

## 摘要

**速度缓慢的原因**——"没有足够的SM单元来使用max_autotune_gemm模式"这条警告并非表面问题。Inductor的`is_big_gpu()`检查要求至少68个SM单元（RTX 3080级别）；而RTX 4070只有46个，因此inductor会**静默跳过每次矩阵乘法的高效Triton GEMM模板**，转而使用通用的归约内核。再加上没有使用cudagraphs和极小的微批次（4），最终得到28.9K tok/s / 47 TFLOPS（仅达到RTX 4070 bf16峰值性能的28.7%，与nanoGPT参考的A100相比仅14.7%），总运行时间约26小时。

**已应用的修复**（位于`/mnt/data/nanoGPT`目录下）：
1. `train.py` — 在`torch.compile`之前强制将`is_big_gpu`设为True，以启用Triton GEMM模板；新增了`compile_mode`配置开关。
2. `config/train_bilingual.py` — 设置`compile_mode = 'reduce-overhead'`（启用cudagraphs，每次迭代减少约1.3万次内核启动）。同时保留了`batch_size=8` + `grad_accum=64`的注释选项（同样524K tok/iter，但GEMM更大——显存约有3.5GB余量）。

**应用方式**（正在运行的进程不会同步文件改动——当前仅运行至约45/5000轮次，重启会损失约15分钟进度）：
```
# 在tmux会话1中：按Ctrl-C，然后执行
cd /mnt/data/nanoGPT && python3.12 train.py config/train_bilingual.py
```
预期：第0次迭代会更慢（几分钟的内核重新编译+模板自动调优+cudagraph捕获），之后稳定状态应从约19秒降至约11-14秒/次迭代（1.3-1.8倍提速）。inductor内核缓存会记住新内核，便于后续重启时直接使用。

需要我现在在tmux中重新启动运行，并观察前几次迭代以验证加速效果吗？