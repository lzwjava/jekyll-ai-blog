---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达Jetson TX1嵌入式AI平台
translated: true
type: note
---

问题：什么是 NVIDIA Jetson TX1（搭配底板 + 电源，运行 Ubuntu）？

答案：

**NVIDIA Jetson TX1** 是一款紧凑型高性能嵌入式计算平台，专为 AI 和计算机视觉任务而设计。以下是您的设备组成：

---

### 🧩 模块（“大脑”）

Jetson TX1 采用模块化架构——一个 **COM 模块（Computer-on-Module）**，包含 Tegra X1 SoC、4 GB LPDDR4 内存、16 GB eMMC 5.1 闪存存储、802.11ac Wi-Fi/Bluetooth 和 Gigabit Ethernet。

| 组件 | 规格 |
|---|---|
| GPU | 256核 NVIDIA Maxwell™ GPU，性能 >1 TFLOP |
| CPU | 四核 ARM Cortex-A57 MPCore（64位） |
| RAM | 4 GB LPDDR4 |
| 存储 | 16 GB eMMC 5.1 |
| 功耗 | 低于 10W |

---

### 🔌 底板（Carrier Board）— I/O 端口

COM 模块安装在底板上，底板提供以下连接器：USB 3.0 Type-A、USB 2.0 Micro-AB（恢复/主机）、HDMI、M.2 Key E、PCIe x4、Gigabit Ethernet、全尺寸 SD 卡、SATA 数据+电源、显示扩展排针和摄像头扩展排针。

还有两个 GPIO 扩展排针——一个 **40 针 2.54mm 排针**（布局与 Raspberry Pi 类似）和一个 **30 针 2.54mm 排针**，用于额外的 GPIO。

---

### ⚡ 电源（Power Supply）

底板需要 **19V DC 输入** 供电。

---

### 🐧 Ubuntu / 软件

NVIDIA 提供了一款软件开发套件（JetPack SDK），包括调试器、编译器、库和工具。该 SDK 基于 NVIDIA 的 CUDA 并行编程框架，并支持 OpenCV、OpenVX 和 VisionWorks 进行图像识别。

注意：JetPack 4.x（基于 Jetson Linux r32）是 Jetson TX1 的**最后支持版本**。TX1 模块已达到生命周期结束（EOL）。您的 Ubuntu 系统很可能是 **Ubuntu 18.04** 搭配 JetPack 4.x。

---

### 🚀 典型应用场景

小巧的体积、低功耗和强大的 GPU 处理能力使 Jetson TX1 非常适合机器人技术、实时图像和传感器数据处理、远程图像识别以及车载计算应用。

参考资料：
- [JetsonHacks – Jetson TX1 Development Kit Overview](https://jetsonhacks.com/2015/11/10/nvidia-jetson-tx1-development-kit/)
- [NVIDIA Developer – Jetson TX1 DevKit](https://developer.nvidia.com/embedded/buy/jetson-tx1-devkit)
- [Linux.com – Jetson TX1 Review](https://www.linux.com/?p=476440)