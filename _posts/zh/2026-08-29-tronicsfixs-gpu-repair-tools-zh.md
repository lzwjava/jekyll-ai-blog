---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TronicsFix的GPU维修工具
translated: true
type: note
---

问题：他使用了哪些工具？

答案：
在整个视频中，**TronicsFix** 使用了多种硬件诊断、拆解、微焊接和测试工具来评估和修复这些显卡：

### 拆解与物理检查工具

*   **螺丝刀：** 用于拆卸所有显卡上的手拧螺丝、背板、散热器和导风罩螺丝 [[00:43](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D43)， [10:45](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D645)]。
*   **检查显微镜：** 用于近距离观察 PCB 上烧毁的元件、线路以及受热变色的区域 [[03:09](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D189)， [11:18](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D678)]。

### 焊接与清洁设备

*   **热风焊台：** 用于加热并拆焊损坏的表贴元件（如爆裂的电容） [[04:09](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D249)]。
*   **助焊剂和焊锡：** 用于辅助焊锡流动，并将替换元件固定在焊盘上 [[04:13](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D253)， [04:26](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D266)]。
*   **清洁用品：** 用于在焊接前清洁烧毁/爆裂的线路区域 [[03:33](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D213)]。
*   **导热硅脂和导热垫：** 在重新组装时更换，以确保 GPU 核心和显存与散热器之间的良好热传导 [[02:35](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D155)， [04:36](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D276)， [20:51](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D1251)]。

### 诊断与测量仪器

*   **万用表：** 广泛用于测量电压轨（12V、5V、3.3V、1.8V）以及测试零欧姆电阻/电容是否对地短路 [[06:47](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D407)， [08:07](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D487)， [21:55](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D1315)]。
*   **热成像相机：** 用于在运行过程中检测板卡元件和 GPU 核心上的局部热点 [[16:13](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D973)]。

### 工作台测试设置与软件

*   **定制 PC 测试台 / 裸主板方案：** 由一台 600W 电源供电，用于工作台测试显卡启动、PCIe 信号和视频显示输出 [[06:32](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D392)， [09:24](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D564)]。
*   **Heaven Benchmark：** 基准测试软件，用于压力测试 GPU 稳定性、帧率和视觉伪影 [[01:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DSmvqqGwN8bQ%26t%3D75)]。

参考文献：

*   [我买了 7 块坏显卡试图修复——结果让我失望](http://www.youtube.com/watch?v=SmvqqGwN8bQ)