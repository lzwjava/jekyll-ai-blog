---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB已移除，Ventoy就绪
translated: true
type: note
---

USB 设备 `/dev/sdb` 已不再连接——它已被移除。

回顾已完成的操作：

### 本次操作

| 项目 | 详情 |
| --- | --- |
| **USB** | 新 USB (`/dev/sdb`, 型号: YGS, 14.6G) |
| **ISO** | 来自 `~/Downloads/` 的 `Win10_22H2_English_x64v1.iso` (5.8G) |
| **工具** | 已安装 Ventoy v1.1.17 |
| **ISO 已复制** | 确认在 Ventoy 分区上为 5.8G |
| **状态** | 已同步、已卸载并已断电 ✅ |

### USB 上的内容

```
/dev/sdb1 (exFAT, label: Ventoy)
  └── Win10_22H2_English_x64v1.iso  (5.8G)

/dev/sdb2 (vfat, label: VTOYEFI)
  └── Ventoy bootloader
```

**仅有 Windows 10 22H2** —— 单个 ISO，干净安装。通过 Ventoy 菜单启动即可。

可以**安全移除** —— 已断电。👍
