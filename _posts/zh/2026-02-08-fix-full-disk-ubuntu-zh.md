---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复磁盘满载并恢复 Ubuntu
translated: true
type: note
---

**Question:** 我的磁盘一直是满的。我删除了 3 GB 的文件并重启，但现在 Ubuntu live USB 出现了，选择它后，GDM 再次启动失败。使用 Ctrl+Alt+F3 并运行 `df -h` 显示 468 GB 的磁盘 100% 已满。我该如何找到最大的文件，停止占用磁盘的内容，并修复系统？

**Answer:**

你的系统正处于危急状态——root filesystem 已完全填满 (100%)，这会导致无法正常引导、登录管理器 (GDM) 无法启动，并且通常会破坏许多 services。

### Step 1: 立即进入可用的 root shell

你已经进入了 tty3 (Ctrl+Alt+F3) → 很好。

如果你**尚未**登录：

- Username: 你的普通用户名
- Password: 你的用户密码

如果因为 filesystem 是 read-only 或太满而导致登录失败：

尝试强制重新挂载为 rw (通常是必须的)：

```bash
mount -o remount,rw /
```

然后再次尝试登录。

如果仍然无法以用户身份登录 → 尝试 root (如果你有 root 密码)：

```bash
Login: root
Password: ...
```

如果没有 root 密码或不起作用 → 使用 live USB 引导 (这是下一步最安全的做法)。

### Step 2: 快速查找占用磁盘的内容 (通过 tty 或 live USB)

在故障系统的 tty 中 (如果你已获取 shell)：

```bash
# 查看最大目录的最快方法
du -shx /* 2>/dev/null | sort -hr | head -15

# 然后深入查看最大的目录，例如：
du -shx /var/* 2>/dev/null | sort -hr | head -10
du -shx /var/log/* 2>/dev/null | sort -hr | head -8
du -shx /home/* 2>/dev/null | sort -hr
```

磁盘突然填满时最常见的巨大“罪魁祸首”：

- `/var/log/journal/` (systemd journal) – 非常常见
- `/var/log/` (nginx/apache/mysql 日志，没有 rotation 的 syslog)
- `/var/cache/apt/archives/` (旧的 .deb 软件包)
- `/tmp/` 或 `/var/tmp/` (某些程序写入的巨型临时文件)
- `/home/youruser/.cache/` (thumbnails, 浏览器 cache, flatpak cache…)
- Docker: `/var/lib/docker/`
- Snap: `/var/lib/snapd/snaps/`
- Timeshift snapshots: `/timeshift/`

查看绝对值最大的单个文件 (非常有用)：

```bash
find / -xdev -type f -size +500M -exec ls -lh {} \; 2>/dev/null | sort -hr
```

或者甚至更大的文件：

```bash
find / -xdev -type f -size +1G -ls 2>/dev/null | sort -k7nr | head -20
```

### Step 3: 立即进行应急空间回收 (删除最大的安全项)

按从大到小且最安全的顺序：

```bash
# 1. 清理旧的 apt cache (通常有几个 GB)
apt-get clean
rm -rf /var/cache/apt/archives/*.deb

# 2. 清理 systemd journal (故障时通常占用 10–30+ GB)
journalctl --vacuum-size=100M
# 或者彻底清理：
rm -rf /var/log/journal/*   # 然后重启 → journald 会重新创建

# 3. 移除旧的 snaps (如果你使用 snap)
snap list --all | grep disabled | awk '{print $1, $3}' | while read snap rev; do snap remove "$snap" --revision="$rev"; done

# 4. 清理 thumbnail cache
rm -rf /home/*/ .cache/thumbnails/*

# 5. 清理 /tmp (通常是安全的)
rm -rf /tmp/*
```

在每次大幅删除后 → 检查剩余空间：

```bash
df -h /
```

### Step 4: 停止持续填满磁盘的进程

2024–2026 年 Ubuntu 系统中最常见的原因：

- Journald 未设置限制 → 在 `/etc/systemd/journald.conf` 中添加：

```ini
SystemMaxUse=300M
SystemKeepFree=2G
RuntimeMaxUse=100M
```

然后执行：`systemctl restart systemd-journald`

- rsyslog / syslog-ng 无限写入且没有 rotation
- snapd 无休止地刷新巨大的 snaps
- flatpak 更新带有巨大 caches 的应用
- docker container 日志没有限制 (json-file driver)
- 某些 VPN / 挖矿 / 备份软件写入日志或临时文件

快速检查当前正在活跃写入的内容：

```bash
watch -n 2 "lsof / | grep REG | grep -v deleted | awk '{print \$NF}' | sort | uniq -c | sort -nr | head -8"
```

或者更简单的：

```bash
iotop   # (如果需要请安装：apt install iotop)
```

### Step 5: 建议的现实恢复路径

1. 引导 Ubuntu live USB (首选相同版本)
2. 打开 terminal
3. 挂载你的 root 分区：

```bash
sudo mount /dev/nvme0n1pX /mnt          # 或 sdaX，通过 lsblk 检查
sudo mount --bind /dev  /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys  /mnt/sys
sudo mount --bind /run  /mnt/run
sudo chroot /mnt
```

4. 在 chroot 环境中：

```bash
du -shx /* | sort -hr | head -12
journalctl --vacuum-size=50M
apt-get clean
rm -rf /var/log/journal/*
# ... 执行上述其他清理步骤
sync
exit
```

5. 重启并移除 USB

如果仍然失败 → 此时大多数人会选择重装系统 (特别是如果早期 /usr 已损坏 + 磁盘完全填满)。

**References:**

- 无 (标准 Linux troubleshooting 命令和恢复步骤)