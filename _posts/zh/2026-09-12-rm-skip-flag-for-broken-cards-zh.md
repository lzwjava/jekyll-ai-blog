---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 损坏卡片的RM跳过标记
translated: true
type: note
---

好问题——这个标志是理解MODS/MATS如何在部分损坏的显卡上工作的关键。

## “RM”的含义

**RM = 资源管理器** —— 它是NVIDIA驱动程序的核心（位于内核驱动中，负责GPU初始化：枚举GPU、建立内存映射、分配通道/FIFO、编程寄存器等）。MODS包含了RM的独立副本，通常作为启动流程的一部分加载。

## 该标志的作用

通常，`mods` 的启动序列大致如下：

```
1. 在PCIe上探查/枚举GPU
2. 运行RM状态初始化  ← 将GPU编程为工作状态
3. 加载测试脚本（gputest.js等）并运行测试
```

`-skip_rm_state_init` 告诉它**跳过步骤2**——它会检测GPU，但**不会**尝试将其带入完全初始化的“健康驱动”状态。

## 测试损坏显卡时需要它的原因

当显卡存在故障时，完整的RM初始化通常会在中途**失败**（例如，显存损坏或某个电源轨不稳定），MODS会在你采取任何操作之前报错退出。通过跳过RM初始化：

- MODS转而以**原始硬件层级**访问GPU
- MATS可以直接读写帧缓冲区，即使该显卡永远无法承受正常的驱动初始化
- 这正是你需要的——你是在诊断，而非使用显卡

这也是手册将该标志与**`-notest`**配对使用的原因：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

- `-notest` → “不实际运行任何测试，仅加载MODS并保持驻留”
- `-skip_rm_state_init` → “不尝试完全初始化显卡”

这两个标志共同使MODS充当一个**最小的引导环境**，以便之后MATS可以运行。

## 实际要点

| 命令组合 | 含义 |
|---|---|
| `./mods gputest.js -skip_rm_state_init -notest` → 显示**PASS** | 显卡至少可以在硬件层级被触及——足以让MATS测试显存 |
| 相同命令 → **失败 / 未显示PASS** | 显卡完全无法访问：核心死亡、无电源轨，或使用错误的MODS版本——此时MATS无用 |

因此，如果在你的显卡上使用`-skip_rm_state_init`的命令失败，那并非标志问题——它表明该显卡完全无法初始化（或者你对该GPU代次使用了错误的MODS版本）。