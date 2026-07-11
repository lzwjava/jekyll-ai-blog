---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI SATA端口命名指南
translated: true
type: note
---

**问题：** 照片中的两个SATA端口组是否标记为 `SATA_A1/A2` 和 `SATA5/6（可选）`？

**回答：**

是的，这符合微星迫击炮系列主板上标准的SATA命名惯例。以下是这些名称的实际含义：

- **`SATA_A1` / `SATA_A2`** —— 这些端口直接来自芯片组（或某些AM5主板上的CPU集成SATA控制器）。后缀 `_A` 是微星用于分组共享同一控制器通道的端口的方式。这些端口始终开启，提供全带宽的SATA 6Gb/s。

- **`SATA5` / `SATA6`（可选）** —— “（可选）”标签是关键部分。在微星主板上，这几乎总是意味着这些端口 **与某个M.2插槽共享PCIe通道**，通常是一个M.2 SATA模式插槽或共享交换器。如果你在该M.2插槽中安装了NVMe/SATA固态硬盘，`SATA5`/`SATA6` 会自动禁用——这与在其他类似微星主板上观察到的模式完全一致，在这些主板上，某些SATA端口由独立的ASMedia控制器而非主芯片组控制，并且官方文档明确说明了哪些端口在哪种配置下工作。

对你装机时的实际影响：如果你计划使用所有SATA硬盘，**在安装M.2固态硬盘之前，请查阅主板手册，确认具体哪个M.2插槽会禁用SATA5/6**——这一点经常让人困扰，包括在X570/B650主板上，手册并不总是明确说明M.2与SATA之间的冲突，直到微星后来澄清了措辞。

如果你告诉我具体型号（根据散热片设计，看起来可能是B650M/B850M Mortar），我可以调取对应手册，确认你的主板上哪个M.2插槽与SATA5/6共享通道。

参考来源：

- [配置RAID时被禁用的SATA端口 - 微星X570（Tom's Hardware）](https://forums.tomshardware.com/threads/disabled-sata-ports-when-configuring-raid-msi-x570.3657256/)