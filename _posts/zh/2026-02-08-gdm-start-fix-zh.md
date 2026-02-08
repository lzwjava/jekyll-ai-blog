---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 GDM 服务启动失败
translated: true
type: note
---

Question: 在进入 recovery mode 或通过 Ubuntu live USB 进行 chroot 后，尝试启动图形界面或重启时，系统仍然提示 "Failed to start gdm.service" (GNOME Display Manager 启动失败)。该如何修复？

Answer: 

"Failed to start gdm.service" 错误通常意味着 GDM 因为权限问题、文件缺失/损坏或 dependencies 损坏而无法启动——在你运行过 `sudo chown -R $(whoami) /usr/` 之后，这些情况极易发生。以下是按推荐顺序排列的最有效的修复步骤。

### Step 1: 再次进入 recovery / root shell (最安全的起点)

使用以下方法之一：
- GRUB → 编辑启动项 → 在 linux 行末尾添加 `rw init=/bin/bash` → Ctrl+X
- 或者从 live USB 启动 → chroot 进入你安装的系统（如前所述）

进入 root shell 后：

### Step 2: 核心所有权与权限修复 (务必执行)

```bash
# 如果需要，重新挂载 root 为读写模式
mount -o remount,rw /

# 修复必须由 root 拥有的主要目录
chown -R root:root /usr
chown -R root:root /etc
chown -R root:root /var
chown root:root / 2>/dev/null

# 恢复标准目录权限 (对 executables 非常重要)
chmod -R 755 /usr/bin /usr/sbin /usr/lib /usr/libexec /usr/share
chmod -R 755 /bin /sbin /lib /lib64 /lib32 2>/dev/null
chmod -R u+rX,go+rX,go-w /usr/bin /usr/sbin /usr/lib /usr/libexec

# 修复常见的 service 和 config 位置
chmod 755 /usr/lib/systemd /usr/lib/systemd/system
chmod 644 /usr/share/gdm /etc/gdm /etc/gdm3 2>/dev/null
chown -R root:root /usr/share/gdm /etc/gdm /etc/gdm3 2>/dev/null

# 确保 /tmp 具有正确的 sticky bit
chmod 1777 /tmp
```

### Step 3: 重新安装 GDM 和 GNOME 核心软件包 (通常能解决问题)

```bash
# 确保 chroot 中的 networking 正常工作 (如果尚未操作)
mount --bind /dev   /dev
mount --bind /proc  /proc
mount --bind /sys   /sys
mount --bind /run   /run

# 更新 package 列表
apt update

# 重新安装 GDM + desktop metapackage (这会恢复缺失或损坏的文件)
apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session gdm3 \
  gnome-shell ubuntu-session xserver-xorg-core xserver-xorg-video-all \
  --no-install-recommends

# 可选：如果你怀疑损坏更深，也可以重新安装以下内容
apt install --reinstall systemd udev libpam-systemd dbus policykit-1 \
  accountsservice libpam-gnome-keyring
```

### Step 4: 清理 GDM cache 和日志，重新生成配置

```bash
rm -rf /var/lib/gdm3/.cache/* 2>/dev/null
rm -f /var/log/gdm3/* 2>/dev/null

# 如果需要，重新生成 GDM 配置
dpkg-reconfigure gdm3

# 确保 GDM 是默认的 display manager
echo "/usr/sbin/gdm3" > /etc/X11/default-display-manager
```

### Step 5: 最后检查并重启

```bash
# 检查明显的错误
journalctl -u gdm --since "1 hour ago"   # 如果 journald 正在运行

# 将更改同步到磁盘
sync

# 如果你在 chroot 中，请退出 (必要时键入 exit 两次)
exit
umount /mnt/dev /mnt/proc /mnt/sys /mnt/run /mnt 2>/dev/null

reboot
```

### 如果重启后仍然失败

- 你可能会看到黑屏或闪烁的游标 → 按下 **Ctrl+Alt+F3** (或 F2–F6) 获取文本终端 → 以你的用户身份登录 → 运行：
  ```bash
  sudo systemctl restart gdm
  # 或者
  sudo systemctl status gdm -l
  ```
  查看最后 10–20 行输出 — 复制任何具体的错误（例如 "permission denied", "cannot execute", "missing file" 等）并进行排查。

- 临时切换到另一个 display manager (lightdm 更轻量，更容易恢复)：
  ```bash
  apt install lightdm
  dpkg-reconfigure lightdm   # 选择 lightdm
  reboot
  ```
  如果 lightdm 可以工作，你可以在一切修复后再切回 gdm3。

### 快速替代方案：从 live USB 重新安装 desktop (如果上述步骤太麻烦，此法更快)

在 live USB 的 "Try Ubuntu" 模式下：
1. 将你的 root 分区 (`/dev/nvme0n1pX` 或类似) 挂载到 `/mnt`
2. 运行：
   ```bash
   sudo apt update
   sudo apt install --reinstall ubuntu-desktop^ gdm3
   ```
   (`^` 符号会重新安装整个 tasksel 组)

这通常能解决 90% 因 chown 导致的 GNOME 损坏问题，而无需全盘重装。

**不要**再对系统目录运行任何递归的 chown/chmod —— 这是导致问题的根源。

References:  

- [https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr](https://askubuntu.com/questions/26496/how-to-recover-from-accidentally-changing-ownership-of-usr)  
- [https://askubuntu.com/questions/1029472/gdm-failed-to-start-after-changing-permissions](https://askubuntu.com/questions/1029472/gdm-failed-to-start-after-changing-permissions)  
- [https://wiki.ubuntu.com/RecoveryMode](https://wiki.ubuntu.com/RecoveryMode)