---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UEFI/BIOS 超越操作系统安装
translated: true
type: note
---

问题：**除了简单地安装 Windows/Linux，使用 UEFI/BIOS 还能做哪些有趣的事情？**

答案：如果你对底层系统感兴趣，**UEFI/BIOS 实际上是一个非常不错的游乐场**。当你不再把它看作是“Windows 启动前的那个屏幕”，而是把它当作硬件与操作系统之间的固件/软件边界时，乐趣就开始了。

以下是我认为确实值得尝试的项目。

### 1. 构建你自己的 UEFI 应用程序

这可能是最好的入门项目。

编写一个微小的 `.efi` 可执行文件，让它直接从 UEFI 固件中运行：

```text
开机
   ↓
UEFI 固件
   ↓
BOOTX64.EFI
   ↓
your_program.efi
   ↓
UEFI 服务
   ↓
硬件 / 文件系统 / 帧缓冲
```

可以构建的内容包括：

* 帧缓冲图形演示
* CPU 信息查看器
* PCI 设备枚举器
* 内存映射查看器
* NVMe/SATA 设备扫描器
* SMBIOS/DMI 检查器
* UEFI 变量浏览器
* 启动项管理器
* 硬件基准测试

例如：

```text
UEFI 硬件检查器

CPU
  AMD Ryzen ...
  核心数：16
  TSC：...

内存
  可用：31.7 GiB
  区域：42

PCI
  00:01.0 AMD USB
  01:00.0 NVIDIA GPU
  02:00.0 NVMe

固件
  UEFI 版本：...
  安全启动：ON
```

这能让你直接进入固件编程领域，而无需编写一整个操作系统。

---

### 2. 制作一个在 Linux/Windows 启动前运行的 GPU 基准测试

这比普通的基准测试**有趣得多**。

构建一个 UEFI `.efi` 程序，它可以：

1. 通过 PCI 发现 GPU
2. 初始化显示路径
3. 绘制帧缓冲
4. 测量 CPU/内存性能
5. 可选地通过其硬件接口与 GPU 通信
6. 显示结果

更棒的是：制作一个 **GPU 压力测试 USB**。

```text
USB
 └── EFI/
      └── BOOT/
           └── BOOTX64.EFI

启动
 ↓
GPU 检测
 ↓
VRAM / PCIe 信息
 ↓
GPU 测试
 ↓
温度 / 时钟 / 错误
 ↓
通过 / 失败
```

困难之处在于 UEFI 本身并不能神奇地为你提供一个类似 CUDA/ROCm 的 GPU API。你需要更接近 **PCIe + GPU 驱动初始化**。

这是一个非常好的“兔子洞”。

---

### 3. 编写一个 UEFI 引导加载程序

替代 GRUB/systemd-boot：

```text
UEFI
 ↓
myboot.efi
 ↓
检测 CPU
 ↓
寻找内核
 ↓
加载内核 ELF
 ↓
构建内存映射
 ↓
设置页表
 ↓
设置帧缓冲
 ↓
ExitBootServices()
 ↓
跳转到内核
```

然后你的内核可以像这样微小：

```c
void kernel_main(struct boot_info *boot)
{
    print("来自内核的问候\n");

    for (;;) {
        asm volatile("hlt");
    }
}
```

这会教你很多关于实际启动边界方面的知识。

---

### 4. 制作一个自定义的 Linux 安装程序

你可以制作自己的类 Rufus 系统：

```text
myinstaller.iso
       ↓
UEFI 启动
       ↓
微型安装程序
       ↓
检测磁盘
       ↓
分区 NVMe
       ↓
创建文件系统
       ↓
解压 Linux rootfs
       ↓
安装内核
       ↓
安装你的 EFI 加载程序
       ↓
创建 NVRAM 启动项
```

然后启动到你自己的 Linux 系统。

你可以让安装程序完全由键盘驱动：

```text
╔══════════════════════════════════╗
║        MY LINUX INSTALLER        ║
╠══════════════════════════════════╣
║                                  ║
║  NVMe0  2TB                      ║
║                                  ║
║  [1] 擦除磁盘                    ║
║  [2] 手动分区                    ║
║  [3] 安装                        ║
║                                  ║
╚══════════════════════════════════╝
```

---

### 5. 构建一个“PC 诊断操作系统”

这是最具商业实用价值的想法之一。

启动一个 USB 并且**不安装任何东西**。

相反：

```text
启动
 ↓
CPU 测试
 ↓
RAM 测试
 ↓
PCIe 枚举
 ↓
GPU 测试
 ↓
NVMe SMART
 ↓
USB 测试
 ↓
网络测试
 ↓
ACPI 检查
 ↓
UEFI 变量
 ↓
报告
```

