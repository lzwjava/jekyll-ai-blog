---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 2000 在Ubuntu启动画面处卡死
translated: true
type: note
---

**问题：** 为什么 NVIDIA Quadro 2000 GPU 能点亮并显示 BIOS，但随后 Ubuntu 在红色启动画面处冻结约 10 秒，始终无法进入登录界面？

---

**回答：**

这是一个非常经典的 NVIDIA + Ubuntu 启动冲突。显卡在 BIOS 阶段（使用 VESA/固件帧缓冲区）正常工作，但 Ubuntu 启动过程中会将显示控制权移交给 GPU 驱动程序——问题就出在这里。以下是原因及解决方法：

---

### 根本原因

Ubuntu 启动时，视频/图形模式设置由内核处理。如果在图形初始化期间发生冲突（这在 NVIDIA 硬件上尤为常见），系统会在启动画面处锁定。

Quadro 2000（GF106GL 芯片）年代较旧，因此在以下两者之间会产生张力：

1. **`nouveau` 开源驱动程序**（默认加载）——Ubuntu 默认使用 `nouveau` 内核驱动程序处理 Quadro 2000，并启用 modesetting。该驱动程序在早期启动 KMS（内核模式设置）交接时可能不稳定。

2. **缺失或损坏的专有 NVIDIA 驱动程序**——Quadro 2000 需要旧版 NVIDIA 驱动 470.xx（最后一个支持 Fermi 架构显卡的版本）。如果未安装，nouveau 接管——有时会在启动过程中失败。

启动画面（Plymouth）隐藏了实际输出，因此您只会看到冻结的红色/橙色 Ubuntu 屏幕，而无法得知底层发生了什么故障。

---

### 修复方法——逐步操作

**第一步：临时添加 `nomodeset`（以便进入系统）**

在 GRUB 内核参数中添加 `nomodeset`。这告诉内核在显示服务器启动 *之后* 再加载视频/图形驱动程序，从而避免早期启动冲突。登录后，即可安装正确的驱动程序。

在 GRUB 菜单处（启动时按住 **Shift**），按 **E**，找到以 `linux` 开头的行，在末尾 `quiet splash` 之前添加 `nomodeset`。按 **Ctrl+X** 启动。

**第二步：进入系统后，安装正确的专有驱动程序**

```bash
sudo apt update
sudo ubuntu-drivers autoinstall
# 或手动安装：
sudo apt install nvidia-driver-470
sudo reboot
```

**第三步：永久修复 GRUB（如果仍需使用 nomodeset）**

```bash
sudo nano /etc/default/grub
# 修改这一行：
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"
sudo update-grub
```

**第四步：检查 Plymouth 问题**

Plymouth（启动画面管理器）有时会崩溃，导致表面卡死，即使系统底层仍在工作。您可以从 GRUB 行中移除 `splash` 以查看实际启动输出——冻结前的最后一行就是线索。

**第五步：如果怀疑 nouveau 与专有驱动程序冲突**

安装 NVIDIA 驱动后禁用 nouveau：

```bash
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u
sudo reboot
```

---

### 总结表格

| 症状 | 可能原因 |
| --- | --- |
| BIOS 显示正常 | VESA/固件帧缓冲区——无驱动程序参与 |
| 在 Ubuntu 红色画面处冻结约 10 秒 | KMS 交接给 nouveau 失败 |
| 始终无法进入登录界面 | 显示管理器（GDM）无法启动 |
| 使用 `nomodeset` 后正常工作 | 确认是驱动程序/KMS 冲突 |

---

**参考链接：**

- [How to Fix Ubuntu Stuck at Boot Screen](https://oneuptime.com/blog/post/2026-03-02-how-to-fix-ubuntu-stuck-at-boot-screen/view)
- [Ubuntu Freezing at Boot – itsfoss.com](https://itsfoss.com/fix-ubuntu-freezing/)
- [Quadro 2000 with nouveau on Linux Mint Forums](https://forums.linuxmint.com/viewtopic.php?t=412775)
- [Nouveau KMS Documentation](https://nouveau.freedesktop.org/KernelModeSetting.html)
