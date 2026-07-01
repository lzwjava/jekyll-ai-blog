---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想Windows驱动程序指南
translated: true
type: note
---

以下为联想笔记本电脑的**Windows硬件驱动程序**。各项说明如下：

| 文件 | 用途 |
| ------ | --------- |
| `audio-*.exe` | Realtek/Conexant 音频驱动 |
| `camera-*.exe` | 摄像头驱动 |
| `cardreader-*.exe` | SD读卡器驱动 |
| `chipset-*.exe` | Intel 芯片组驱动 |
| `dispatcher-*.exe` | 联想设备驱动调度程序 |
| `EM-*.exe` | 电源管理驱动 |
| `fingerprint-*.exe` | 指纹传感器驱动 |
| `HID-*.exe` | 人机接口设备驱动 |
| `intelDTT-*.exe` | Intel Dynamic Tuning Technology（散热管理） |
| `LACN41WW.exe` | 联想音频驱动套件 |
| `LAME04WW.exe` | 联想 ME（管理引擎）驱动 |
| `MEI-*.exe` | Intel 管理引擎接口 |
| `RTKwlan-*.exe` | Realtek 无线网卡驱动 |
| `sensor-*.exe` | 陀螺仪/加速度传感器驱动 |
| `SIO-*.exe` | 串行输入输出驱动 |

**可以删除它们吗？** 可以安全删除——这些是Windows平台的`.exe`安装程序，在macOS系统中无法运行。它们仅占用约185 MB的磁盘空间。只有在联想设备上重装Windows系统时才需要用到这些文件。
