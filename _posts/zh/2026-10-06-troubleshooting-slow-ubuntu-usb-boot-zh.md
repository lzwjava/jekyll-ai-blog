---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu USB启动缓慢故障排查
translated: true
type: note
---

**为什么我的 Ubuntu USB 启动缓慢 / 显示所有这些错误？**

回答：截图显示了**两个独立的问题**，而主要问题出在你的 USB / live Ubuntu 环境上。

### 1. 你的 Windows NTFS 磁盘没有正常关机

你看到了：

```text
The disk contains an unclean file system (0, 0).
Metadata kept in Windows cache, refused to mount.
Falling back to read-only mount because the NTFS partition is in an unsafe state.
Please resume and shutdown Windows fully (no hibernation or fast restarting).
```

这意味着 Ubuntu 检测到了一个 NTFS 分区，而 Windows 将其留在了**休眠 / 快速启动 / 未正常关机**的状态。

如果那是你的 Windows SSD/HDD，请先启动 Windows 一次，然后执行：

```powershell
shutdown /s /t 0
```

然后再启动 Ubuntu USB。

如有必要，也请禁用 Windows 快速启动。

---

### 2. 更重要的是：你的 Ubuntu live USB 的持久化分区有错误

这一行很关键：

```text
EXT4-fs (sdb4): Could not load journal inode
mount: mounting /dev/disk/by-label/writable on /log-persistence failed: Invalid argument
```

你的 USB 显然是 `/dev/sdb`，并且：

```text
/dev/sdb4
```

是 Ubuntu live USB 的**可写 / 持久化分区**。

Ubuntu 试图将其挂载到：

```text
/log-persistence
```

但无法加载 ext4 文件系统的日志。

这通常意味着**文件系统损坏**，或持久化分区创建不当/已损坏。

所以如果你是用持久化方式创建的 Ubuntu USB，这很可能才是真正的问题所在。

---

### 3. 为什么卡在 `Get: ... file:/cdrom ...`？

在底部：

```text
Ign:1 file:/cdrom resolute InRelease
Get:2 file:/cdrom resolute Release
Get:3 file:/cdrom resolute Release.gpg
Get:4 file:/cdrom resolute/restricted amd64 Packages
Get:5 file:/cdrom resolute/main amd64 Packages
```

这实际上对于 live Ubuntu 系统来说是**正常的**。

`file:/cdrom` 的意思是：

> “将 USB 中挂载的 Ubuntu 安装 ISO 用作 APT 软件包源。”

它并不是从互联网下载这些软件包，而是**从 USB** 读取软件包元数据。

如果你的 USB 速度慢或存在 I/O 问题，这可能会极其缓慢。

---

### 有趣的线索

你之前说过：

> Ubuntu USB 进度条跑了半个小时

结合这张截图，我强烈怀疑问题出在 **USB 驱动器 / USB 文件系统**，而不是你的主板或 SSD。

你看到了：

```text
/dev/sdb4
EXT4 journal error
```

并且系统还在读取：

```text
file:/cdrom
```

所以启动环境可能花了大量时间进行 USB I/O / 恢复。

### 我会怎么做

如果你不需要在这个 USB 上保存任何内容：

```text
1. 重新创建 Ubuntu USB
2. 如果可能，换一个不同的 U 盘
3. 最初不要启用持久化
4. 启动它
5. 检查 Ubuntu 是否恢复正常/变快
```

然后在 Ubuntu 内执行：

```bash
lsblk -f
sudo dmesg | grep -Ei 'usb|sdb|error|ext4|I/O'
```

第二条命令特别有用。如果你看到类似这样的信息：

```text
I/O error
Buffer I/O error
reset SuperSpeed USB device
blk_update_request
EXT4-fs error
```

那么我们就能判断**U 盘本身是否在失效**，还是持久化文件系统只是创建得不对。

**我暂时不会怪罪你的 SSD。** 截图更明确地指向了 `/dev/sdb4` / Ubuntu USB 环境。
