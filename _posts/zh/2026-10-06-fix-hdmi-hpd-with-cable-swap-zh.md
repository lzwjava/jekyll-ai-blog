---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更换线缆修复HDMI HPD问题
translated: true
type: note
---

### 说明

- **脚本**：`/home/lzw/fix-hdmi-hpd.sh`（幂等；可重复执行）。
- **备份**：`/etc/default/grub.bak.20261006020242` — 恢复方法：`sudo cp /etc/default/grub.bak.* /etc/default/grub && sudo update-grub` 然后重启。
- **权衡**：关闭轮询后，运行时插入*不同*显示器将无法自动检测（适用于固定桌面场景）。
- **过时配置**：`~/.config/monitors.xml` 中仍列出一个不存在的 `DVI-I-1` 1024x768 显示器。虽非问题根源，但建议清除——如有需要请告知。

### 仍建议执行

这些只是软件层面的临时方案。根本原因在于 HDMI **HPD** 信号线抖动——**请更换 HDMI 线缆**（或尝试 `HDMI-A-2`/DP 接口）。若更换好线缆并重启后问题依旧，则可能是 GPU 端口或显示器输入端存在故障。
