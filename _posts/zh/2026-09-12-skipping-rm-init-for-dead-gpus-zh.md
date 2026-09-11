---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跳过失效GPU的RM初始化
translated: true
type: note
---

问题：**`-skip_rm_state_init` 在 MODS/MATS 中到底做了什么？为什么它对测试一块部分损坏的 NVIDIA GPU 很有用？**

答案：

关键思路是：

> **`-skip_rm_state_init` 并不会神奇地让 GPU 正常工作。它只是让 MODS 跳过 GPU 初始化中一个在损坏显卡上可能失败的特定阶段。**

可以把 MODS 理解为位于 Linux 和 GPU 之间：

```text
Linux
  │
  ▼
MODS
  │
  ├── PCIe access
  ├── MMIO/register access
  ├── NVIDIA RM initialization
  │
  ▼
GPU
  ├── GPU core
  ├── VRAM controller
  └── VRAM chips
```

### 1. 什么是 RM？

**RM = Resource Manager**，是 NVIDIA 的底层 GPU 管理层。

从概念上讲，RM 负责把 GPU 从：

```text
PCIe device detected
        ↓
"GPU exists"
```

变成：

```text
GPU initialized
        ↓
memory controller configured
        ↓
GPU engines initialized
        ↓
channels / memory mappings / resources available
        ↓
GPU usable by higher-level software
```

因此，正常的初始化路径大致是：

```text
PCIe enumeration
      ↓
identify GPU
      ↓
RM state initialization
      ↓
initialize GPU subsystems
      ↓
run tests
```

一个重要区别是：**PCIe 检测到设备，远比 GPU 成功初始化要“弱”**。

一块损坏的 RTX 3060 仍然可能显示为：

```text
NVIDIA GPU detected on PCIe
```

但在后续初始化过程中失败。

---

### 2. `-skip_rm_state_init` 改变了什么？

不加这个标志时：

```bash
./mods gputest.js
```

MODS 会尝试初始化 RM 状态。

加上：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

你实际上是在告诉 MODS：

```text
"Don't perform that RM state initialization step.
Load MODS and leave the GPU in the minimally initialized state
needed for the subsequent test workflow."
```

所以：

```text
Normal:

PCIe
 ↓
RM init
 ↓
GPU initialized
 ↓
tests


Skip RM state init:

PCIe
 ↓
[SKIP RM state initialization]
 ↓
MODS remains available
 ↓
MATS
 ↓
VRAM testing
```

这就是为什么这一组合对 **VRAM 维修诊断** 很有用。

---

### 3. 一个微妙但重要的点

我想对之前的解释稍作修正：

> `-skip_rm_state_init` 并 **不** 意味着“MODS 获得了不受限制的原始硬件访问权限”。

MODS 本来就具备底层硬件访问机制。

你其实是在避开一条要求 GPU 更多部分保持健康的初始化路径。

这个区别很重要。

例如，假设一块 RTX 3060 存在以下情况：

```text
GPU core       OK
PCIe           OK
VRAM controller OK
M0/M1/M2/M3... missing/damaged VRAM
```

正常的初始化可能会遇到损坏的显存配置并失败。

但对于 MATS，你可能只需要 GPU/显存子系统中足够完成以下操作的部分：

```text
write VRAM
   ↓
read VRAM
   ↓
compare
```

因此：

```text
Full GPU initialization
        ↓
       FAIL
```

并不一定意味着：

```text
VRAM testing impossible
```

这正是这个变通方法的意义所在。

---

### 4. 为什么 `-notest` 会和它一起使用

这两个标志解决的是 **不同的问题**：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

`-skip_rm_state_init`：

```text
Don't perform RM state initialization.
```

`-notest`：

```text
Don't immediately execute the gputest test sequence.
```

所以从概念上讲：

```text
                 MODS startup
                     │
          ┌──────────┴──────────┐
          │                     │
  skip_rm_state_init          notest
          │                     │
  skip RM state init       don't run tests
          │                     │
          └──────────┬──────────┘
                     ↓
             MODS stays loaded
                     ↓
                  MATS
```

这也就是为什么这条命令更像是一个 **引导/设置命令**，而不是真正的 VRAM 测试。

---

### 5. 然后 MATS 才做真正关键的部分

一旦 MODS 成功驻留：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

并且你得到预期的成功启动，就可以运行 MATS。

对于你的维修流程来说，MATS 更有意义，因为它能暴露出 **哪一颗 VRAM 颗粒/哪一段地址区域有问题**。

从概念上讲：

```text
GPU
 │
 ├── VRAM M0 ─── OK
 ├── VRAM M1 ─── OK
 ├── VRAM M2 ─── FAIL
 ├── VRAM M3 ─── OK
 ├── VRAM M4 ─── OK
 └── VRAM M5 ─── OK
```

于是，你不再只是知道：

```text
"RTX 3060 crashes"
```

而是能更接近：

```text
"Memory device M2 is failing"
```

这为板卡维修提供了可操作的信息。

---

### 6. 把它看作一个诊断阶梯

对于你的 GPU 维修工作，我会把整个过程看成这样：

```text
             Does the machine POST?
                       │
                       ▼
             Is the GPU visible on PCIe?
                       │
                       ▼
       Can MODS bootstrap with skip-RM?
                       │
                       ▼
             Can MATS access VRAM?
                       │
                       ▼
          Which memory device fails?
                       │
                       ▼
       Inspect VRAM / power / signals
                       │
                       ▼
              Replace / reball
                       │
                       ▼
                  Test again
```

每一层都会告诉你不同的信息。

所以，如果：

```bash
./mods gputest.js -skip_rm_state_init -notest
```

失败，**不要立刻断定“GPU 核心坏了”**。

可能的原因包括：

```text
wrong MODS/MATS version
       │
       ├── wrong GPU generation support
       ├── incorrect command/environment
       ├── PCIe communication problem
       ├── GPU power problem
       ├── GPU core problem
       └── sufficiently severe memory/controller problem
```

因此，这条命令是一个 **有用的诊断分界线**，而不是一个二元的“GPU 活着/死了”测试。

对于你的 RTX 3060 VRAM 维修工作，我接下来可以梳理 **M0–M7 物理 GDDR6 颗粒 → 显存通道/地址映射 → MATS 报错如何指向具体某一颗颗粒**，这大概是最有用的下一步。