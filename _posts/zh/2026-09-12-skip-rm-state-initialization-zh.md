---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跳过RM状态初始化
translated: true
type: note
---

问题：在 NVIDIA MODS 中，`-skip_rm_state_init` 是什么意思？

答案：

`-skip_rm_state_init` 告诉 **MODS 在启动时不要初始化/重置 NVIDIA 资源管理器（RM）状态**。

概念上：

```text
正常流程：
MODS
  ↓
初始化 RM
  ↓
初始化 GPU 状态
  ↓
运行测试

-skip_rm_state_init 流程：
MODS
  ↓
跳过 RM 状态初始化
  ↓
使用 GPU 已有的/启动时的状态
  ↓
运行测试
```

### 为什么在这里使用它？

你的命令是：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

重点是这**还不是 VRAM 测试**。

`gputest.js` 被用来让 GPU 进入一个 MATS 随后能够访问的状态。`-notest` 的含义大致是：

> 初始化/枚举 GPU，但实际不执行测试。

而：

```text
-skip_rm_state_init
```

意思是：

> **不要让 MODS 执行其正常的 RM 状态初始化。**

这种用法在特定的 **iGPU 作为显示 + dGPU 作为测试对象** 的设置中很有用，因为你不想让 MODS 的正常初始化序列在 MATS 访问 dGPU 之前干扰其现有的 PCIe/GPU 状态。

因此，大致流程是：

```bash
./mods gputest.js -skip_rm_state_init -notest
#      ↑                 ↑
#      初始化             不重置/初始化 RM 状态
#      GPU 环境

./mats -n 1 -e 10
#       ↑
#       定位第二个 GPU
```

### `-skip_rm_state_init` 与 `-notest` 的区别

它们做的事情**不同**：

| 标志                    | 含义                      |
| ----------------------- | ------------------------- |
| `-skip_rm_state_init`   | 跳过 RM 状态初始化         |
| `-notest`               | 实际不运行测试             |

因此：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

大致意思是：

> **使用 `gputest.js` 准备/枚举 GPU，但不运行测试，也不执行正常的 RM 状态初始化。**

一个重要的细微差别：我**不会将 `skip_rm_state_init` 解释为“完全不初始化 GPU”**。MODS 仍然需要枚举/访问 GPU 的足够部分，以便后续的 MATS 工作流正常运行。它专门跳过了 **RM 状态初始化阶段**，而不是所有 GPU 初始化。

如果你想了解这为什么能避免 `GPU register invalid` 错误，关键点在于 **MODS → RM → GPU BAR/寄存器 → MATS** 初始化链。
