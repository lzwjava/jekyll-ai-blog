---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Ubuntu 启动进入 TTY
translated: true
type: note
---

问题：为什么 Ubuntu 会引导到 TTY（终端）而不是正常的图形窗口，以及如何切换回 GUI？

回答：

当 Ubuntu 引导到 TTY（纯文本终端，如 `tty1`）而不是图形桌面时，通常表示图形系统启动失败。这通常与 display manager、desktop environment 或 graphics drivers 相关。

---

## 🚀 快速临时修复（优先尝试）

按下：

```
Ctrl + Alt + F2   (或 F1–F7)
```

* 其中一个可能会带你回到图形登录屏幕。
* 如果看到 GUI → 正常登录即可。

---

## 🔧 步骤 1：手动启动 GUI

在 TTY 中登录，然后运行：

```bash
startx
```

如果成功 → 问题可能是 display manager 未自动启动。

---

## 🔧 步骤 2：重启 Display Manager

Ubuntu 使用 display manager，如：

* `gdm3`（GNOME 默认）
* `lightdm`（较旧系统）

尝试：

```bash
sudo systemctl restart gdm3
```

或：

```bash
sudo systemctl restart lightdm
```

如果 GUI 出现 → 问题是暂时的。

---

## 🔧 步骤 3：在引导时启用 GUI

检查默认 target：

```bash
systemctl get-default
```

如果显示：

```
multi-user.target
```

👉 这意味着仅 CLI 模式。

修复它：

```bash
sudo systemctl set-default graphical.target
sudo reboot
```

---

## 🔧 步骤 4：重新安装桌面环境

有时 GNOME 已损坏：

```bash
sudo apt update
sudo apt install ubuntu-desktop
```

最小重新安装：

```bash
sudo apt install --reinstall gdm3
```

---

## 🔧 步骤 5：检查磁盘空间（非常常见！）

```bash
df -h
```

如果根分区 (`/`) 已满 → GUI 无法启动。

清理：

```bash
sudo apt clean
sudo apt autoremove
```

---

## 🔧 步骤 6：检查 GPU / 驱动问题

如果你最近安装了 NVIDIA 驱动，它可能会破坏 GUI。

尝试：

```bash
sudo ubuntu-drivers autoinstall
```

或移除有问题的驱动：

```bash
sudo apt purge nvidia*
```

---

## 🔧 步骤 7：检查日志（高级）

```bash
journalctl -xe
```

或：

```bash
cat /var/log/Xorg.0.log | grep EE
```

查找与以下相关的错误：

* display
* GPU
* gdm

---

## 🧠 常见原因总结

| 原因                   | 解释                          |
| --------------------- | ----------------------------- |
| GUI 被禁用            | 系统引导目标设置为 CLI        |
| Display manager 崩溃  | gdm3/lightdm 未启动           |
| 磁盘已满              | 无空间 → GUI 失败             |
| 更新损坏              | 软件包部分安装                |
| GPU 驱动问题          | 尤其是 NVIDIA                 |

---

## ✅ 最快修复路径（推荐顺序）

1. `Ctrl + Alt + F2~F7`
2. `sudo systemctl restart gdm3`
3. `systemctl get-default` → 设置为 graphical
4. 检查磁盘：`df -h`
5. 重新安装：`sudo apt install ubuntu-desktop`

---

如果你愿意，请粘贴你在 TTY 中看到的内容（错误、登录消息），我可以快速定位确切根因。