生成：

```text
PC 诊断报告

CPU      通过
RAM      通过  32 GB
GPU      通过
PCIe     通过  x16 Gen4
NVMe     通过
USB      通过
网络     通过

结果：健康
```

这基本上就是一个迷你的**硬件测试操作系统**。

---

### 6. 探索 ACPI

这会变得非常深入。

UEFI 公开了描述机器的 ACPI 表：

```text
RSDP
 ↓
XSDT
 ├── FADT
 ├── DSDT
 ├── SSDT
 ├── MADT
 ├── MCFG
 └── ...
```

编写一个能够转储并解析它们的工具。

然后你可以探索：

* CPU 拓扑
* APIC
* PCIe 配置空间
* 电源管理
* 睡眠状态
* 热区
* 嵌入式控制器接口

Linux 已经有工具可以完成其中大部分工作，但实现你自己的解析器是一个极好的系统项目。

---

### 7. 制作你自己的 BIOS/UEFI “演示场景”

这可能真的很有趣。

直接启动到：

```text
UEFI 演示

████████████████████
█                  █
█   3D 风格演示    █
█                  █
█  CPU: 4.8 GHz    █
█  GPU: 已检测     █
█                  █
████████████████████
```

然后实现：

* 等离子效果
* 曼德勃罗集
* 光线行进
* 软件 3D
* 粒子模拟
* 音频
* 键盘输入

没有 Linux。

没有 Windows。

只有固件 → 你的 `.efi`。

---

### 8. 尝试 UEFI 变量/启动项

UEFI 维护着持久的 NVRAM 变量。

例如，概念上：

```text
Boot0000 → Windows 启动管理器
Boot0001 → Linux
Boot0002 → MyOS
```

构建：

```bash
uefi-tool list
uefi-tool inspect Boot0002
uefi-tool create MyOS ./BOOTX64.EFI
uefi-tool delete Boot0002
```

这教你固件启动管理是如何实际工作的。

**这里要小心：** 格式错误或具有破坏性的 NVRAM 操作可能会使机器难以恢复。

---

### 9. 制作一个多启动“瑞士军刀”

如果我想做一些立即可用的东西，这可能是我会构建的项目。

一个 USB：

```text
UEFI 工具包
│
├── 硬件信息
├── CPU 基准测试
├── RAM 测试
├── GPU 测试
├── PCI 检查器
├── NVMe 测试器
├── 网络测试器
├── Linux 安装程序
├── Windows 安装程序
├── 固件工具
├── 安全启动检查器
├── ACPI 浏览器
└── UEFI Shell
```

启动菜单：

```text
┌─────────────────────────────┐
│       智维 启动工具          │
├─────────────────────────────┤
│ > 硬件诊断                   │
│   CPU 基准测试               │
│   GPU 基准测试               │
│   内存测试                   │
│   PCI 浏览器                 │
│   NVMe 浏览器                │
│   Linux 安装程序             │
│   Windows 安装程序           │
│   UEFI Shell                 │
│   重启                       │
└─────────────────────────────┘
```

这本质上就是**你自己的微型预操作系统环境**。

---

### 10. 再深入一层：编写一个微内核

我建议的进阶路径是：

```text
Rufus
  ↓
UEFI 应用程序
  ↓
UEFI 硬件检查器
  ↓
UEFI 引导加载程序
  ↓
ExitBootServices()
  ↓
x86_64 内核
  ↓
分页
  ↓
中断
  ↓
APIC
  ↓
SMP
  ↓
PCI
  ↓
NVMe
  ↓
USB
  ↓
GPU
```

在那一刻，你已经不再仅仅是在“折腾 BIOS 相关的东西”了。

你正在**从固件边界开始向上构建一个操作系统**。

并且特别有趣的分界点是：

```text
                固件
                   │
            UEFI 服务
                   │
          ┌────────┴────────┐
          │                 │
      UEFI 应用         引导加载程序
                            │
                     ExitBootServices
                            │
                          内核
                            │
             ┌──────────────┼──────────────┐
             │              │              │
            CPU            PCIe           RAM
                            │
                     ┌──────┴──────┐
                    NVMe           GPU
```

如果你的目标是 **“我想找个在这个周末可以捣鼓的有趣东西”**，我会选择 **#1 → #2 → #5**：编写一个 UEFI 硬件检查器，然后把它变成一个可启动的 CPU/RAM/GPU 诊断环境。这比仅仅制作另一个 Windows 安装程序要有趣得多。
