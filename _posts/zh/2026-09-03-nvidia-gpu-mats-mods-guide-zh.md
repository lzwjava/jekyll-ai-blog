---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA GPU MATS MODS指南
translated: true
type: note
---

问题：**关于 Levirepair 的帖子内容是什么？它是否是您正在寻找的 MATS/MODS GPU 内存测试工具？**

回答：

是的。**这与 GPU 维修高度相关。** 该页面是一个社区维护的 **NVIDIA MATS + MODS + NVMT 工具及可启动 Linux 环境** 合集，专门用于诊断显卡。([Levirepair][1])

[Levirepair — Nvidia MATS & MODS USB stick 帖子](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com)

### 1. 三个重要工具

| 工具       | 测试内容                          | 用途                                                 |
| ---------- | --------------------------------- | ---------------------------------------------------- |
| **MATS**   | GPU **VRAM**                      | 查找有问题的 GDDR 内存                                |
| **MODS**   | GPU + VRAM / GPU 功能              | 更广泛的 GPU 硬件测试                                 |
| **NVMT**   | NVIDIA 信息/诊断                   | VBIOS、设备信息、内存相关分析                         |

作者明确表示：

> `mods` 会测试 GPU 及其内存
> `mats` 只测试 GPU 的内存。 ([Levirepair][1])

因此，思维模型如下：

```text
                    NVIDIA GPU
                       │
             ┌─────────┴─────────┐
             │                   │
          GPU 核心              VRAM
             │                   │
           MODS                 MATS
       GPU + 内存             仅内存
```

### 2. 这基本上就是您之前询问的那类工具

您之前问过，是否存在类似 **汽车诊断扫描仪** 的工具用于 NVIDIA GPU。

**MATS/MODS 是 GPU 维修领域中最接近这一概念的工具之一。**

如果原来是这样：

```text
汽车
  ↓
OBD 扫描仪
  ↓
错误代码
  ↓
有故障的子系统
```

现在变成了：

```text
GPU
 ↓
启动诊断 Linux 系统
 ↓
MATS / MODS
 ↓
内存 / GPU 测试
 ↓
错误信息
 ↓
映射错误 → VRAM 通道 / 芯片 / GPU 子系统
 ↓
物理维修
```

例如，如果您正在维修一张出现 **黑屏 / 花屏 / 驱动崩溃** 的显卡，MATS 可以告知您 VRAM 子系统是否产生错误，而不是盲目更换组件。

### 3. 最有趣的部分：它映射 VRAM 错误

该帖子包含了不同代显卡的 **内存布局示意图和映射**，包括 GDDR5/GDDR6/GDDR6X。 ([Levirepair][1])

此外，它还包含了特意用于将内存测试结果与物理内存芯片关联的信息。

这对您当前的方向极为有用：

```text
MATS 错误
    ↓
内存通道 / 地址
    ↓
物理 GDDR 芯片
    ↓
测量周边电路
    ↓
更换 VRAM / 修复走线 / 检查 GPU
```

这比单纯运行 FurMark 或 CUDA 基准测试对维修更有用。

### 4. 它可以从 USB 启动

该帖子描述的主要软件包是一个基于 Linux 的 USB 环境。

原始软件包包含：

* MATS
* MODS
* NVMT
* 多个 MODS 版本
* 脚本
* 自动保存报告
* 不同 GPU 代的环境

帖子称主镜像大约 **2.31 GB**，安装说明使用 Rufus 将其写入 U 盘。 ([Levirepair][1])

还有更新的独立环境，用于：

```text
GTX
RTX
RTX 50 系列
```

作者特别指出，RTX 50 系列需要 **UEFI 和 PCIe Gen 5** 才能使用该环境。 ([Levirepair][1])

### 5. 主 GPU 与从 GPU

这部分对于损坏的 GPU 特别有用。

如果 GPU 仍能输出视频：

