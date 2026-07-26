---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在2017款MacBook Pro上安装Windows
translated: true
type: note
---

问题：2017款MacBook Pro可以安装Windows吗？

答案：

可以。**2017款MacBook Pro可以安装Windows**，官方通过 **Boot Camp助理**（双系统）实现，或者非官方通过虚拟机实现。

2017款MacBook Pro是 **Intel Mac**，因此由于CPU为x86-64架构，Windows可以原生运行。

## 方案一：Boot Camp（原生Windows）

这是性能最佳的选择。

架构：

```
MacBook Pro 2017
        |
        +-- macOS
        |
        +-- Windows 10
             |
             +-- Intel CPU
             +-- Radeon Pro GPU
             +-- SSD
```

重启后选择：

```
macOS
   或
Windows
```

要求：

* macOS High Sierra 或更新版本
* Windows 10 64位 ISO
* 至少约64GB可用磁盘空间（建议128GB以上）
* 根据机型/macOS版本可能需要U盘

步骤：

1. 下载Windows ISO：

[下载Windows 10 ISO](https://www.microsoft.com/software-download/windows10ISO?utm_source=chatgpt.com)

2. 打开：

```
应用程序
 → 实用工具
 → Boot Camp助理
```

3. 勾选：

```
创建Windows安装盘
安装Windows
下载Windows支持软件
```

4. 选择分区大小：

示例：

```
macOS     300GB
Windows   200GB
```

5. 安装Windows。

Windows启动后：

运行：

```
BootCamp\Setup.exe
```

这会安装：

* Apple键盘驱动
* 触控板驱动
* WiFi驱动
* GPU驱动
* Thunderbolt驱动

---

## 方案二：虚拟机

在macOS内运行Windows：

示例：

* Parallels
* VMware Fusion
* VirtualBox

架构：

```
macOS
 |
 +-- 虚拟机
       |
       +-- Windows
```

优点：

* 无需重启
* 系统间可复制粘贴
* 适合开发

缺点：

* GPU性能较差
* 占用macOS的RAM/CPU

对于2017款MacBook Pro：

* 16GB RAM → 可行
* 8GB RAM → 可行但较紧张

---

## Windows 11？

官方支持：

* Windows 10：Boot Camp支持
* Windows 11：官方不支持

原因：

Apple Intel Mac缺少：

* TPM 2.0
* 安全启动要求

但可以通过绕过方法安装Windows 11。

---

## 性能

典型的2017款MacBook Pro：

```
CPU:
Intel Core i5/i7
      ↓
Windows性能良好

GPU:
Intel Iris Plus
或
Radeon Pro 555/560
      ↓
轻量游戏/GPU工作尚可

RAM:
8GB/16GB
      ↓
主要瓶颈
```

对于编程：

```
Windows + VS Code
Windows + Docker
Windows + Java/Python
```

运行良好。

对于AI/ML：

```
MacBook Pro 2017 GPU
≈ 对CUDA无帮助
```

因为NVIDIA CUDA不可用，且AMD/Intel GPU的ML生态支持有限。

---

所以答案是：**2017款MacBook Pro是最后一代可以轻松实现Windows双启动的MacBook之一。** 安装Boot Camp后，它实际上是一款不错的Windows小型笔记本，尤其是因为它仍然具备Intel CPU兼容性。