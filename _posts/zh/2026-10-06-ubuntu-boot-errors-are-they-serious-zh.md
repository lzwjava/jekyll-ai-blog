---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu启动错误：它们严重吗？
translated: true
type: note
---

**这个 Ubuntu 安装/启动画面中发生了什么？这些错误严重吗？**

**这里有几条不同的信息。大多数是警告，但有两条值得注意。**

### 1. GPT/PMBR 不匹配

你有：

```text
GPT PMBR size mismatch (12732371 != 30719999) will be corrected by write.
The backup GPT table is not on the end of the device.
The backup GPT table is corrupt, but the primary appears OK, so that will be used.
```

这意味着 USB/磁盘的 **GPT 分区元数据与实际的磁盘大小不匹配**。

例如：

```text
GPT 认为磁盘 ≈ 12.7 GB
实际磁盘 ≈ 30.7 GB
```

这通常发生在：

* 一个镜像被写入到不同大小的 USB 驱动器
* 磁盘被克隆过
* 磁盘大小被改变
* GPT 备份头部没有被移动到磁盘的物理末尾

关键的一行是：

```text
primary appears OK, so that will be used.
```

所以 **仅凭这一点并不意味着 USB 已损坏**。安装程序通常可以自动修复它。

---

### 2. 更值得关注：EXT4 日志错误

你有：

```text
EXT4-fs (sda4): Could not load journal inode
```

这意味着 Linux 试图将 `/dev/sda4` 挂载为 ext4 文件系统，但 **无法加载其日志（journal）**。

如果 `/dev/sda4` 是你尝试安装 Ubuntu 的分区，这可能表示：

* 文件系统损坏
* 上次安装被中断
* 文件系统元数据损坏
* 磁盘可能正在故障

如果你是全新安装，并且 **不需要该磁盘上的任何数据**，最简单的解决方案通常是完全重新创建分区/文件系统，而不是尝试保留旧的 ext4 文件系统。

---

### 3. 这可能是你看到长时间停顿的原因

在底部：

```text
Get:1 file:/cdrom ...
Get:2 file:/cdrom ...
Get:3 file:/cdrom ...
Get:4 file:/cdrom ...
Get:5 file:/cdrom ...
```

这实际上是 Ubuntu 的软件包系统在从 **安装 USB / live CD** 读取软件包：

```text
file:/cdrom
```

所以它不一定是从互联网下载。

之前的：

```text
A connection to the bus can't be made
```

和

```text
fuse: device /dev/fuse not found
```

在这种情况通常 **不构成恐慌的理由**。

---

## 我会怎么做

如果这是你的 **旧/测试机器，并且你不需要 `/dev/sda` 上的数据**，我会停止尝试保留现有的文件系统。

启动 Ubuntu 安装程序，选择：

**清除磁盘并安装 Ubuntu**

这会干净地重新创建分区表/文件系统。

如果你特别想先诊断磁盘，可以从 live 终端运行：

```bash
lsblk -f
sudo fdisk -l
sudo smartctl -a /dev/sda
```

对于 ext4 分区：

```bash
sudo e2fsck -f /dev/sda4
```

**不要在已挂载的文件系统上运行 `e2fsck`。**

### 关键区别

| 消息 | 含义 | 严重？ |
| ------------------------------------------ | ------------------------------------ | ------------------------------ |
| GPT PMBR mismatch                          | GPT 元数据与磁盘大小不匹配 | 通常可修复 |
| Backup GPT not at end                      | GPT 需要重新定位/修复 | 通常可修复 |
| Backup GPT corrupt, primary OK             | 备份分区表损坏 | 如果主分区表有效则可修复 |
| `EXT4-fs ... Could not load journal inode` | ext4 文件系统问题 | **值得修复** |
| `file:/cdrom` package messages             | 安装程序读取 USB 介质 | 正常 |
| `/dev/fuse not found`                      | 此环境中 FUSE 不可用 | 通常无关紧要 |

**如果进度条在大约 30 分钟内没有任何变化，我不会认为这是正常的。** 鉴于 GPT 和 ext4 错误同时出现，我会先验证 USB 和目标磁盘是否健康，而不是无限期等待。