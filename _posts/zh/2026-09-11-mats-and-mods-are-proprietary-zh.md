---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MATS和MODS是专有的
translated: true
type: note
---

问题：我们这里提到的 MATS 和 MODS 是否有开源版本？

答案：**不，MATS 和 MODS 是专有软件。**

手册中提到的 MATS（内存自动化测试系统）和 MODS（模块化诊断软件）工具集是 NVIDIA 和 AMD 开发的内部专有诊断工具，未以任何开源许可证发布。

关于这些工具的关键细节包括：

* **来源/可用性：** 这些工具是硬件供应商专有的内部工厂及维修工具，通过泄露流出。它们通常以预编译的第三方 Linux/DOS 修复磁盘镜像形式分发，而非来自官方或开源仓库。

* **使用方式：** 它们作为闭源二进制可执行文件（`./mods`、`./mats`、`./tserver`）运行，旨在对 GPU 核心和 VRAM 芯片执行直接硬件测试。