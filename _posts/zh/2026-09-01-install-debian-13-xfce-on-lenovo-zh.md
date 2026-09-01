---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在联想上安装Debian 13 XFCE
translated: true
type: note
---

问题：如何从 `debian-live-13.6.0-amd64-xfce.iso` 在旧款 Lenovo L-IG41M3 机器上安装 Debian 13 XFCE？

回答：**是的。这个 ISO 镜像对于这台机器来说是个不错的选择**，前提是 Celeron CPU 是 64 位的。Debian 的 Live Xfce 映像专门设计用于从 USB 启动，让你测试硬件，然后使用 Calamares 将 Debian 安装到硬盘上。([Debian][1])

### 1. 制作可启动 USB

由于你很可能是在 Mac 上准备 USB，请插入一个 **8 GB 或更大的 USB 闪存盘**。

在 macOS 上：

```bash
diskutil list
```

找到 USB 设备，例如：

```text
/dev/disk4
```

卸载它：

```bash
diskutil unmountDisk /dev/disk4
```

然后写入 ISO：

```bash
sudo dd if=debian-live-13.6.0-amd64-xfce.iso \
  of=/dev/rdisk4 \
  bs=4m \
  status=progress
```

然后：

```bash
diskutil eject /dev/disk4
```

**操作 `/dev/disk4` 时要格外小心。** `dd` 命令会销毁目标磁盘。Debian 明确建议将混合映像写入 **整个 USB 设备**，而不是像 `/dev/disk4s1` 这样的分区。([Debian][2])

如果你愿意，也可以使用图形界面的 USB 写入工具，但 `dd` 是理解底层操作的最简洁方式。

---

### 2. 将 USB 插入 Lenovo 机器

连接：

```text
USB 闪存盘
   ↓
L-IG41M3 USB 端口
```

启动电脑。

立即开始反复按 BIOS/启动菜单键。

在 Lenovo 机器上，通常为：

```text
F12
```

或者有时是：

```text
F2
Delete
```

你需要进入 **启动菜单 (Boot Menu)**。

选择类似这样的选项：

```text
USB HDD
USB Storage
UEFI: <USB 名称>
```

对于这台非常古老的 G41 机器，**极有可能是传统 BIOS 启动**，所以即使没有看到 UEFI 选项也不必担心。

---

### 3. Debian Live 应该能够启动

你会看到一个类似这样的 Debian 菜单：

```text
Debian GNU/Linux Live

Debian GNU/Linux Live
Debian GNU/Linux Live (failsafe)
...
```

选择：

```text
Debian GNU/Linux Live
```

它会在完全不碰硬盘的情况下，直接从 USB 启动 XFCE。这正是 Live 映像的主要用途之一。([Debian][1])

最终你会进入 XFCE 桌面。

**这对于你的硬件维修实验来说非常棒**，因为可以在安装任何东西之前测试机器。

打开一个终端：

```bash
lscpu
free -h
lsblk
lspci
```

查看 GPU 插槽：

```bash
lspci -vv
```

---

### 4. 确认 Celeron CPU 确实是 64 位的

这一点很重要，因为你下载的是：

```text
amd64
```

`amd64` 并**不**意味着你需要 AMD CPU。它表示 **64 位 x86** 架构，Intel 的 64 位 CPU 也能与之兼容。Debian 将 amd64 描述为适用于 64 位 PC 兼容系统的架构。([Debian][3])

运行：

```bash
lscpu | grep -E 'Architecture|Model name|CPU MHz'
```

你希望看到：

```text
Architecture: x86_64
```

如果看到：

```text
Architecture: i686
```

那么 CPU 是 32 位的，这个特定的 ISO 将无法使用。

---

### 5. 将其安装到硬盘

进入 Debian XFCE 后，寻找：

```text
Install Debian
```

或者 **Calamares 安装程序**。

Debian 的 Live 映像专门包含了 Calamares，用于将 Live 系统安装到硬盘上。([Debian][1])

基本流程如下：

```text
Debian Live USB
       │
       ▼
   XFCE 桌面
       │
       ▼
 安装 Debian
       │
       ▼
 选择磁盘
       │
       ▼
 分区磁盘
       │
       ▼
 安装引导加载程序
       │
       ▼
 重启
       │
       ▼
 移除 USB
       │
       ▼
 Debian XFCE 在 HDD/SSD 上
```

如果机器使用的是旧式 HDD，我**强烈建议换成一块廉价 SATA SSD**。

即使是这样的配置：

```text
G41 + Celeron + 4 GB
        +
     SATA SSD
```

其体验也会比以下配置好得多：

```text
G41 + Celeron + 4 GB
        +
    7200 RPM HDD
```

### 我建议先做的一件事

**不要立即安装。**

启动 Live USB 并运行：

```bash
lscpu
free -h
lsblk
lspci
lspci -nn
```

然后把输出结果发给我。

特别是：

```bash
lscpu
lspci -nn
```

我可以准确地告诉你，你那块特定的 **L-IG41M3** 主板拥有什么 CPU、芯片组、PCIe 控制器、GPU 插槽、网络控制器等，以及 Debian 13 在这上面是否能顺利运行。

[1]: https://www.debian.org/CD//live/?utm_source=chatgpt.com "Debian -- Live install images"
[2]: https://www.debian.org/releases/bookworm/amd64/install.en.pdf?utm_source=chatgpt.com "Debian GNU/Linux Installation Guide"
[3]: https://www.debian.org/CD/?utm_source=chatgpt.com "Debian installation media for USB, CD, DVD"