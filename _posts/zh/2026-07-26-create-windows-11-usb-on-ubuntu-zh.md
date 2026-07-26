---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu上创建Windows 11 USB
translated: true
type: note
---

问题：**在 Linux/Ubuntu 中，如何从 ISO 创建 Windows 11 可安装启动 U 盘？**

回答：

在 Ubuntu 上，对于 Windows 11 最可靠的方法是 **Ventoy**。与 `dd` 不同，它能正确处理 Windows ISO 文件（Windows ISO 通常包含大于 4GB 的文件以及特殊的 UEFI 要求）。

## 方法 1（推荐）：Ventoy

### 1. 下载 Ventoy

```bash
wget https://github.com/ventoy/Ventoy/releases/latest/download/ventoy-1.0.xx-linux.tar.gz
```

解压：

```bash
tar xzf ventoy-*.tar.gz
cd ventoy-*
```

### 2. 找到你的 U 盘设备

插入 U 盘：

```bash
lsblk
```

示例：

```
sda      500G  SSD
sdb       32G  USB
```

假设 U 盘为 `/dev/sdb`。

⚠️ 此操作会清空 U 盘。

### 3. 安装 Ventoy

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdb
```

确认操作。

### 4. 复制 Windows 11 ISO

Ventoy 完成后，U 盘会显示为普通磁盘。

直接复制即可：

```bash
cp Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/
```

安全弹出：

```bash
sync
```

从 U 盘启动 → Ventoy 菜单 → 选择 ISO → Windows 安装程序启动。

---

## 方法 2：WoeUSB-ng（Windows 专用 U 盘写入工具）

安装：

```bash
sudo apt update
sudo apt install woeusb-ng
```

创建 U 盘：

```bash
sudo woeusb \
  --device \
  Win11_25H2_English_x64_v2.iso \
  /dev/sdb
```

---

## 方法 3：手动 FAT32 + 拆分 install.wim

如果 BIOS 比较挑剔（某些联想小新机型）时有用。

### 给 U 盘分区

```bash
sudo parted /dev/sdb --script mklabel gpt
sudo parted /dev/sdb --script mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdb1
```

挂载 ISO：

```bash
sudo mount -o loop Win11.iso /mnt/iso
```

挂载 U 盘：

```bash
sudo mount /dev/sdb1 /mnt/usb
```

复制除 `install.wim` 之外的所有文件：

```bash
rsync -av --exclude=sources/install.wim /mnt/iso/ /mnt/usb/
```

安装 wimlib：

```bash
sudo apt install wimtools
```

拆分 Windows 镜像：

```bash
wimsplit \
 /mnt/iso/sources/install.wim \
 /mnt/usb/sources/install.swm \
 3800
```

结果：

```
sources/
 ├── boot.wim
 ├── install.swm
 ├── install2.swm
```

Windows 安装程序能够识别 `.swm` 文件。

---

## 避免使用此方法

**不要**对 Windows 11 执行以下操作：

```bash
sudo dd if=Win11.iso of=/dev/sdb bs=4M
```

`dd` 对 Linux ISO 效果很好，但 Windows ISO 经常失败，因为：

* FAT32 无法存储大于 4GB 的 `install.wim`
* UEFI 启动布局不同
* 某些固件不接受混合 ISO 布局

---

针对你的联想小新情况，我会建议：

1. **优先使用 Ventoy**（最快）
2. 如果联想 BIOS 拒绝启动 → **手动 FAT32 + wimlib 拆分**
3. 如果 Windows 安装程序看不到 SSD → 检查 Intel VMD/RST 驱动问题

参考资料：

* Ventoy 项目：[https://www.ventoy.net/](https://www.ventoy.net/)
* WoeUSB-ng：[https://github.com/WoeUSB/WoeUSB-ng](https://github.com/WoeUSB/WoeUSB-ng)
* wimlib：[https://wimlib.net/](https://wimlib.net/)