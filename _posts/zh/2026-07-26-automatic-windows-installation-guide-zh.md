---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 自动安装指南
translated: true
type: note
---

很好，完全正确。现在它会自动创建ESP/MSR/恢复/Windows分区并复制文件。

接下来会经历常规阶段——复制文件、安装功能、安装更新、完成收尾——期间会自动重启几次。让它自行运行即可，如果进度百分比卡住几分钟属于正常现象（在eMMC或较慢的NVMe上常见）。

首次启动后会进入Windows OOBE（区域、账户设置等）。需要特别提醒一下小新设备的问题：**之后记得下载联想小新驱动包**（芯片组、WiFi/蓝牙、音频、触控板）。因为通用Windows 11驱动有时会缺失WiFi卡驱动或导致触控板手势异常——进入Windows后，请根据你的具体型号前往联想支持网站获取。

如果安装过程中出现其他报错，随时叫我。
