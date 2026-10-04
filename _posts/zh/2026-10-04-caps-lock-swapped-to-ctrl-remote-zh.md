---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Caps Lock交换至Ctrl远程
translated: true
type: note
---

已验证 — **已切换并生效于 `192.168.1.45`** ✅

当前机器上的状态：

- `xkb-options` = `['ctrl:swapcaps']`（持久保存在用户的 dconf 中）
- 输入布局：`us`（单个布局，因此该选项适用于所有输入）
- GNOME Wayland 会话（会话 3，tty2）处于 **活动** 状态，gnome-shell 正在运行且设置了该选项（`gsd-keyboard` 守护进程已确认）
- 日志甚至证明了持久性：会话在今天 05:31 被重新创建（新的登录/重启），设置依然存在——它存储在 `~/.config/dconf/user` 中，因此重启后仍保留

**该机器键盘当前的实际效果：**

| 按下的按键 | 输出结果 |
| --- | --- |
| **Caps Lock** | → **Ctrl**（左 Control 行为） |
| **左 Ctrl** | → **Caps Lock** |

**适用范围**：这适用于该盒子上的 **GNOME 桌面会话**——即插入该盒子的物理 USB 键盘，或附加到该 GUI 会话的任何输入会话（GNOME Remote Desktop 等）。

⚠️ 请在你那端确认两件事：

1. 如果你在 SSH 登录时使用的是 **笔记本电脑自己的键盘**，那么交换不适用于笔记本——它只适用于远程机器的键盘处理。
2. 如果你是想与 **右 Ctrl** 进行交换，那是另一个选项（`ctrl:swapcaps_rctrl`）——请告诉我，我会修改。

如果在实际硬件键盘上仍然感觉没有交换，请告诉我，我会进一步检查物理键盘是否走的是不同的输入路径（例如 KVM 或无线适配器会话）。
