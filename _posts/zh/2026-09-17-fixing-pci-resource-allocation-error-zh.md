---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决PCI资源分配错误
translated: true
type: note
---

问题: 您的 MSI Click BIOS 报告 **“PCI OUT OF RESOURCES CONDITION — 检测到 PCI 资源不足。”**

答案: 这是 **POST 期间的 PCI/PCIe 地址资源分配问题**，而非存储或内存错误。

BIOS 告知您无法为所有检测到的 PCI/PCIe 设备分配足够的 PCI 资源空间（通常是 MMIO/I/O 地址范围），因此已禁用部分设备。

### 首先：让机器启动

在此屏幕中：

1. 按下 **F10** / 进入 **保存并退出**。
2. 选择 **启动设备** 并选中您的操作系统磁盘，或者如果您未更改 BIOS 设置，选择 **放弃更改并退出**。
3. 如果 Windows/Linux 启动成功，机器可用，但一个或多个 PCI 设备可能缺失。

### 然后修复底层分配

进入 BIOS，在以下路径中查找：

**高级 → PCI 子系统设置**

查找：

```text
Above 4G Decoding
```

如果存在，设置为：

```text
Above 4G Decoding = Enabled
```

如果您拥有现代/高显存 GPU 或多个 PCIe 显卡，这一点尤为重要。它允许 PCIe MMIO 资源映射到 4 GB 物理地址边界之上。

同时检查：

```text
Re-Size BAR Support
```

如果您正在排查旧主板/GPU 组合的问题，请临时设置为：

```text
Re-Size BAR = Disabled
```

然后再次测试启动。

### 如果问题仍然存在

从物理上减少 PCIe 设备数量。

例如，临时移除：

```text
PCIe 网卡
PCIe NVMe 适配器
PCIe USB 卡
声卡
采集卡
第二块 GPU
其他 PCI/PCIe 扩展卡
```

仅保留：

```text
GPU
启动/存储设备
```

成功启动后，逐个添加回这些卡。

### 为什么会发生这种情况

PCIe 设备不仅消耗电气通道。在固件初始化期间，它们会请求地址区域，例如：

```text
BAR0 ── MMIO
BAR1 ── MMIO
BAR2 ── I/O
...
```

一块 GPU 可能请求非常大的 MMIO 区域。固件需要构建大致如下的结构：

```text
CPU 物理地址空间
│
├── RAM
├── PCI MMIO
│   ├── GPU BARs
│   ├── NVMe BARs
│   ├── NIC BARs
│   └── 其他 PCIe BARs
│
└── 其他固件保留区域
```

如果固件找不到足够的合适地址空间，就会出现您照片中的错误。

### 如果您最近更换了硬件

最有用的线索是 **在此问题出现之前发生了什么变化**。

如果您告诉我您的：

```text
CPU：
主板型号：
BIOS 版本：
GPU(s)：
PCIe 卡：
NVMe 驱动器：
```

我可以将问题缩小到具体的 BIOS 设置/资源冲突，而不需要您随机禁用设备。
