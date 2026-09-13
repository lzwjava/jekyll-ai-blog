---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复MATS MODS USB TTY启动错误
translated: true
type: note
---

**问题：** 我按照第70号帖子（关于MATS/MODS的GRUB裸机设置）的说明操作，但USB无法启动——似乎卡住了，无法启动TTY（终端）。哪里出了问题？如何修复？

---

**解答：**

“无法启动tty”错误是这类裸机USB设置中常见的Linux启动问题。以下是可能的原因及解决方案：

**1. 错误的启动模式（UEFI vs Legacy）**

GTX版本仅支持**Legacy模式**（不支持UEFI），而RTX版本同时支持Legacy和UEFI。RTX 50系列必须使用UEFI启动。

请确保BIOS启动模式与您的显卡世代匹配：
- GTX显卡 → 将BIOS设置为**Legacy/CSM模式**
- RTX显卡 → Legacy或UEFI均可
- RTX 50xx → 必须使用**UEFI**

**2. GRUB vs Syslinux — 尝试另一种启动器**

第69号帖子提供的是**Syslinux版本**，第70号帖子提供的是**GRUB版本**。如果GRUB版本无法启动或卡在TTY，请尝试Syslinux版本——某些系统对某一种启动器的兼容性更好。

Syslinux设置（`mats_syslinux.zip`）和GRUB设置（`mats_grub.zip`）的步骤相同：将USB格式化为FAT32，将可执行文件解压到USB，然后从USB运行该可执行文件以创建启动器。

**3. USB格式问题**

在运行可执行文件之前，USB驱动器必须格式化为**默认的FAT32格式**。如果您使用了exFAT或NTFS，请重新格式化为FAT32并重新进行设置。

**4. 屏幕分辨率问题**

对于RTX映像，屏幕分辨率被强制设置为**1280x720**，并且可以在`syslinux.cfg`文件中更改。如果您的显示器不支持该分辨率，启动过程可能看起来像是卡住了（但实际上正在运行，只是没有可见输出）。请尝试使用不同的显示器或电视。

**5. 显卡无显示输出**

如果显卡本身有故障且无法输出画面，您需要一块带有集成显卡（iGPU）的主板和CPU，将显示器连接到**主板的显示输出接口**，然后在运行`mods`或`mats -n 1`之前，先运行`modsinit`。

---

**快速检查清单：**

| 检查项 | 操作 |
|---|---|
| 启动模式 | 将Legacy/UEFI与您的显卡世代匹配 |
| 启动器 | 如果GRUB失败，尝试Syslinux |
| USB格式 | 必须为FAT32 |
| 显示输出 | 如果显卡无信号，使用集成显卡输出 |
| 分辨率 | 如果屏幕空白，尝试不同的显示器 |

---

**参考链接：**
- [Nvidia MATS & MODS USB启动盘（含NVMT） — Levirepair论坛](https://www.levirepair.eu/infusions/forum/viewthread.php?thread_id=3&pid=70#post_70)