```text
GPU
 │
 └── HDMI/DP → 显示器

启动 USB
   ↓
MATS/MODS
```

您可以将其作为主 GPU 进行测试。

但如果 GPU **不产生图像**，帖子描述了使用带有集成显卡的主板/CPU：

```text
CPU 集成显卡
   │
   └── 显示器

损坏的 NVIDIA GPU
   │
   └── PCIe x16

        ↓

启动 MATS/MODS

        ↓

modsinit
        ↓
MATS/MODS 测试从 GPU
```

说明中明确给出了：

```bash
modsinit
mods
```

用于 MODS，以及：

```bash
modsinit
mats -n 1
```

用于在从 GPU 上运行 MATS。 ([Levirepair][1])

**这对您的维修实验非常实用。**

### 6. 甚至还有 VRAM 温度实验

该帖子给出了这个 MODS 命令：

```bash
./mods gputest.js -test 13 \
    -run_on_error \
    -bg_dram_temp 1000
```

其目的是测试/记录 VRAM 温度，并帮助识别有问题的内存芯片。 ([Levirepair][1])

这是一个有趣的维修流程：

```text
运行内存/GPU 测试
       ↓
出现错误
       ↓
观察 DRAM 温度
       ↓
识别可疑的 VRAM
       ↓
对该芯片进行电气检查
       ↓
更换/重新植球等
       ↓
重新运行 MATS
```

### 7. 还有通道禁用功能

该帖子包含了 MODS 的 `floorsweep` 信息，用于禁用特定的 FBIO/FBP 通道。

例如：

```text
A = 0x01
B = 0x02
C = 0x04
D = 0x08
E = 0x16
F = 0x32
```

并解释了如何组合掩码来禁用多个通道。 ([Levirepair][1])

这属于 **高级 GPU 维修领域**：您不再只是问“VRAM 工作正常吗？”，而是通过实验 GPU 的内存拓扑来隔离有缺陷的内存通道。

---

## 对于您学习维修 4090/4070 的建议

我会将这个网站列为非常重要的资源。

您最终的维修流程可能如下所示：

```text
              ┌──────────────────┐
              │ 损坏/故障的 GPU   │
              └────────┬─────────┘
                       │
              目视检查
                       │
              电阻/二极管测量
                       │
              电源轨
                       │
              PCIe / 辅助供电
                       │
              ┌────────▼────────┐
              │ GPU 是否 POST？  │
              └───────┬─────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
         是                      否
          │                       │
       MATS/MODS             电气诊断
          │                       │
          │                   电源/BIOS/
      VRAM 错误？              GPU 核心等
          │                       │
          ↓
    映射内存通道
          ↓
    确定物理
       GDDR 芯片
          ↓
    维修/更换
          ↓
     再次运行 MATS
```

**因此，MATS/MODS 应该是您最早学习的软件工具之一**，与万用表、示波器、板图/原理图以及最终需要的编程器/返修设备同等重要。

一个重要注意事项：该帖子是一个 **社区分发版**，并非 NVIDIA 支持的诊断产品。该页面还引导用户从社区来源获取某些 MODS 版本。 ([Levirepair][1]) 因此，请将下载的镜像/工具视为不可信软件：在提供哈希值的情况下验证哈希，使用专用测试机器，并且不要在启动环境中放置敏感数据。

该页面为其主镜像提供了一个 MD5 哈希值：

```text
3cc2ce1e4b9836548a8fad6479a2c4c3
```

以及 CRC32：

```text
15B10F3F
```

([Levirepair][1])

对于 **您当前的 GPU 维修设置**，接下来要学习的是 **MATS 如何将诸如 `FBIO / 通道 / 地址` 这样的错误转化为“板上的这个物理 GDDR6(X) 芯片可能坏了”**。这正是将 MATS 从基准测试转变为维修诊断工具的关键部分。

[1]: https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3 "Nvidia MATS & MODS USB stick (with NVMT): Forum - Levirepair"