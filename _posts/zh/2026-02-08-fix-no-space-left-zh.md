---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复设备空间不足错误
translated: true
type: note
---

Question: 系统提示 "no space left on device"，这是导致当前问题（包括 GDM 启动失败）的根本原因。在通过 Ctrl+Alt+F3（或类似组合键）进入文本控制台、登录并运行 `sudo systemctl restart gdm` 或 `sudo systemctl status gdm -l` 等命令后，问题仍然存在。如何修复 "no space left on device" 错误并恢复系统？

Answer: 

**"No space left on device"** 错误是目前的主要阻碍 —— 即使所有权/权限已部分修复，GDM（以及许多其他 service）也无法启动，因为磁盘（通常是 root `/` 分区）已完全填满。这通常发生在鲁莽的 `chown` 操作后，伴随着尝试重新安装 package、大量 log 产生或临时文件堆积。

### 在文本控制台 (TTY / Ctrl+Alt+F3) 执行的分步修复方案

1. 使用你的用户名 (`lzwjava`) 和密码**登录**文本控制台。

2. **检查哪个分区已满以及原因**

```bash
df -h
# 查看 / (root) —— 如果显示 100% 或非常接近，这就是问题所在

# 查看占用空间最大的项（逐条运行）
du -sh /* | sort -hr | head -15

# 在损坏的 Ubuntu 系统中，最常见的元凶是：
du -sh /var /var/log /var/cache /tmp /home /usr
```

Ubuntu 系统损坏时的常见占用者：
- `/var/log/journal/` —— 反复启动失败产生的大量 logs
- `/var/cache/apt/archives/` —— 旧的 .deb packages
- `/tmp/` —— 滞留的临时文件
- `/var/lib/systemd/coredump/` —— crash dumps

3. **释放空间 —— 激进但安全的清理**
请谨慎运行以下命令（这些是非破坏性的）：

```bash
# 清理旧的 package cache（通常能释放 1–5 GB）
sudo apt clean
sudo apt autoclean
sudo rm -rf /var/cache/apt/archives/*.deb 2>/dev/null

# 截断庞大的 logs（安全）
sudo journalctl --vacuum-time=2weeks
sudo journalctl --vacuum-size=100M
sudo truncate -s 0 /var/log/*.log /var/log/*/*.log 2>/dev/null

# 如果安装了多个内核，移除旧内核（每个可释放约 500 MB）
sudo apt autoremove --purge

# 彻底清理 /tmp（仅当你没有运行重要的临时任务时安全）
sudo rm -rf /tmp/*
sudo mkdir /tmp
sudo chmod 1777 /tmp

# 如果 /var/log/journal 占用巨大：
sudo rm -rf /var/log/journal/*
sudo systemctl restart systemd-journald
```

4. **再次检查空间**

```bash
df -h
free -h   # 同时检查 RAM/swap —— 低 RAM 也会导致类似症状
```

你至少需要 `/` 分区有 500 MB–1 GB 的剩余空间，才能让 GDM 和基础 service 可靠地启动。

5. **再次尝试重启 GDM**

```bash
sudo systemctl restart gdm

# 如果仍然失败，查看现在的真实错误信息
sudo systemctl status gdm -l --no-pager | tail -30

# 或者查看自上次启动以来的完整 journal
journalctl -b -u gdm --no-pager | tail -40
```

如果仍然无法工作，请复制任何新的具体错误（permission denied, cannot write file 等）。

6. **如果空间已释放但 GDM 仍无法启动**
重新运行之前的重新安装命令（现在有空间了）：

```bash
sudo apt update
sudo apt install --reinstall gdm3 ubuntu-gnome-desktop gnome-session ubuntu-session
sudo dpkg-reconfigure gdm3
sudo systemctl restart gdm
```

7. **切换到 lightdm 作为备选方案（更轻量，所需空间更少）**

```bash
sudo apt install lightdm
sudo dpkg-reconfigure lightdm   # 选择 lightdm
sudo reboot
```

如果 lightdm 成功启动，你将重新获得图形登录界面 —— 然后你可以稍后修复 GDM 或继续使用 lightdm。

### 如果你无法从 TTY 释放足够的空间
重新引导进入 **Ubuntu live USB**（就像你之前做的那样）：
- 将你的 root 分区挂载到 `/mnt`
- 然后运行类似的清理命令：

```bash
sudo mount /dev/nvme0n1pX /mnt   # 替换为你的 root 分区
sudo rm -rf /mnt/var/log/journal/*
sudo rm -rf /mnt/var/cache/apt/archives/*
sudo journalctl --rotate   # 如果 journald 可访问
```

- 或者直接使用 `du` 识别并删除最大的文件。

一旦空间被释放，系统几乎总是可以恢复的。

### 预防说明
避免在 `/usr`, `/var`, `/etc` 上运行宽泛的递归命令。仅使用针对性的修复（例如 `chown $USER:$USER ~/somefolder`）。

如果你分享 `df -h` 和 `du -sh /* | sort -hr | head`（或最大文件夹）的输出，我可以告诉你下一步确切清理哪些目录。

References:  

- [https://askubuntu.com/questions/2663/no-space-left-on-device-but-there-is-tons-of-space-available](https://askubuntu.com/questions/2663/no-space-left-on-device-but-there-is-tons-of-space-available)  
- [https://help.ubuntu.com/community/FullDisk](https://help.ubuntu.com/community/FullDisk)  
- [https://askubuntu.com/questions/104635/how-to-clear-journalctl-logs](https://askubuntu.com/questions/104635/how-to-clear-journalctl-logs)