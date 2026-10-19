---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jetson Nano与Orin NX规格及用途对比
translated: true
type: note
---

**问题：** Jetson Nano/NX 的硬件规格是什么，它能用来做什么？

---

**回答：**

先快速说明一下：“Jetson Nano NX”并不是单一产品——NVIDIA 有两条独立但相关的产品线。以下是各自的具体情况：

---

### 🔷 Jetson Nano（入门级，上一代）

Jetson Nano 采用 **128 核 Maxwell GPU** 和 **四核 ARM Cortex-A57 @ 1.43 GHz CPU**，配备 **4 GB LPDDR4** 内存。其算力约为 0.5 TFLOPS，功耗为 **5–10W**——非常适合学习和轻量级 AI 任务。

---

### 🔶 Jetson Orin NX（当前一代“NX”）

这是现代的继任产品，提供 **8 GB** 和 **16 GB** 两种版本：

| 规格 | Orin NX 8GB | Orin NX 16GB |
| ------ | ------------- | -------------- |
| AI 性能 | 70 TOPS（超级模式下 117） | 100 TOPS（超级模式下 157） |
| GPU | 1024 核 NVIDIA Ampere + 32 个 Tensor Core | 相同 |
| CPU | 6 核 ARM Cortex-A78AE v8.2 64 位 | 8 核 ARM Cortex-A78AE |
| 内存 | 8 GB 128 位 LPDDR5 | 16 GB LPDDR5 |
| 功耗 | 10W–20W | 10W–25W |
| PCIe | Gen4 | Gen4 |
| 视频解码 | 最高 8K30（H.265） | 相同 |

Orin NX 模块可通过**软件升级提升至 SUPER 模式**，性能最高提升 70%——无需更换硬件。

它还支持最多 **4 路相机**（通过虚拟通道最多 8 路），配备 8 通道 MIPI CSI-2 D-PHY 2.1，视频编码最高支持 **4K60（H.265）**。

---

### 🛠 它能用来做什么？

Orin NX 非常适合**机器人、无人机、工业 AI 和多传感器视觉系统**。

实际部署场景包括**配送无人机、巡检无人机、农业测绘和 GPS 拒止环境下的自主导航（VSLAM）**，以及用于仓储、物流、导航、障碍物检测和库存管理的**自主移动机器人（AMR）**。

其紧凑的尺寸和可配置的功耗使其非常适合**零售、制造和物流**环境中的分布式工作负载。

它支持复杂的 AI 模型，用于**语言理解、3D 感知和多传感器融合**等任务，并由 NVIDIA 完整的软件栈提供支持，包括 **Isaac**（机器人）、**DeepStream**（视觉 AI）和 **Riva**（对话式 AI）。

---

**简而言之：** Jetson Nano = 预算型/学习型边缘 AI。Jetson Orin NX = 严肃的生产级边缘 AI，在手掌大小的模块中提供超级计算机级别的性能。

---

**参考链接：**

- [NVIDIA Jetson 模块 – 官方](https://developer.nvidia.com/embedded/jetson-modules)
- [Jetson Orin NX 评测 – ThinkRobotics](https://thinkrobotics.com/blogs/product-reviews-buying-guides/nvidia-jetson-orin-nx-module-review-specs-use-cases-price-and-how-it-compares)
- [Jetson Orin NX 8GB 模块 – ConnectTech](https://connecttech.com/?p=17661)
- [Supermicro Jetson Orin NX 边缘系统](https://www.supermicro.com/en/products/nvidia-jetson)
