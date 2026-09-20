---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU的4GB以上PCI MMIO
translated: true
type: note
---

**问题：这个 PCI/MMIO 诊断实际上意味着什么，为什么 `pci=nocrs` / `pci=realloc=on` 会帮助 Tesla M40？**

答案：

关键概念是 **GPU 显存并未直接映射到 CPU 物理内存中**。GPU 通过 PCIe **BAR（基地址寄存器）** 暴露其显存，而 Linux 需要将该 BAR 分配到 CPU 物理地址空间中的一个范围内。

对于具有 12/24 GB 显存的 Tesla M40，一个 BAR 非常大，通常需要 **64 位 PCI MMIO 地址**，通常位于 4 GB 边界之上。

### 1. 将 PCI BAR 视为通往显存的窗口

假设 M40 具有 12 GB 显存：

```text
GPU 显存
┌──────────────────────────────┐
│                              │
│          12 GB 显存           │
│                              │
└──────────────────────────────┘
             ▲
             │ PCIe BAR
             │
CPU 物理地址空间
┌──────────────────────────────────────────────────┐
│ 0x00000000                                       │
│                                                  │
│ 内存                                            │
│                                                  │
│ 0xFFFFFFFF  = 4 GB - 1                           │
├──────────────────────────────────────────────────┤
│                                                  │
│ PCIe MMIO                                       │
│                                                  │
│       GPU BAR → M40 显存                         │
│                                                  │
└──────────────────────────────────────────────────┘
```

重要的区别是：

```text
显存大小 != VRAM 占用的 CPU 物理地址空间
```

GPU 不需要 12 GB 的常规系统内存。

它需要一个 **12 GB 可寻址的 MMIO 窗口**，通过该窗口 CPU 可以访问 GPU 的资源。

---

## 2. 为什么 `0xfeafffff` 值得怀疑

您有：

```text
PCI 主机桥窗口：

[mem 0xdf200000-0xfeafffff]
```

将其转换为大小：

```text
0xfeafffff - 0xdf200000 + 1
≈ 510 MB
```

因此，这个特定的 PCI 根桥大约有一个 **510 MB 的 MMIO 窗口**，重要的是：

```text
0xfeafffff < 0x100000000
```

其中：

```text
0x100000000 = 4 GB
```

因此，操作系统被告知：

```text
PCI 设备可以在此处使用 MMIO：

0xdf200000 ─────────────── 0xfeafffff
             ~510 MB

4 GB 以上的 PCI MMIO：

             ❌ 显然不可用
```

这就是核心问题。

---

# 3. 为什么 4 GB 很重要

PCI 历史上使用 32 位地址：

```text
0x00000000
       ...
0xffffffff
```

最大：

```text
2^32 = 4 GB
```

因此，PCI 设备可以具有如下 BAR：

```text
BAR0 = 0xd0000000
大小  = 256 MB
```

一切都适合在 4 GB 以下。

现代 GPU 则不同。

GPU 可以暴露类似这样的东西：

```text
BAR：
    大小 = 16 GB
    支持 64 位
```

您无法将其放入 32 位物理地址空间。

因此，平台需要为 PCIe 提供一个 64 位 MMIO 区域：

```text
0x100000000              4 GB
      │
      ▼
┌─────────────────────────────────────┐
│ 4 GB 以上的 PCI MMIO                 │
│                                     │
│ M40 帧缓冲 BAR                       │
│                                     │
│ 可能为多个 GB                        │
└─────────────────────────────────────┘
```

这就是为什么人们会提到：

> **4G 以上解码**

这本质上就是允许大型 PCIe BAR/MMIO 资源放置在 4 GB 物理地址边界之上的平台/PCIe 配置。

---

# 4. 令人困惑的部分：您的机器确实有 4 GB 以上的地址

这一行非常重要：

```text
0000000100000000-000000011fdfffff System RAM
```

让我们来解读：

```text
0x100000000
```

正好是：

```text
4 GB
```

而：

```text
0x11fdfffff
```

大约为：

```text
4.5 GB
```

所以您的机器在 4 GB 以上有一些物理上位于的物理内存。

大致：

```text
物理地址空间

0x000000000
     │
     │ 内存 / 设备
     │
0x0FFFFFFFF
     │
     │ 4 GB
     ▼
0x100000000
     │
     │ ~500 MB 系统内存
     │
0x11FDFFFFF
```

