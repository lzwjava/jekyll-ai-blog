---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解AMI BIOS/UEFI固件
translated: true
type: note
---

问题：什么是 **American Megatrends (AMI) BIOS**？

答案：

**American Megatrends (AMI)** 是一家开发 **BIOS/UEFI 固件** 的公司，主板制造商使用这些固件。你可以把 AMI 视为提供固件平台的公司，而 ASUS、Huanan、MSI、Gigabyte 等则根据各自的主板进行配置/定制。

### 1. BIOS 的实际作用

当你按下电源按钮时：

```text
Power ON
   ↓
CPU starts executing firmware
   ↓
AMI BIOS / UEFI
   ↓
POST
(Power-On Self Test)
   ↓
Initialize CPU / RAM / chipset / PCIe / USB / storage
   ↓
Find boot device
   ↓
Windows / Linux bootloader
```

因此，BIOS 是开机后 **CPU 上运行的第一个软件**。

### 2. AMI BIOS 与 UEFI

从历史上看：

```text
BIOS
 └── legacy firmware interface

UEFI
 └── modern replacement for traditional BIOS
```

人们仍然习惯将整个东西称为“BIOS”，即使固件实际上是 UEFI。

现代 AMI 固件通常是 **AMI UEFI**，一般基于 **AMI Aptio**。

在 POST 过程中，你常常会看到类似这样的信息：

```text
American Megatrends
AMIBIOS
Aptio
UEFI
```

### 3. 你可以配置的内容

BIOS/UEFI 本质上是主板的硬件配置层。

例如：

```text
CPU
 ├── CPU 设置
 ├── 电源管理
 └── 虚拟化

RAM
 ├── 频率
 ├── 时序
 └── XMP（如果支持）

PCIe
 ├── PCIe 版本
 ├── 主显示器
 └── PCIe 设备

存储
 ├── SATA
 ├── NVMe
 └── 启动配置

启动
 ├── UEFI / Legacy
 ├── CSM
 └── 启动顺序

安全
 ├── Secure Boot
 └── TPM
```

对于你的 **Huanan B75**，AMI 固件在测试不同 CPU、RAM、PCIe GPU、SATA 驱动器等时尤其有用。

### 4. AMI 蜂鸣/错误代码

AMI 固件还可以通过 **蜂鸣代码** 或主板诊断指示灯报告 POST 故障。

概念上：

```text
Power ON
   ↓
POST
   ├── CPU OK
   ├── RAM OK
   ├── GPU/display initialization
   ├── chipset OK
   └── boot device
```

如果系统无法显示 BIOS 之前出现故障，你可能会遇到：

```text
beep
LED diagnostic code
no display
automatic reboot
```

这就是为什么 BIOS/POST 知识对于 **GPU 和主板维修** 非常有用：你可以区分电源/POST 路径中的问题与稍后在 Windows/Linux 中出现的问题。

**一个重要区别：** AMI 不是主板。你的 Huanan B75 是主板；**AMI 提供主板使用的固件技术**。