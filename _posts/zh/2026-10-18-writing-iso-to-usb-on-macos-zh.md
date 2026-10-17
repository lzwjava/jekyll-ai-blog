---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上将 ISO 写入 USB
translated: true
type: note
---

ISO（756M）可以正常放到这个4GB的U盘上。命令如下：

```bash
# 1. 卸载磁盘（不要弹出——dd需要原始访问权限）
diskutil unmountDisk /dev/disk14

# 2. 将ISO写入原始设备节点（rdisk = 比disk快得多）
sudo dd if=/Users/lzwjava/Downloads/debian-13.7.0-amd64-netinst.iso of=/dev/rdisk14 bs=4m status=progress

# 3. 刷新缓冲区，然后弹出
sync
diskutil eject /dev/disk14
```

关键点：

- **`/dev/rdisk14`**（原始设备）——用`/dev/disk14`会慢得让人抓狂；`rdisk`会绕过块缓存。
- **`bs=4m`**——4MB块大小以提高速度；`status=progress`显示实时进度。
- **`sudo`**——写入原始设备需要管理员权限；系统会提示你输入密码。
- 这会**覆盖整个U盘**——之前的FAT32“USB”卷会消失，被Debian安装程序镜像替代。这对于制作可启动U盘来说是预期且正确的。

完成后，这个U盘可以在任何x86-64机器（UEFI或传统BIOS）上启动Debian 13.7 netinst安装程序。

需要我帮你执行吗？我可以运行卸载 + dd + sync这些步骤——注意它会在终端中提示你输入sudo密码。