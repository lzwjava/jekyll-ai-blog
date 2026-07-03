---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从Linux内核启动失败中恢复
translated: true
type: note
---

问题：我在MacBook Pro上构建了一个自定义Linux内核，重启Fedora后系统无法启动——该怎么办？

回答：

这通常意味着系统无法引导新内核（引导项丢失、initramfs损坏或EFI/GRUB问题）。别担心——你的数据很可能仍然完好。目标是启动救援环境并修复引导加载程序/内核。

---

## 1. 首先检查：是完全死机了，还是仅仅无法引导Linux？

尝试以下操作：

* 按住**电源键约10秒**完全关机
* 再次开机
* 立即按住**Option（⌥）键**（Intel Mac）或按住电源键并保持启动选项（Apple Silicon 不同）

如果你看到：

* **“EFI Boot” / “Fedora”** → 选择它
* 没有任何与Linux相关的内容 → 引导项可能已损坏

---

## 2. 从Fedora Live U盘启动（最可靠的修复方法）

你可能需要另一台电脑来制作U盘：

* 下载Fedora Workstation ISO
* 使用以下工具刻录：

  * Rufus（Windows）
  * balenaEtcher（Mac/Linux）

启动MacBook：

* 启动时按住**Option（⌥）**
* 选择**EFI USB / Fedora Live**

---

## 3. 进入Live环境后：修复系统

打开终端并执行：

### 找到你的Linux根分区

```bash
lsblk
```

寻找类似这样的内容：

* `/dev/nvme0n1pX`（根分区）

---

### 挂载系统

```bash
sudo mount /dev/nvme0n1pX /mnt
sudo mount --bind /dev /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys /mnt/sys
sudo mount --bind /run /mnt/run
```

---

### 进入系统（chroot）

```bash
sudo chroot /mnt
```

---

## 4. 修复内核/引导问题

### 选项A：重新安装内核（安全）

```bash
dnf reinstall kernel-core kernel-modules kernel
```

### 选项B：重建initramfs

```bash
dracut --regenerate-all --force
```

---

## 5. 重新安装GRUB（在Mac EFI上很重要）

对于UEFI系统：

```bash
grub2-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=fedora
grub2-mkconfig -o /boot/grub2/grub.cfg
```

---

## 6. 退出并重启

```bash
exit
reboot
```

重启时移除U盘。

---

## 7. 如果你编译了自己的内核（很可能是原因）

你的构建显示：

> 自定义内核 + “构建成功”

但常见问题：

### 可能的失败原因

* 内核未复制到 `/boot`
* 缺少 `initramfs`
* GRUB未更新
* 内核缺少模块（尤其是存储驱动！）
* EFI引导项未指向新内核

---

## 8. 快速恢复技巧（如果GRUB仍然可用）

在GRUB菜单中：

* 按 `e`
* 手动引导旧内核

如果旧内核能工作 → 是你的自定义内核损坏，而非系统本身。

---

## 9. 最坏情况（仍然可以修复）

如果所有方法都无效：

* 从Live U盘启动
* 备份 `/home`
* 在不触及home分区的情况下重新安装Fedora

---

## 如果你需要下一步的帮助

请告诉我：

* Intel Mac 还是 Apple Silicon？
* 你是否还能看到GRUB菜单？
* 启动时具体发生了什么（黑屏/苹果标志/EFI shell）？

我可以据此给出精确的恢复路径。
