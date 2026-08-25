---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PC主板LED灯区别
translated: true
type: note
---

问题：PC主板上的HDD LED和Power LED有什么区别？

答案：

**Power LED** 指示计算机处于开机、关机还是睡眠状态。通常开机时常亮，关机时熄灭，睡眠/待机时闪烁。

**HDD LED**（硬盘指示灯）在存储设备（HDD或SSD）进行读取或写入操作时会闪烁。它提供磁盘活动的实时指示。

| 特性 | Power LED | HDD LED |
| --- | --- | --- |
| 显示内容 | 系统电源状态 | 存储活动 |
| 行为 | 常亮 / 睡眠时闪烁 | 磁盘读写时闪烁 |
| 连接器引脚 | `PWR LED+` / `PWR LED−` | `HDD LED+` / `HDD LED−` |
| 是否适用于SSD？ | 不适用 | 是，SSD活动时仍会闪烁 |

实用技巧：如果系统看似卡死，查看HDD LED可以判断它是否仍在执行操作（忙碌中）还是真正无响应。
