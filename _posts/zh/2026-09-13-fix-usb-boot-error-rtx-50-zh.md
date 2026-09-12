---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复RTX 50 USB启动错误
translated: true
type: note
---

**问题：** 在USB磁盘上运行50系列GPU测试程序时，如何修复启动错误？

**回答：**

在TinyLinux USB启动时出现错误 `Partition with root filesystem not found` 对于**较新硬件（RTX 50系列）** 非常常见，因为该USB通常是为旧系统创建的。以下是修复方法：

---

**根本原因**
RTX 50系列系统通常使用：
- **仅NVMe** 存储（无SATA），导致设备名称不匹配
- **USB 3.x控制器**，旧TinyLinux内核无法快速识别
- **安全启动** 阻止未签名的内核

---

**修复选项（按顺序尝试）：**

**① 增加启动延迟（最简单）**
在GRUB/启动菜单中，按 `e` 编辑启动参数并添加：
```
rootdelay=10
```
这给内核更多时间来检测USB驱动器。

**② 修复 `root=` 参数**
在GRUB菜单中，按 `e` 并将root行改为使用你的USB设备。在紧急 Shell 中，首先找到它：
```sh
lsblk
# 查找你的USB，例如 /dev/sdb1 或 /dev/sda1
```
然后重启，在GRUB界面按 `e`，找到包含 `root=` 的行，将其改为：
```
root=/dev/sdb1   # 或 lsblk 显示的其他设备
```

**③ 在BIOS中禁用安全启动**
- 重启 → 进入BIOS（通常按 `Del` 或 `F2`）
- 找到 **Secure Boot** → 设置为 **Disabled**
- 保存并重新尝试从USB启动

**④ 使用正确设置重新制作USB**
ISO镜像可能需要重新正确写入：
```sh
# 在Linux/Mac上 — 将 /dev/sdX 替换为你的USB驱动器
sudo dd if=tinylinux.iso of=/dev/sdX bs=4M status=progress oflag=sync

# 或在Windows上使用Rufus：
# - 分区方案：MBR（用于BIOS）或GPT（用于UEFI）
# - 文件系统：FAT32
```

**⑤ 在BIOS中启用CSM/Legacy Boot**
- 进入BIOS → 找到 **CSM** 或 **Legacy Boot**
- 启用它，然后再次尝试从USB启动

---

**你正在使用哪个GPU测试程序？**
如果是特定工具如 **OCCT**、**FurMark** 或厂商特定的RTX 50系列诊断程序，请告知我——有些工具提供了专门针对新硬件更新的ISO镜像。

---

**参考：**
- [TinyLinux启动问题 – kernel.org](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
- [Rufus USB制作指南](https://rufus.ie/en/)
- [NVIDIA RTX 50系列Linux支持](https://www.nvidia.com/en-us/drivers/unix/)