在具有内存重映射的机器上，这完全正常。

语句：

> “这台机器只有 4 GB 内存”

**不**意味着：

> “CPU 只能寻址 4 GB 以下的物理地址。”

这是两码事。

---

# 5. 那为什么 Linux 不能将 GPU 放在 4 GB 以上？

因为实际上涉及多个层次。

想想：

```text
CPU 物理地址空间
        │
        ▼
固件 / ACPI
        │
        ▼
PCI 主机桥
        │
        ▼
PCIe 总线
        │
        ▼
GPU BAR
```

固件描述了 PCI 主机桥允许使用哪些资源。

ACPI 通过如下方式提供这些信息：

```text
_CRS
```

当前资源设置。

内核看到大致相当于：

```text
PCI 根桥
    MMIO：
        0xdf200000 - 0xfeafffff
```

因此认为：

> “这个 PCI 层级结构有这些 MMIO 空间可用。”

内核不一定可以自由地简单说：

```text
我将把这个 PCI BAR 放在 0x200000000。
```

因为平台尚未告知它该 PCI 根复合体拥有该地址范围。

---

# 6. 这就是为什么考虑使用 `pci=nocrs`

通常，Linux 从 ACPI 获取 PCI 资源信息。

概念上：

```text
BIOS/UEFI
   │
   ├── ACPI _CRS
   │
   ▼
Linux PCI 子系统
   │
   └── “根桥拥有 0xdf200000-0xfeafffff”
```

`pci=nocrs` 告诉 Linux：

> 不要信任/使用 ACPI `_CRS` PCI 资源信息。

然后 Linux 可以使用其他信息，包括固件内存映射，来构建 PCI 资源分配。

所以实验是：

```text
正常：

ACPI _CRS
    ↓
PCI 根窗口
    ↓
0xdf200000-0xfeafffff
    ↓
M40 BAR 无法容纳


pci=nocrs：

忽略 _CRS
    ↓
以不同方式派生 PCI 资源
    ↓
可能发现可用的 64 位 MMIO
    ↓
M40 BAR 可能容纳
```

**但是 `pci=nocrs` 不会神奇地创造硬件能力。**

这是一个重要的注意事项。

如果芯片组/固件确实无法路由 4 GB 以上的 PCIe MMIO，`pci=nocrs` 将无法修复它。

---

# 7. `pci=realloc=on` 的作用

这是一个不同的机制。

假设固件分配了错误的 PCI 资源：

```text
根桥：

MMIO：
0xdf200000-0xfeafffff

GPU：

BAR：
需要 12 GB
```

显然：

```text
12 GB > 510 MB
```

Linux 可能重新分配 PCI 资源：

```text
固件分配
        │
        ▼
Linux 注意到冲突
        │
        ▼
重新分配 PCI BAR/窗口
        │
        ▼
更大的 MMIO 窗口
```

这就是 `pci=realloc` 系列选项试图启用的。

但同样：

```text
Linux 可以重新排列资源
```

不同于：

```text
硬件支持任意的 64 位 PCI MMIO
```

前者无法弥补后者。

---

# 8. `assign-busses` 是另一个层面

PCI 具有层次结构。

例如：

```text
根复合体
│
├── 总线 00
│   │
│   └── PCIe 根端口
│       │
│       └── 总线 01
│           │
│           └── Tesla M40
```

固件通常分配总线编号和资源。

如果该分配损坏，Linux 可以潜在地重新分配总线编号：

```text
pci=assign-busses
```

但从显示的信息来看，**这不是我首先怀疑的**。

您的明显失败是 MMIO 资源空间，而不一定是总线编号。

---

# 9. 真正的问题是平台是否支持 64 位 PCI MMIO

因此，层次结构是：

```text
                 ┌─────────────────────┐
                 │ BIOS/UEFI           │
                 │                     │
                 │ 4G 以上解码？        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ PCI 根复合体         │
                 │                     │
                 │ 64 位 MMIO？         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Linux PCI 子系统     │
                 │                     │
                 │ 资源分配器           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Tesla M40           │
                 │                     │
                 │ 大型 64 位 BAR       │
                 └─────────────────────┘
```

如果 BIOS 说：

```text
4G 以上的 PCI MMIO：否
```

那么：

```text
pci=nocrs
```

可能救不了您。

如果 BIOS 支持但 ACPI 错误地描述了根桥，那么：

