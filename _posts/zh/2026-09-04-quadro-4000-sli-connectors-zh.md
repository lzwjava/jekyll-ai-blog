---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 4000 SLI 连接器
translated: true
type: note
---

问题：Quadro 4000 顶部边缘的两个接口是什么？

答案：这些**不是显示输出接口**，而是**SLI 接口**。

在 **Quadro 4000（Fermi，GF100）** 上：

* **顶部边缘接口** → **SLI / Quadro SLI 接口**，用于连接两块专业 GPU 以进行多 GPU 工作负载。
* **后挡板** → 实际的显示输出接口：

  * **2 × DisplayPort**
  * **1 × DVI-I**

你照片中看到的接口是 **SLI 接口**，用于高速 GPU 之间的通信。它并非连接到主板 PCIe 插槽的接口。

一个有趣的细节：**Quadro 显卡使用 SLI 的方式与 GeForce 显卡不同**，尤其是在专业可视化和同步/多显示器工作流程中。

如果你需要，我还可以为你绘制 **Quadro 4000 PCB 上每个接口及主要元件的布局图**，用于 GPU 维修学习。