---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挂载并chroot Fedora分区
translated: true
type: note
---

**问题：** 我的 Fedora 启动 U 盘上的 `lsblk` 显示 `nvme0n1p1`（600M）、`nvme0n1p2`（2G）、`nvme0n1p3`（231.2G，已挂载到 `/mnt/sysroot`）。针对这种分区布局，具体的挂载和 chroot 命令是什么？

**答案：**

你的分区布局是标准的 Fedora 方案：

| 分区 | 大小 | 角色 |
| --- | --- | --- |
| `nvme0n1p1` | 600M | EFI 系统分区（FAT32） |
| `nvme0n1p2` | 2G | `/boot`（ext4）—— 内核和 initramfs 在此 |
| `nvme0n1p3` | 231.2G | 根分区，几乎肯定是 **btrfs**，包含 `root` 和 `home` 子卷 |

需要注意两点：p3 已被挂载到 `/mnt/sysroot`；如果是 btrfs，它可能挂载在 *顶层*（显示 `root/` 和 `home/` 目录），而不是 `root` 子卷。先检查一下：

```bash
lsblk -f /dev/nvme0n1        # 确认文件系统类型
ls /mnt/sysroot              # 如果只看到 "root home" 目录 → 顶层 btrfs 挂载
```

最干净的方式——从 `/mnt` 重新开始：

```bash
sudo umount -R /mnt/sysroot 2>/dev/null

# root 子卷（Fedora btrfs 默认）
sudo mount -o subvol=root /dev/nvme0n1p3 /mnt
# 如果 lsblk -f 显示 ext4：则用 sudo mount /dev/nvme0n1p3 /mnt

sudo mount /dev/nvme0n1p2 /mnt/boot
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# 虚拟文件系统（使用 rbind 以同时挂载 /dev/pts 和 efivars）
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc proc  /mnt/proc
sudo mount --bind  /run  /mnt/run

sudo chroot /mnt /bin/bash
```

进入 chroot 后进行修复前的检查：

```bash
ls /boot                          # 应显示 vmlinuz-*、initramfs-*
ls /boot/efi/EFI/fedora           # grubx64.efi、grub.cfg 存根
ls /sys/firmware/efi/efivars | head   # 非空 → efibootmgr 可用
cat /etc/resolv.conf && ping -c1 pypi.org   # 用于 dnf 的 DNS
```

然后执行实际修复（沿用之前的流程）：

```bash
dnf reinstall -y kernel-core kernel-modules
dracut --regenerate-all --force
grub2-mkconfig -o /boot/grub2/grub.cfg
```

关于你的输出有两个补充说明：`nvme0n1` 和 `nvme0n2` 在磁盘层级显示 `0B` 是已知的 Apple NVMe 特性（多命名空间控制器报告）——分区大小才是关键，而且它们是正确的。`zram0 [SWAP]` 只是当前 live 会话的压缩内存交换，无需理会。

**参考资料：**

- [Fedora 默认分区（btrfs 子卷）](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/install/Installing_Using_Anaconda/#sect-installation-gui-manual-partitioning-recommended)
- [从失败的 Linux 内核启动中恢复 — lzwjava](https://lzwjava.github.io/recover-from-a-failed-linux-kernel-boot-en)
