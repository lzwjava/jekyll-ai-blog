---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新Windows版
translated: true
type: note
---

问题：我应该在联想小新还是 MacBook Pro 2017 上安装 Windows？

回答：

对于 **Windows**，请使用 **联想小新**。它是更好的 Windows 机器。

比较：

|                   | 联想小新               | MacBook Pro 2017      |
| ----------------- | ---------------------- | --------------------- |
| Windows 支持      | ⭐⭐⭐⭐⭐ 原生支持        | ⭐⭐⭐⭐ Boot Camp        |
| 驱动程序          | 优秀                   | 良好但逐渐老化        |
| CPU               | 更新的 Intel/AMD       | Intel 第 7 代         |
| 电池              | 通常更好               | 电池可能已衰减        |
| SSD               | 更快的 PCIe NVMe       | PCIe SSD              |
| 内存              | 通常 16GB+             | 8/16GB                |
| GPU               | 更新的集成显卡         | Intel Iris/Radeon Pro |
| Linux 支持        | 更简单                 | 更麻烦                |
| AI/ML 开发        | 更好                   | 较差                  |
| 维修/升级         | 更容易                 | 困难                  |

## 联想小新

它基本上是为 Windows 设计的：

```
联想小新
      |
      +-- UEFI BIOS
      |
      +-- Windows 11
      |
      +-- 联想驱动程序
      |
      +-- WSL2 / Docker / CUDA GPU (如果是 NVIDIA)
```

适合：

* Visual Studio Code
* Python
* Java
* Docker
* WSL2
* AI 开发
* 日常 Windows 应用

---

## MacBook Pro 2017

这是一台不错的机器，但 Windows 不是它的“原生家园”：

```
MacBook Pro 2017

Apple EFI
   |
Boot Camp 层
   |
Windows
   |
Apple 驱动程序
```

问题：

* 较旧的 Intel CPU
* 不支持官方 Windows 11
* Boot Camp 驱动程序逐渐老化
* Touch Bar 驱动程序可能很烦人
* Apple 键盘布局不同
* 在 Windows 下散热不佳
* 如果你编译内核，可能会花时间修复硬件兼容性

它更适合作为：

```
MacBook Pro 2017
       |
       +-- Ubuntu/Linux
       |
       +-- macOS
       |
       +-- 开发机器
```

---

考虑到你的使用场景（Linux 内核编译、AI、PyTorch、LLM 实验）：

我会这样做：

```
联想小新
    |
    +-- Windows 11
    |
    +-- WSL2 Ubuntu
    |
    +-- Docker
    |
    +-- Python/PyTorch

MacBook Pro 2017
    |
    +-- Ubuntu
    |
    +-- 内核实验
    |
    +-- 轻量级编码
```

联想小新让你在硬件上遇到的麻烦更少。MacBook Pro 2017 对于学习 EFI/Linux 内部机制来说很有趣，但到 2026 年它并不是最好的 Windows 笔记本。