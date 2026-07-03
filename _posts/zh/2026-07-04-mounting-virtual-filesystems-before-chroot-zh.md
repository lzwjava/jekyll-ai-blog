---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挂载虚拟文件系统后再执行chroot
translated: true
type: note
---

**问题：** 在我之前的文章 [Recover from a Failed Linux Kernel Boot](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en) 的恢复流程中，为什么在执行 `chroot /mnt` 之前要运行这五个挂载命令？每个命令实际做了什么？

**答案：**

这五条命令在 `/mnt` 内部构建了一个你已安装系统*功能完整*的副本，使得 `chroot /mnt` 的行为就像你实际启动了那个系统一样。其中一条命令挂载你的真实磁盘；另外四条则将 **live USB 的内核提供的虚拟文件系统** 嫁接进去。

## 核心洞察：chroot 改变的是文件系统视图，而非内核

`chroot` 是一个非常简单的系统调用——它只改变进程所见的 `/` 路径。在 `chroot /mnt` 之后，当程序打开 `/proc/mounts` 时，内核会将其解析为真实文件系统上的 `/mnt/proc/mounts`。但你仍然在运行 **live USB 的内核**。磁盘上损坏的内核只是文件，并未执行。

因此问题是：你的磁盘根文件系统中包含 `/dev`、`/proc`、`/sys`、`/run` 这些 *空目录*——它们总是在运行时由内核填充，永远不会存储在磁盘上。直接 chroot 到一个裸磁盘挂载点，会得到一个看似正常但实则又聋又瞎的系统：没有设备、没有进程信息、没有内核接口。

## 逐行解释

```bash
sudo mount /dev/nvme0n1pX /mnt
```

普通的块设备挂载。内核读取该 NVMe 分区上的文件系统（ext4/btrfs），并将其挂载到 `/mnt`。现在 `/mnt/boot`、`/mnt/etc`、`/mnt/usr` 就是你的真实已安装系统。（在 Fedora 上使用 btrfs 默认设置时，可能需要 `-o subvol=root`，并且需要单独执行 `mount /dev/nvme0n1pY /mnt/boot` 和 `/mnt/boot/efi` —— 下文会详细说明。）

```bash
sudo mount --bind /dev /mnt/dev
```

**绑定挂载（bind mount）** 使一个已有的目录树在第二个位置可见——相同的 inode，无需复制，类似于目录树在 VFS 层的硬链接。live 系统上的 `/dev` 是由内核 + udev 填充的 `devtmpfs`，包含设备节点：`/dev/nvme0n1`、`/dev/null`、`/dev/urandom`、`/dev/tty`。

chroot 环境中的工具为什么需要它：

- `grub2-install` 必须打开 `/dev/nvme0n1` 以写入 EFI 分区并探测磁盘布局
- `dracut` 读取 `/dev/urandom`，探测块设备以决定将哪些存储驱动包含进 initramfs
- 任何启动 shell 的操作都需要 `/dev/tty`、`/dev/pts`

没有它：会出现 `grub2-install: error: cannot find a device for /boot/efi`。

```bash
sudo mount --bind /proc /mnt/proc
```

`procfs` 是内核的进程/状态接口，以文件形式呈现。这里的关键消费者是 **`/proc/mounts`**——`grub2-mkconfig` 和 `dracut` 读取它来了解挂载情况以及根设备是什么。`/proc/cmdline`、`/proc/filesystems`、`/proc/cpuinfo` 也会被查询。没有它，`grub2-mkconfig` 通常会报错：`/usr/sbin/grub2-probe: error: failed to get canonical path`。

```bash
sudo mount --bind /sys /mnt/sys
```

`sysfs` 是内核的设备模型树——每个设备、驱动和总线都以目录层级呈现。两个关键使用者：

- **EFI 变量** 位于 `/sys/firmware/efi/efivars`。在 UEFI 系统上，`grub2-install` 调用 `efibootmgr`，通过该接口将启动条目写入 NVRAM。没有 `/sys` → GRUB 被安装到磁盘上，但 Mac 的固件无法感知到它——这正是文章中提到的“启动条目可能损坏”的故障模式。
- `dracut` 遍历 `/sys/block/` 和 `/sys/devices/` 来检测你的硬件需要哪些驱动（这正是它知道要包含 NVMe 驱动的方式——而该模块的缺失很可能导致你的自定义内核无法启动）。

```bash
sudo mount --bind /run /mnt/run
```

一个用于运行时状态的 `tmpfs`。在 Fedora 上的主要原因：udev 的设备数据库位于 `/run/udev`，`dracut` / `lvm` / `cryptsetup` 会查询它以解析设备属性和 UUID。此外，Fedora 将 `/etc/resolv.conf` 符号链接到 `/run/systemd/resolve/...`，因此绑定 `/run` 可以让你的 chroot 拥有 **可用的 DNS**——执行 `dnf reinstall kernel-core` 时需要它。

## 心智模型

```
Live USB 内核（运行中）          磁盘（仅文件）
        │                                │
        ├── /dev  ─── bind ──►  /mnt/dev │
        ├── /proc ─── bind ──►  /mnt/proc├── 你损坏的 Fedora
        ├── /sys  ─── bind ──►  /mnt/sys │
        └── /run  ─── bind ──►  /mnt/run │
                                         ▼
                  chroot /mnt = 在 USB 的内核上
                  “启动”磁盘的用户空间
```

你正在进行一次“弗兰肯斯坦式”启动：live 内核提供硬件访问，磁盘提供用户空间（`dnf`、`dracut`、`grub2-install`、你的配置）。这就是整个技巧。

## 两个实用改进

**1. 对 `/dev` 和 `/sys` 使用 `--rbind` + `--make-rslave`**（Arch 的 `arch-chroot` 就是这样做的）：

```bash
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc /proc /mnt/proc
sudo mount --bind /run   /mnt/run
```

普通的 `--bind` 只嫁接顶层挂载，会遗漏子挂载点，比如 `/dev/pts`（伪终端——某些脚本没有它会挂起）和 `/sys/firmware/efi/efivars`。`--rbind` 递归绑定整个子树；`--make-rslave` 防止 chroot 内部的卸载操作传播回 live 会话并导致其崩溃。

**2. 在 chroot 之前不要忘记挂载启动分区。** Fedora 将它们分离，而两者对于内核和 GRUB 修复都很重要：

```bash
# 先检查分区布局
lsblk -f
sudo mount /dev/nvme0n1pY /mnt/boot        # ext4 /boot，存放 vmlinuz + initramfs
sudo mount /dev/nvme0n1p1 /mnt/boot/efi    # FAT32 ESP，存放 grubx64.efi
```

如果 `/boot` 没有挂载，`dnf reinstall kernel` 和 `dracut --regenerate-all` 会将内核写入根分区上的一个目录，而固件永远看不到它——修复“成功”，但机器仍然无法启动。这是该恢复流程中最常见的无声故障之一。

或者完全跳过这些繁琐步骤：`systemd-nspawn -D /mnt`（从 live USB 运行）会自动为你设置所有这些，并提供一个更干净的容器式 chroot 环境。

**参考：**

- [Recover from a Failed Linux Kernel Boot — lzwjava](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en)
- [`mount(8)` — 绑定挂载语义](https://man7.org/linux/man-pages/man8/mount.8.html)
- [arch-chroot 源码——规范的 rbind/rslave 设置](https://gitlab.archlinux.org/archlinux/arch-install-scripts/-/blob/master/arch-chroot.in)