---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 通过 GRUB 恢复模式修复 Sudo
translated: true
type: note
---

Question: I am now at the GRUB menu showing options like Ubuntu, Advanced options, Memory test, etc. How do I proceed to fix the broken sudo?

Answer:

Since your main goal is to recover the broken sudo (due to wrong ownership after the chown mistake), **do not** select the normal "Ubuntu" entry yet — it will boot into the broken system and you still won't have sudo.

Instead, follow one of these two paths from the current GRUB screen (both can work, pick the easier one for you):

**Path 1: Try Recovery Mode first (fastest if it works — no USB needed)**

1. 在 GRUB 中，高亮选择 **Advanced options for Ubuntu** 并按 Enter。
2. 你会看到一个 kernel 列表，例如：
   - Ubuntu, with Linux 6.8.0-40-generic (或类似内容)
   - Ubuntu, with Linux 6.8.0-40-generic (recovery mode)   ← **选择这一项**
   - Older kernels (如果有的话)
3. 选择对应最新 kernel 的 **(recovery mode)** 行（通常是第二或第三行）并按 Enter。
4. 等待 recovery menu 出现。它看起来像一个紫色/蓝色的文本界面，包含如下选项：
   - resume             normal boot
   - clean              clean disk space
   - dpkgs              repair broken packages
   - fsck               check all filesystems
   - grub               update GRUB boot loader
   - network            enable networking
   - root               Drop to root shell prompt   ← **选择这一项**
5. 选择 **root** → 按 Enter。
6. 你现在应该进入了 root shell 提示符（显示 # 符号，已经是 root 权限 — 大多数情况下不需要密码）。
7. 文件系统起初可能是 read-only（只读）的。将其设为可写：

   ```
   mount -o remount,rw /
   sync
   ```

8. 现在修复 sudo（最简命令）：

   ```
   chown root:root /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   ```

   同时修复你之前提到的 sudo library 目录：

   ```
   chown -R root:root /usr/lib/sudo
   chmod -R 755 /usr/lib/sudo
   ```

9. 可选但强烈建议 — 修复更多由 chown -R 造成的常见损坏：

   ```
   chown root:root /usr/bin/pkexec 2>/dev/null
   chmod 4755 /usr/bin/pkexec 2>/dev/null
   chown -R root:root /usr/libexec /usr/lib/cups 2>/dev/null
   ```

10. 退出 shell 并继续启动：

    ```
    exit
    ```

    然后选择 **resume**（或者如果你愿意，直接输入 `reboot`）。
11. 系统现在应该可以正常启动，sudo 应该恢复工作了（登录后用 `sudo -l` 测试）。

**Path 2: If recovery mode fails or you get errors → boot from the Ubuntu live USB instead**

- 重启电脑（如有必要，长按电源键）。
- 进入 **boot menu**（启动时按下 F12, F10, F9, Esc 或屏幕上显示的类似按键 — 不同笔记本/品牌按键不同）。
- 选择你的 USB 启动盘（可能显示为 "USB: Kingston", "UEFI: Ubuntu" 等）。
- 选择 **Try Ubuntu** (而不是 Install)。
- 进入桌面后 → 按照我之前给你的 live USB chroot 步骤操作：
  - 使用 `lsblk -f` 识别分区
  - 挂载分区 (`sudo mount /dev/sdaX /mnt/root`)
  - 为 /dev /proc /sys /run /dev/pts 挂载 bind mounts
  - `sudo chroot /mnt/root`
  - 运行与上方相同的 chown/chmod 命令
  - 退出，卸载分区，拔掉 USB 重启

**快速提示：** 如果你能通过 Recovery Mode（方案 1）成功修复，速度会快得多 — 无需动用 USB。
如果它没有给你一个可用的 root shell（例如掉进了 busybox 或出现文件系统错误），请直接采用方案 2。

修复 sudo 后，你还可以在修复好的系统中清理巨大的 CUPS 日志：

```
sudo truncate -s 0 /var/log/cups/error_log*
```

祝你好运 — 胜利在望。

References:

- [Ask Ubuntu: How to boot into recovery mode](https://askubuntu.com/questions/156209/how-do-i-boot-to-recovery-mode)
- [Ubuntu Community Help: RecoveryMode](https://help.ubuntu.com/community/RecoveryMode)
