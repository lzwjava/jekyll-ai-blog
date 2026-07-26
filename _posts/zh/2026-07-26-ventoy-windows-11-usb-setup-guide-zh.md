---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy Windows 11 USB 安装指南
translated: true
type: note
---

## ✅ 完成！Ventoy v1.1.17 + Windows 11 ISO — 已完成

### 最终 USB 布局

| 分区 | 大小 | 文件系统 | 标签 | 内容 |
| --- | --- | --- | --- | --- |
| `/dev/sdb1` | 14.6G | exFAT | **Ventoy** | `Win11_25H2_English_x64_v2.iso` (7.9G) |
| `/dev/sdb2` | 32M | vfat | **VTOYEFI** | Ventoy EFI 引导加载器 |

### 使用方法

1. **插入 USB** 到你的联想小新笔记本
2. **开机** → 按 F2/F12（或你机型对应的进入启动菜单的按键）
3. 选择 **UEFI: <USB 名称>**（不要选 legacy/CSM）
4. 出现 Ventoy 菜单 → 选择 `Win11_25H2_English_x64_v2.iso`
5. Windows 安装程序启动

### 如果 SSD 未被识别（联想小新常见问题）

Windows 11 安装程序可能无法识别 NVMe SSD — 这是 **Intel VMD/RST 驱动** 问题。你需要：

1. 从 [Intel 官网](https://www.intel.com/content/www/us/en/download/19512/) 下载 Intel RST F6 驱动
2. 解压到 **第二个 U 盘**
3. 在磁盘选择界面 → **加载驱动程序** → 浏览到解压的文件夹
4. SSD 出现 → 继续安装

### 额外提示：多 ISO 启动

Ventoy 支持多个 ISO 文件。你可以将 Linux ISO、救援盘等与 Windows 放在一起：

```bash
sudo cp ~/Downloads/ubuntu-24.04-desktop.iso /media/$USER/Ventoy/
```

所有 ISO 都会显示在 Ventoy 启动菜单中。
