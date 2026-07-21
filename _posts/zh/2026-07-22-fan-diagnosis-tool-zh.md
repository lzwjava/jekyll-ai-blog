---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 风扇诊断工具
translated: true
type: note
---

完成。已保存至 `~/projects/ww/ww/linux/check_fan.py`，并注册为 `ww linux check-fan`。

下次听到风扇噪音大时，只需运行：

```
ww linux check-fan
```

它会一次性收集以下信息：

- **温度** — CPU 核心、GPU、NVMe、机箱，通过 lm-sensors + sysfs 获取
- **风扇控制器** — PWM 芯片、导出的通道、占空比，或检测到 "BIOS controls fans"
- **GPU 风扇** — nvidia-smi 风扇转速百分比、温度、功耗
- **旋转磁盘** — lsblk ROTA 标志以标记 HDD
- **thermald** — 热守护进程是否有配置文件，或是否在轮询模式下运行
- **CPU 负载/频率** — 最高消耗进程 + 每核心 MHz
- **磁盘 I/O** — iostat 快照，显示 util%、await、iowait
- **总结结论** — 告知操作系统是否没有风扇控制（需要 BIOS 修复），或标记 HDD 噪音

已提交并推送为 `c9cca06`。