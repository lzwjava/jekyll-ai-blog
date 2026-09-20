---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺失UUID导致紧急模式
translated: true
type: note
---

问题：为什么这台 Linux 机器卡在紧急模式？

答案：屏幕上显示**启动配置引用的两个文件系统 UUID 已不存在**：

```text
警告：/dev/disk/by-uuid/2B6A-70B5 不存在
警告：/dev/disk/by-uuid/bba45be2-f8c5-4745-8438-f62d853a3198 不存在
```

这几乎可以肯定意味着 `/etc/fstab` 中包含 Linux 当前无法找到的磁盘或分区条目。

### 怎么办

按 **Enter** 进入维护 shell，然后运行：

```bash
lsblk -f
blkid
cat /etc/fstab
```

重要的对比是：

```text
/etc/fstab          <-- Linux 期望的 UUID
blkid / lsblk -f    <-- 实际存在的 UUID
```

你可能会发现类似这样的内容：

```fstab
UUID=2B6A-70B5    /some/mount    ...
UUID=bba45be2-...  /another/mount ...
```

但这些 UUID 不在 `blkid` 输出中。

### 如果这些只是旧的或丢失的磁盘

备份 `fstab`：

```bash
cp /etc/fstab /etc/fstab.bak
```

然后编辑它：

```bash
nano /etc/fstab
```

通过在行首添加 `#` 注释掉过时的行：

```fstab
# UUID=2B6A-70B5 ...
# UUID=bba45be2-...
```

然后测试：

```bash
mount -a
```

如果命令无错误返回：

```bash
reboot
```

### 如果你*期望*这些磁盘存在

先不要删除 `fstab` 条目。检查：

```bash
lsblk -o NAME,SIZE,FSTYPE,UUID,MOUNTPOINTS
```

如果物理磁盘完全缺失，可能的原因包括：

* 外接驱动器未插好
* 驱动器故障或无法识别
* BIOS 或虚拟机磁盘配置更改
* 分区被重新创建，导致 UUID 改变

如果磁盘存在但有**不同的 UUID**，请更新 `/etc/fstab` 中的 UUID。

**关键点：** 这主要不是内核故障——而是因为 `/etc/fstab` 中指定的必需文件系统无法找到，导致启动过程拒绝继续。

如果你粘贴这三个命令的输出：

```bash
lsblk -f
blkid
cat /etc/fstab
```

我可以告诉你**具体需要修改哪些 `fstab` 行**。