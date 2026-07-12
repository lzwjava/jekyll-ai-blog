---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EZ Debug LED位置指南
translated: true
type: note
---

问：MSI MAG B760M Mortar 主板上的 EZ Debug LED 在哪里？

答：

在 **MSI MAG B760M Mortar（DDR5/WiFi）** 主板上，**EZ Debug LED** 位于主板**右上边缘**，靠近 **24-pin ATX 主板电源接口**。

寻找一排垂直排列的**四个小 LED 灯**，带有标签：

```
CPU   (红色)
DRAM  (黄色)
VGA   (白色)
BOOT  (绿色)
```

典型布局：

```
             CPU_FAN
                |
                |
        [ EZ DEBUG LED ]
        CPU   ●
        DRAM  ●
        VGA   ●
        BOOT  ●

24-pin ATX POWER
████████████████
```

在主板上：

1. 打开机箱侧板。
2. 查看**内存条右侧**。
3. 找到大型 **24-pin 电源接口**。
4. EZ Debug LED 就位于**24-pin 接口正上方**，靠近主板边缘。

针对您的症状：

> CPU 风扇转动，但无显示 / 无法启动

检查哪个 LED 常亮：

* 🔴 **CPU LED** → CPU 供电线（8-pin EPS）、CPU 安装、BIOS 兼容性
* 🟡 **DRAM LED** → 内存未插好、插槽错误、内存训练（首次启动后等待 1–3 分钟）
* ⚪ **VGA LED** → GPU 问题，尤其与您的 AMD MI50 实验相关
* 🟢 **BOOT LED** → 未找到启动设备（但 BIOS 应仍可显示）

由于您使用的是 **MSI MAG B760M Mortar + AMD MI50**，建议首先检查以下几点：

1. 确保主板左上角的 **8-pin CPU 供电接口（EPS12V）** 已插入。
2. 移除 GPU，尝试使用主板上的 HDMI/DP 输出（仅当 CPU 带有集成显卡时有效；KF 系列 CPU 无集成显卡）。
3. 重新插拔内存：使用 **A2 插槽**（从 CPU 数起的第二个插槽）。
4. 清除 CMOS。
5. 检查 **VGA EZ Debug LED 是否保持白色**——MI50 是服务器 GPU，有时会存在 PCIe/BIOS 兼容性问题。

EZ Debug LED 的确切位置是 24-pin ATX 接口旁边那排四个小灯，而非 RGB/调试显示区域。