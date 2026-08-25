---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主板无电源故障排除
translated: true
type: note
---

**问题：** 我为技嘉 GA-H81M-DS2 主板购买了一个蜂鸣器排针，但主板不通电——如何修复不通电问题，以便使用蜂鸣器排针？

**回答：**

如果主板完全不通电，蜂鸣器排针本身无法工作——根本问题在于无法开机自检（no-POST）/不通电。蜂鸣器实际上是一种诊断工具：一旦主板通电并尝试开机自检，它会通过蜂鸣器发出哔声代码，告诉你问题所在。

以下是恢复主板供电的方法：

**1. 检查电源连接**
确保主板上的 24 针 ATX 电源连接器和 4 针 CPU 电源连接器都已完全插紧。遗漏 4 针 CPU 连接器是完全无法通电的常见原因。

**2. 使用最小化配置进行测试**
断开所有非必要组件，仅保留：CPU、1 根内存条和电源。不连接显卡、硬盘、扩展卡。尝试开机。如果主板此时能通电，说明某个外设导致了短路。

**3. 检查是否短路**
确保主板没有直接接触金属机箱（缺少铜柱螺丝可能导致整板短路）。如果在机箱外测试，请将主板放在非导电表面（如包装盒）上。

**4. 测试或更换电源**
电源功率不足或出现故障是常见原因。建议使用 500W 或更高功率的电源。如果有已知完好的电源，可以替换测试。

**5. 清除 CMOS**
拔掉电源线，取下主板上的纽扣电池约 1 分钟，然后重新装回。这会将 BIOS 设置重置为默认值，可能解决阻止启动的问题。

**6. 检查主板是否有物理损坏**
检查供电区域附近是否有电容鼓包、烧焦痕迹或 MOSFET 损坏。如果发现，主板可能需要专业维修。

一旦电源恢复并且主板开始开机自检，蜂鸣器排针就会发出哔声代码——以此来指示内存、显卡或其他组件是否存在问题。

---

**参考资料：**
- [GA-H81M-DS2 用户手册（技嘉官方 PDF）](https://download.gigabyte.com/FileList/Manual/mb_manual_ga-h81m-ds2_4001_e.pdf)
- [lzwjava.com — 技嘉 H81M-DS2 无显示修复](https://lzwjava.com/gigabyte-h81m-ds2-no-display-fix-en)
- [Badcaps 论坛 — GA-H81M-DS2 持续断电重启（已解决）](https://www.badcaps.net/forum/troubleshooting-hardware-devices-and-electronics-theory/troubleshooting-desktop-motherboards-graphics-cards-and-pc-peripherals/85547-solved-gigabyte-ga-h81m-ds2-rev-3-0-constant-power-cycling)