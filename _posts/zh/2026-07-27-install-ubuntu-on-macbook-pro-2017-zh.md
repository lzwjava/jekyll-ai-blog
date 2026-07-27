---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在2017款MacBook Pro上安装Ubuntu
translated: true
type: note
---

问题：**如何在 2017 款 MacBook Pro 上安装 Ubuntu 24.04 / 26.04？**

答案：

2017 款 MacBook Pro 是 **Intel Mac**，因此可以运行 Ubuntu。最简单的路径是**仅安装 Ubuntu（清除 macOS）** 或双系统启动。Ubuntu 24.04 LTS 是更安全的选择；Ubuntu 26.04 更新，可能需要更多修复。Ubuntu 的安装程序支持在 Intel Mac 上通过按住 **Option（⌥）** 启动并选择 **EFI Boot** 从 USB 引导。（[Ubuntu 文档][1]）

## 1. 下载 Ubuntu ISO

推荐：

* Ubuntu 24.04 LTS：

  * `ubuntu-24.04.x-desktop-amd64.iso`

Ubuntu 26.04（如果您的目标日期已发布）：

* `ubuntu-26.04-desktop-amd64.iso`

您的 2017 款 MacBook Pro 需要 **amd64/x86_64**，而非 ARM。

---

## 2. 制作可启动 USB

在 Ubuntu/Linux 中：

```bash
lsblk

# 示例 USB = /dev/sdb
sudo dd if=ubuntu-24.04.x-desktop-amd64.iso \
  of=/dev/sdX \
  bs=4M \
  status=progress \
  oflag=sync
```

或使用 Ventoy：

```bash
sudo ./Ventoy2Disk.sh -i /dev/sdX
```

将 ISO 复制到 Ventoy USB。

---

## 3. 允许从外部启动（如果被阻止）

重启 Mac：

```
Command (⌘) + R
```

进入恢复模式。

打开：

```
实用工具
 → 启动安全实用工具
 → 允许从外部介质启动
```

部分带有 Apple 安全芯片的 MacBook 型号需要此步骤。（[YouTube][2]）

---

## 4. 启动 Ubuntu USB

插入 USB。

开机并按住：

```
Option (⌥)
```

您应该看到：

```
EFI Boot
```

选择它。

（[Ubuntu][3]）

---

## 5. 安装 Ubuntu

选择：

```
安装 Ubuntu
```

若要完全替换：

```
擦除磁盘并安装 Ubuntu
```

若要双系统启动：

1. 先打开 macOS 磁盘工具
2. 缩小 APFS 分区
3. 留出空闲空间
4. Ubuntu 安装程序中选择：

   ```
   其他选项
   ```

5. 创建：

```
/boot/efi   512MB   FAT32

/           ext4    剩余空间
```

对于简单的单操作系统安装，Ubuntu 推荐“擦除磁盘并安装 Ubuntu”。（[Ubuntu 文档][1]）

---

## 6. 安装后：2017 款 MacBook Pro 修复

2017 款 MacBook Pro 有一些 Apple 专用硬件：

### WiFi

检查：

```bash
lspci | grep -i network
```

安装 Broadcom 固件：

```bash
sudo apt update
sudo apt install bcmwl-kernel-source
```

---

### 触控栏

检查：

```bash
lsusb | grep Apple
```

部分用户需要额外的内核/支持包。Ubuntu 26.04 报告在某些 2017 型号上支持有所改进，但 WiFi/音频/触控栏可能仍需要手动修复。（[Reddit][4]）

---

### 音频

检查：

```bash
sudo dmesg | grep -i audio
```

---

### 触控板

通常自动工作，使用：

```bash
libinput
```

测试：

```bash
sudo libinput list-devices
```

---

## 我对 2017 款 MBP 的建议

使用：

```
Ubuntu 24.04 LTS
+
最新 HWE 内核
```

因为：

* 稳定
* 长期支持
* 社区修复更好
* 驱动调试更简单

之后再升级到 26.04。

参考：

* Ubuntu 桌面安装指南（[Ubuntu 文档][1]）
* Ubuntu 在 MacBook Pro 2017-2019 上的 wiki（[Ubuntu Wiki][5]）
* Ubuntu 试用/安装 USB 启动指南（[Ubuntu][3]）

[1]: https://documentation.ubuntu.com/desktop/en/24.04/tutorial/install-ubuntu-desktop/?utm_source=chatgpt.com "安装 Ubuntu 桌面 - Ubuntu 桌面文档"
[2]: https://www.youtube.com/watch?v=qjfBP4UYx9c&utm_source=chatgpt.com "如何在 Mac 上双系统启动 Ubuntu 24.04 和 macOS || 在 Mac 上安装新版 Ubuntu（仅限 Intel）- YouTube"
[3]: https://ubuntu.com/desktop/docs/en/latest/tutorial/try-ubuntu-desktop/?utm_source=chatgpt.com "试用 Ubuntu 桌面 - Ubuntu 桌面文档"
[4]: https://www.reddit.com/r/linux_on_mac/comments/1v02681/macbook_pro_2017_macbookpro142_on_ubuntu_2604/?utm_source=chatgpt.com "MacBook Pro 2017 (MacBookPro14,2) 在 Ubuntu 26.04 上——Wi-Fi、触控栏和音频可正常工作"
[5]: https://wiki.ubuntu.com/Apple/MacBook%20Pro%2015%22%202017-2019?utm_source=chatgpt.com "Apple/MacBook Pro 15\" 2017-2019 - Ubuntu Wiki"