```text
pci=nocrs
```

或：

```text
pci=realloc=on
```

可能会修复 Linux 端的分配问题。

---

# 10. 对于 M40，还有一个更重要的区别

对于 NVIDIA GPU，您应该检查实际的 BAR。

运行：

```bash
lspci -vv -s 01:00.0
```

查找：

```text
Region 0:
Region 1:
Region 2:
...
Memory at ...
```

尤其注意：

```text
Memory at <64-bit address> [size=...]
```

另外：

```bash
lspci -xxxx -s 01:00.0
```

以及：

```bash
dmesg | grep -Ei \
  '01:00|BAR|resource|MMIO|pci.*assign|no space|failed'
```

核心问题会是类似这样的消息：

```text
BAR X: no space for ...
BAR X: failed to assign ...
```

或：

```text
can't assign mem resource
```

然后我们就知道我们实际上是在处理 PCI BAR 分配问题，而不是后续的 NVIDIA 驱动问题。

---

# 11. 对引用推理的一个细微修正

这句话：

> “M40 需要 4GB 以上的 BAR 来容纳其帧缓冲（12GB 或 24GB）。”

方向正确，但稍微过于简单。

GPU **不一定** 需要在每种配置下都有一个完全等于整个物理显存容量的 BAR。

现代 NVIDIA GPU 暴露多个 BAR，确切的 BAR 布局/大小取决于设备和配置。

重要的不变量是：

```text
M40 具有大型 PCIe MMIO 资源需求
```

而您可用的 PCI 根 MMIO 窗口似乎只有：

```text
4 GB 以下约 510 MB
```

对于大内存 GPU 来说，这显然值得怀疑。

---

# 12. 我接下来会检查什么

不要立即开始随机添加内核参数。

首先确定硬件拓扑：

```bash
sudo lspci -nn
```

然后：

```bash
sudo lspci -vv -s 01:00.0
```

然后：

```bash
sudo lspci -tv
```

然后：

```bash
sudo dmesg | grep -Ei \
  'pci|BAR|resource|MMIO|above 4G|no space|failed to assign'
```

以及特别地：

```bash
cat /proc/iomem
```

最后这个特别有用，因为您会看到实际的物理地址映射：

```text
00000000-...
System RAM

...

df200000-feafffff
PCI Bus 0000:00

100000000-11fdfffff
System RAM
```

如果在 `0x100000000` 之上**没有 PCI MMIO 区域**，尽管那里存在内存，这强烈表明 PCI 层次结构没有被赋予 64 位 MMIO 窗口。

---

## 心智模型

整个问题可以归结为：

```text
                  CPU 物理地址空间

0 GB                                              4 GB
 │                                                  │
 ▼                                                  ▼
┌────────────────────────────────────────────────────┐
│                    系统内存                        │
├───────────────────────────────┬────────────────────┤
│ PCI MMIO                      │                    │
│ df200000-feafffff             │                    │
│ ~510 MB                       │                    │
└───────────────────────────────┴────────────────────┘
                                │
                                │
                                ▼
                         0x100000000
                              4 GB
                                │
                                ▼
                     ┌────────────────────┐
                     │ ~500 MB 系统内存    │
                     └────────────────────┘

                     ❌ 此处没有 PCI MMIO
```

但 M40 想要的东西在概念上像这样：

```text
0x100000000
      │
      ▼
┌──────────────────────────────────────────┐
│                                          │
│       大型 M40 PCI MMIO BAR              │
│                                          │
│       可能为多个 GB                       │
│                                          │
└──────────────────────────────────────────┘
```

所以真正的问题不是：

> **“这台机器内存超过 4 GB 吗？”**

而是：

> **“PCI 根复合体在 4 GB 以上是否有足够大的 64 位 MMIO 窗口，Linux 是否知道这一点？”**

这就是我在使用 `pci=nocrs` 之前要验证的事情。

### 参考资料

* Linux 内核 PCI 文档：[PCI support and kernel parameters](https://docs.kernel.org/PCI/?utm_source=chatgpt.com)
* Linux 内核启动参数：[PCI kernel parameters](https://docs.kernel.org/admin-guide/kernel-parameters.html?utm_source=chatgpt.com)
* `lspci` 文档：[pciutils lspci documentation](https://man7.org/linux/man-pages/man8/lspci.8.html?utm_source=chatgpt.com)
