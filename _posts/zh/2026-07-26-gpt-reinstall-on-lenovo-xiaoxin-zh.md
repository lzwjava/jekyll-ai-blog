---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT重装联想小新
translated: true
type: note
---

## ✅ 完成 — 已使用 GPT 重新安装

### 变更内容

| 之前 | 之后 |
| --- | --- |
| **MBR** 分区样式 | **GPT** 分区样式 |
| Ventoy 默认安全启动 | Ventoy 默认安全启动（仍启用） |
| 已复制 Win10 ISO | 已复制 Win10 ISO（5.8G） |

### 在您的联想小新上 — 请按以下步骤操作

1. **启动** → 按 **F2** 进入 BIOS 设置
2. **安全选项卡** → **安全启动** → **禁用**
3. **启动选项卡** → **启动模式** → **UEFI**（非 Legacy）
4. **保存并退出**（F10）
5. 立即按 **F12** 进入启动菜单
6. 现在您应该能看到列表中的 **UEFI：<USB 名称>**
7. 选择它 → Ventoy 菜单 → `Win10_22H2_English_x64v1.iso` → 回车

如果**仍未显示**，请在 BIOS 中尝试以下设置：

- **USB 启动** → **启用**
- **XHCI 切换** → **启用**
- 尝试使用 **USB 2.0 端口** 而非 USB 3.0（在较旧的小新机型上有时会有影响）
