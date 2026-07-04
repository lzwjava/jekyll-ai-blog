---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挂载并修复Fedora Btrfs启动
translated: true
type: note
---

**问题：** `lsblk -f` 确认 `nvme0n1p1` = FAT32 (ESP)，`nvme0n1p2` = ext4（`/boot`），`nvme0n1p3` = btrfs 标签为 `fedora`。本次会话中 `/mnt/sysroot` 不存在。接下来该怎么办？

**回答：**

很好——文件系统检查消除了所有歧义。本次启动会话从未挂载任何东西（之前的 `/mnt/sysroot` 来自其他会话，可能是救援模式启动），因此 `/mnt` 是空闲的。直接执行完整序列：

```bash
# 1. 根目录 — btrfs，因此挂载 'root' 子卷，而不是顶层
sudo mount -o subvol=root,compress=zstd:1 /dev/nvme0n1p3 /mnt

# 确认你得到了实际的 OS 树，而不是 "root/ home/" 文件夹：
ls /mnt        # 预期：bin boot etc usr var ...

# 2. 启动链
sudo mount /dev/nvme0n1p2 /mnt/boot
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# 3. 虚拟文件系统
sudo mount --rbind /dev  /mnt/dev  && sudo mount --make-rslave /mnt/dev
sudo mount --rbind /sys  /mnt/sys  && sudo mount --make-rslave /mnt/sys
sudo mount -t proc proc  /mnt/proc
sudo mount --bind  /run  /mnt/run

# 4. 进入 chroot
sudo chroot /mnt /bin/bash
```

如果第1步因 `subvol=root` 未找到而失败，请列出实际存在的子卷：

```bash
sudo mount /dev/nvme0n1p3 /mnt          # 顶层挂载
sudo btrfs subvolume list /mnt          # 查找 'root' 和 'home'（Fedora 默认）
sudo umount /mnt                        # 然后使用正确的子卷名称重新挂载
```

在 chroot 内部，先验证再修复：

```bash
ls /boot                            # vmlinuz-*、initramfs-* 文件是否存在？
ls /boot/efi/EFI/fedora             # grubx64.efi 是否存在？
cat /etc/fedora-release             # 确认你在正确的根目录中
ping -c1 pypi.org                   # 通过绑定的 /run 进行 DNS 检查
```

然后进行修复：

```bash
dnf reinstall -y kernel-core kernel-modules kernel-modules-core
dracut --regenerate-all --force
grub2-mkconfig -o /boot/grub2/grub.cfg
exit
```

在重启前干净地卸载：

```bash
sudo umount -R /mnt
sudo reboot
```

在 chroot 环境中值得做的一项诊断（因为你的原始问题是自定义内核）：执行 `ls /boot` 并比较 `initramfs-*` 文件的大小。自定义内核的 initramfs 如果明显小于标准内核，通常意味着 dracut 省略了存储驱动（NVMe/btrfs 模块）——这是启动时挂起的典型原因。这能告诉你修复方法是使用正确的模块配置执行 `dracut --force --kver <你的内核版本>`，而不是完全重装。

**参考：**

- [Fedora btrfs 布局 — 子卷 `root` 和 `home`](https://fedoraproject.org/wiki/Changes/BtrfsByDefault)
- [dracut(8) — 重新生成 initramfs](https://man7.org/linux/man-pages/man8/dracut.8.html)