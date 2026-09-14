---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双头PCIe转CPU线缆
translated: true
type: note
---

问题：“双头pcie转cpu线”是什么意思？

回答：“双头pcie转cpu线”字面翻译为**双头PCIe转CPU供电线**——更具体地说，它指的是一种**PCIe电源转接线**，具有以下特点：

- **双头**——一端有两个连接器（通常是两个6针或8针PCIe插头）
- **转**——转换/适配
- **CPU线**——另一端使用CPU/EPS 12V连接器（通常用于为主板上的CPU供电的8针或4+4针连接器）

在实际使用中，这是一种**从电源的CPU/EPS 12V输出取电并转换为PCIe电源**的线缆，用于为显卡或计算卡（如Tesla P100）供电——因为P100是**数据中心卡**，没有标准的PCIe电源插头，但需要通过适配器进行外部供电。

> **补充说明：** Tesla P100是专为AI/深度学习工作负载设计的专业计算卡。它没有显示输出，也没有游戏驱动，因此很遗憾，无论其原始计算性能如何，它**都无法用于游戏**。
