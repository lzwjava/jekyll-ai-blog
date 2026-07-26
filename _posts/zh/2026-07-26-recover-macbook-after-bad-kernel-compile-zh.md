---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内核编译失败后恢复MacBook
translated: true
type: note
---

问题：MacBook Pro 2017 运行 Ubuntu，编译 Linux 内核后无法启动。如何恢复？

答案：

是的，这是常见情况。**MacBook Pro 2017 (Intel)** 可以运行 Ubuntu，但手动编译内核后，错误的内核配置或缺少 Apple 专用驱动可能导致无法启动。

好消息是：你的数据很可能还在。你主要需要启动一个旧内核或修复 GRUB。

## 1. 首先尝试 GRUB 恢复

开机时立即按住：

```
Option (⌥) 键
```

你会看到 Apple 的启动选择器。

选择：

```
EFI Boot
```

然后在 GRUB 中：

按：

```
Esc
```

或按住：

```
Shift
```

你应该会看到：

```
Ubuntu
Ubuntu 高级选项
```

选择：

```
Ubuntu 高级选项
```

然后选择之前的内核：

示例：

```
Ubuntu, with Linux 6.8.0-xx-generic
Ubuntu, with Linux 6.8.0-xx-generic (recovery mode)
Ubuntu, with Linux 6.6.x
```

启动旧内核。

---

## 2. 如果能启动旧内核

检查已安装的内核：

```bash
dpkg --list | grep linux-image
```

示例：

```
linux-image-6.8.0-40-generic
linux-image-6.8.0-custom
```

移除损坏的内核：

```bash
sudo apt remove linux-image-6.8.0-custom
sudo update-grub
```

---

## 3. 如果没有内核能启动：使用 Ubuntu 启动 U 盘

从 U 盘启动：

```
开机
按住 Option (⌥)
选择 EFI Boot
```

挂载你的 Ubuntu 分区：

```bash
sudo fdisk -l
```

示例：

```
/dev/nvme0n1p2   Linux filesystem
```

挂载：

```bash
sudo mount /dev/nvme0n1p2 /mnt
```

挂载 EFI：

```bash
sudo mount /dev/nvme0n1p1 /mnt/boot/efi
```

进入你的系统：

```bash
sudo chroot /mnt
```

然后：

```bash
update-grub
```

或重新安装内核：

```bash
apt install --reinstall linux-image-generic linux-headers-generic
```

退出：

```bash
exit
sudo reboot
```

---

## 4. 为什么编译内核会破坏 MacBook Pro 启动

MacBook Pro 2017 硬件需要多个内核选项：

重要：

```
CONFIG_EFI=y
CONFIG_EFI_STUB=y

CONFIG_NVME_CORE=y
CONFIG_NVME=y

CONFIG_HID_APPLE=y
CONFIG_BCM5974=y

CONFIG_DRM_AMDGPU=y   (如果是 Radeon Pro 型号)
CONFIG_DRM_I915=y     (Intel 显卡)
```

常见错误：

### 缺少 EFI 支持

Mac 通过 EFI 启动：

```
Mac EFI firmware
        |
        v
Linux EFI stub
        |
        v
Kernel
```

如果：

```
CONFIG_EFI_STUB=n
```

Mac 无法启动内核。

---

### 缺少 NVMe 驱动

SSD 需要：

```
CONFIG_NVME_CORE
CONFIG_BLK_DEV_NVME
```

否则：

```
Kernel starts
        |
        X
cannot find root filesystem
```

---

### 错误的 initramfs

安装自定义内核后：

```bash
sudo update-initramfs -c -k <kernel-version>
sudo update-grub
```

没有 initramfs，挂载 `/` 前所需的驱动可能会缺失。

---

## 5. 为将来编译内核做准备

在 Ubuntu 上，从当前配置开始：

```bash
cp /boot/config-$(uname -r) .config
```

然后：

```bash
make olddefconfig
make -j$(nproc)
sudo make modules_install
sudo make install
sudo update-grub
```

这样会保留 Apple 所需的选项。

---

关键问题是：**你现在启动时具体发生了什么？**

示例：

1. 立即黑屏？
2. GRUB 出现但内核提示 `unable to mount root fs`？
3. 内核 panic？
4. 卡在 Apple 标志？
5. 进入 `initramfs` shell？

另外请告诉我确切的 MacBook Pro 2017 型号：

* 13 英寸仅 Intel？
* 15 英寸带 Radeon Pro GPU？
* Ubuntu 版本？
* 你编译的内核版本？
