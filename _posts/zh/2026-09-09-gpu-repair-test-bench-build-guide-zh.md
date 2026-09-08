---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU维修测试台搭建指南
translated: true
type: note
---

## 问题

手册推荐 ASUS B85/H170/B150，但该推荐大约在 2021 年修订过。**如今，对于专用的 GPU 维修/测试平台**，我会推荐什么？

## 答案

是的——我**不会盲目围绕 B85 搭建今天的平台**。

手册中的重点其实不是“B85”。真正的需求是：

1. **Legacy/CSM 启动**
2. **集成显卡**
3. **核显 + 独显同时工作**
4. **足够的内存**
5. **可靠的 PCIe 插槽**
6. 便宜、可替换的硬件

手册明确说明，核显的目的是在测试一块**无显示输出**的独显时，将显示器连接到主板上，并在 BIOS 中选择 CPU 显卡。

### 我在 2026 年搭建的方案

我会选择**两个时代**的硬件，而不是试图找到一块“完美”的老款 ASUS 主板。

| 平台                    | 我的评分 | 原因                                                         |
| ----------------------- | -------: | ------------------------------------------------------------ |
| **B85 + i5-4460**       |    ⭐⭐⭐⭐ | 极其便宜，经过你的手册验证                                   |
| **B150/H170 + i5-6500** |   ⭐⭐⭐⭐⭐ | 可能是我最喜欢的廉价旧款测试平台                             |
| **B250 + i5-7500**      |   ⭐⭐⭐⭐⭐ | 更新、便宜、兼容性好                                         |
| **H310/B360 + i5-8500** |    ⭐⭐⭐⭐ | 更新，但 legacy/CSM 行为变得更多依赖主板                     |
| **B550 + Ryzen APU**    |     ⭐⭐⭐ | 现代，但不适合旧的 DOS/MATS 工作流程                         |
| **X99 + Xeon E5**       |     ⭐⭐⭐ | 功能强大，但缺少核显工作流                                   |

**我的首选：B150/H170 + i5-6500/6600 + 16 GB DDR4。**

为什么？

手册本身将 **B85、B150 和 H170** 列为已验证稳定的主板。

但 B150/H170 提供了一个比 B85 好得多的折中选择：

* DDR4
* Skylake
* i5-6500 二手极其便宜
* Intel HD 530
* PCIe x16
* SATA
* UEFI + legacy 兼容性
* 比 Haswell 新得多
* 仍然足够老旧/简单，适用于奇怪的 GPU 维修软件

### 我会使用的架构

大致如下：

```text
             ┌─────────────────────┐
             │   i5-6500           │
             │   Intel HD 530      │
             └──────────┬──────────┘
                        │
                   motherboard
                        │
              ┌─────────┴─────────┐
              │                   │
          iGPU output          PCIe x16
              │                   │
           Monitor             GPU under test
                                  │
                            RTX 3090 / 4090
                            RX 580 / 6800
                            etc.
```

这比单纯拥有一颗强大的 CPU 对维修更有用。

如果 GPU 完全死掉：

```text
GPU under test
      │
      ├── PCIe power
      ├── PCIe slot
      │
      X── no video output

Motherboard iGPU
      │
      └── Monitor
```

你仍然可以启动 Linux 并针对 PCIe GPU 运行诊断程序。

这正是手册中描述的工作流程。

---

## 我会对手册做出的一项更改

我**不会特意使用 250 GB 的 SSD**。

手册建议 250 GB 以上并推荐 SATA SSD，主要是因为它的镜像被分成多个 MBR 分区。

如今我会直接使用：

```text
120 GB / 240 GB SATA SSD
        +
USB 闪存盘
        +
独立的现代 Linux SSD（如果需要）
```

存储不是瓶颈。

**真正的瓶颈是与旧的 MATS/MODS 环境的兼容性**。

---

# 更重要的是：不要把它作为你唯一的测试机器

对于你的 GPU 维修工作，我实际上会搭建一个**双机实验室**。

### 工作台 A —— legacy 诊断机器

```text
B150/H170
i5-6500
16 GB DDR4
120/240 GB SATA SSD
Intel iGPU
PCIe x16
```

用途：

```text
MATS/MODS
旧版 NVIDIA
旧版 AMD
无显示输出的 GPU
VRAM 诊断
BIOS/固件操作
```

手册中的 MATS 工作流程专门用于识别 VRAM 故障，甚至可以将错误通道映射到物理内存芯片。

### 工作台 B —— 现代 GPU 测试机器

你的新机器：

```text
现代 CPU
RTX 4070 或任意现代 GPU
64 GB+ RAM
NVMe
现代 UEFI
```

用途：

```text
RTX 30 系列
RTX 40 系列
RTX 50 系列
现代 AMD 显卡
GPU-Z
CUDA
Linux
Windows
压力测试
vBIOS 工具
驱动测试
```

这种区分很重要，因为**旧的 MATS/MODS 环境与现代 GPU 验证环境不是一回事**。

---

# 这个手册还有一个更大的问题

手册本身提到：

> N 卡：RTX 3090 及以下

而它的 AMD 文档涵盖的是 RX 6000/RX 5000 时代的硬件。

所以我应该把它当作一本**旧款维修手册**，而不是一套完整的 2026 年 GPU 测试方法论。

例如：

```text
GTX 1080
RTX 2080
RTX 3090
RX 580
RX 5700
RX 6900
        ↓
非常适合使用本手册的场景
```

但：

```text
RTX 4090
RTX 4080
RTX 5090
RTX PRO 6000 Blackwell
RX 7900 XTX
更新的 Blackwell GPU
        ↓
不要认为此镜像中的 MATS/MODS 足够用
```

你还需要一套现代的诊断工具。

---

## 我对你的实际推荐

考虑到你正在购买廉价二手硬件专门用于 **GPU 维修**，我会在闲鱼上寻找：

```text
ASUS B150 / H170
        +
i5-6500 / i5-6600
        +
16 GB DDR4
```

如果其他可靠的 B150/H170 主板具备：

```text
Intel iGPU
PCIe x16
CSM/Legacy 支持
```

则不必为 ASUS 品牌支付溢价。

但 **对于这个特定手册，ASUS 仍然是非常好的选择**，因为作者明确验证了 ASUS B85/B150/H170，而不仅仅是理论上推荐芯片组。

### 二手市场价格目标

我大致估算：

```text
B150/H170 主板     ¥80–150
i5-6500            ¥30–60
16 GB DDR4         ¥50–80
240 GB SATA SSD    ¥30–50
廉价电源           ¥50–100
机箱               可选

总计              ~¥240–440
```

在这个价位上，**我绝对会搭建它**。

同时保留你的 X99 机器。不要替换它。

理想的维修台就变成了：

```text
                 GPU REPAIR LAB
                       │
             ┌─────────┴─────────┐
             │                   │
       Legacy bench         Modern bench
       B150/H170            X99 / newer
       i5-6500              powerful CPU
       Intel iGPU           modern GPU
             │                   │
       MATS/MODS              modern tests
       dead GPU              stress/driver
       VRAM diagnosis        CUDA/GPU-Z
```

**这样要比仅仅因为手册说 B85 就去买一块 B85 强大得多。**