---
audio: false
generated: true
lang: zh
layout: post
title: Ubuntu 挂起指南
translated: true
type: note
---

在 Ubuntu 系统中，您可以通过多种方式让电脑进入睡眠或休眠状态：

## 图形界面操作：
- **右上角菜单**：点击顶部面板的电源/设置图标，选择“挂起”（睡眠）或“休眠”（若可用）
- **活动菜单**：按下 Super 键，输入“电源”或“挂起”，选择相应电源选项

## 命令行操作：
```bash
# 进入睡眠模式
systemctl suspend

# 进入休眠模式
systemctl hibernate

# 进入混合睡眠模式（睡眠+休眠）
systemctl hybrid-sleep
```

## 键盘快捷键：
- 多数 Ubuntu 系统默认使用 **Fn + 睡眠键** 或 **Ctrl + Alt + End**
- 可通过“设置 > 键盘 > 快捷键”自定义快捷键

## 重要提示：
- **睡眠/挂起**：保持内存供电，唤醒迅速但会消耗少量电量
- **休眠**：将当前状态保存至硬盘后关机，唤醒较慢但完全断电
- 由于部分硬件兼容性问题，新版 Ubuntu 可能默认未启用休眠功能

若休眠功能无法使用，可能需要先配置交换空间并编辑系统设置。睡眠功能在大多数系统上可直接使用。
