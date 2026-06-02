---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过假脱机实现高效 I/O 处理
translated: true
type: note
---

问题：What does spooling mean?

回答：

**Spooling**（全称为 **Simultaneous Peripheral Operations On-Line**）是计算机系统中用于更有效地管理输入和输出操作的一种技术。

### 计算中的主要含义（最常见用法）
Spooling 允许程序向慢速设备（如 printers、tape drives 或 disk writers）发送数据，而无需等待慢速设备完成实际工作。

而是：
- 数据被临时写入（非常快速）到快速存储（通常是磁盘）上的 **spool file** 或 **spool buffer**。
- 一个独立的 **spooler** 程序（或 print spooler）稍后从这个 spool file 读取数据，并以设备的自身速度将数据发送到实际的慢速设备。

这样：
- 原始程序可以快速完成并继续执行其他工作。
- 慢速设备保持忙碌，而不会阻塞 CPU 或用户程序。

### 经典且仍然非常常见的例子
- **Printing spooling**（大多数人知道的含义）
  当你打印文档时，它不会直接发送到 printer。它会进入 **print spooler** → 保存到磁盘 → 然后逐页缓慢发送到 printer。这就是为什么你可以打印 20 个文档并立即继续工作的原因。

- **Batch job spooling**（较旧的主机系统）
  Card readers 和 tape drives 极其缓慢 → 作业首先被 spooled 到磁盘。

### “spooling” 在其他上下文中的用法
- **Cable spooling** / **hose spooling** — 有序地将 cable、rope、hose 缠绕到鼓或 reel 上（机械/工程含义）
- **Thread spooling** — 在极低级别的 threading 讨论中偶尔使用（非常罕见）
- **Data spooling** — 有时泛指传输或处理前的任何数据 buffering

但在几乎所有计算机科学、IT 和编程上下文中 → **spooling = 通过中间磁盘存储管理慢速 I/O**。

现代术语总结：
Spooling = 将输出数据临时存储到磁盘上，以便程序无需等待慢速 peripheral device。

参考文献：

- 此通用计算概念解释无需参考文献
