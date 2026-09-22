---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU BIOS芯片引脚功能
translated: true
type: note
---

**问题：** GPU 上的 8 针 BIOS 芯片是什么，每个引脚有什么作用？

**回答：**

GPU 上的 8 针 BIOS 芯片是一种 **SPI NOR Flash 存储器** IC（常见型号：Winbond W25Q128、MX25L 系列）。它存储 GPU 的固件——即 VBIOS——GPU 在加电时会读取该固件来自我初始化。该芯片使用 **SPI（串行外设接口）** 协议，并采用微小的 SOIC-8 封装。

以下是每个引脚的作用：

| 引脚 | 名称 | 功能 |
| ----- | ------ | ---------- |
| 1 | CS# | 片选——拉低以激活芯片 |
| 2 | DO (MISO) | 数据输出——将数据发送到 GPU |
| 3 | WP# | 写保护——拉低时，阻止任何写入操作 |
| 4 | GND | 接地 |
| 5 | VCC | 电源（1.8V 或 3.3V，具体取决于芯片） |
| 6 | HOLD# | 暂时暂停串行通信 |
| 7 | CLK | 时钟信号——驱动数据时序 |
| 8 | DI (MOSI) | 数据输入——从 GPU 接收数据 |

**WP# 引脚** 对于 GPU BIOS 修改尤其重要——某些电路板将其永久接地以防止意外覆盖。要刷写新 BIOS，有时需要将该引脚桥接到 VCC，或使用可以覆盖它的夹式编程器（如 CH341A）。

**参考：**

- [Winbond W25Q128 数据表](https://www.winbond.com/resource-files/w25q128jv%20spi%20revc%2011162016.pdf)
- [SPI Flash Programming — flashrom 维基](https://www.flashrom.org/Flashrom)
- [GPU BIOS 修改指南 — TechPowerUp](https://www.techpowerup.com/vgabios/)
