---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复GPU初始化失败指南
translated: true
type: note
---

问题：**如何修复截图中显示的 GPU 初始化失败？**

回答：

**TSC 警告不是问题所在**。实际失败信息是：

```text
PCI chip ID 0x00001006 (DID=1287) is an unrecognized GPU
Possibly you need a newer MODS package.

There are no active devices to test.
Error 220: Gpu.Initialize pci device not found
Error Code = 00000220
```

`DID=1287` 是关键信息：**PCI 设备 ID `1287` 对应 NVIDIA GK208B / GeForce GT 730**（与 NVIDIA 供应商 ID `10de` 配合使用）。（[blog.jklug.work][1]）

因此，我会按以下顺序进行调试：

### 1. 检查 Linux 实际识别到的内容

在 Shell 中运行：

```bash
lspci -nn | grep -Ei 'vga|3d|display|nvidia'
```

然后：

```bash
lspci -nn -s 01:00.0
```

将 `01:00.0` 替换为实际的 GPU PCI 地址。

期望的输出类似：

```text
01:00.0 VGA compatible controller [0300]:
NVIDIA Corporation GK208B [GeForce GT 730] [10de:1287]
```

其中关键部分是：

```text
[10de:1287]
```

`10de` = NVIDIA，`1287` = GK208B/GT 730。（[blog.jklug.work][1]）

### 2. 如果 Linux 报告 `10de:1287`

那么 **你的 GPU 对 PCIe 可见**，这几乎可以确定是 **MODS 兼容性/版本问题**，而非 GPU 损坏。

屏幕本身已提示：

```text
Possibly you need a newer MODS package.
```

获取一个明确支持你所测试 GPU 代的 MODS 版本。

同时检查：

```bash
lspci -nnk -s 01:00.0
```

以及：

```bash
dmesg | grep -Ei 'nvrm|nouveau|pci|vfio|gpu'
```

如果 `nouveau`、`nvidia` 或 `vfio-pci` 已经占用了该设备，也会干扰 MODS。

例如：

```bash
lspci -nnk -s 01:00.0
```

如果看到：

```text
Kernel driver in use: nouveau
```

或：

```text
Kernel driver in use: nvidia
```

则在运行 MODS 之前需要处理这一情况。

### 3. 如果 Linux 报告 `1006:1287`

那就更有意思了。

`1006` **并非 NVIDIA 的供应商 ID**；NVIDIA 是 `10de`。PCI ID 数据库将 `1006` 识别为 Reply Group，而非 NVIDIA。（[GitHub][2]）

这种情况下，暂时不要调整 TSC 设置。我们需要确定 PCI 供应商 ID 为什么显示不正确。

运行：

```bash
lspci -nn
```

以及：

```bash
lspci -xxxx -s <GPU_BDF>
```

另外：

```bash
cat /sys/bus/pci/devices/<GPU_BDF>/vendor
cat /sys/bus/pci/devices/<GPU_BDF>/device
```

对于正常的 GT 730，这些值应为：

```text
0x10de
0x1287
```

### 4. 暂时忽略 TSC 警告

以下信息：

```text
NURM: Warning - TSC is unstable on this CPU!
```

是独立的 Linux 时钟源问题。Linux 有明确的 `tsc=` 内核参数用于处理不稳定的 TSC，但更改这些参数不会让丢失的 PCI GPU 出现。（[Kernel.org][3]）

因此，**不要从 `tsc=reliable` 或 BIOS 时钟设置入手**。

---

### 我最可能的猜测

根据：

```text
DID=1287
/home/GT610
MODS
Error 220
```

我首先会假设 **MODS 版本过旧，无法识别已安装的 NVIDIA GPU**，尤其是在自定义的 TinyLinux/MODS 启动环境中。

请运行以下三条命令并粘贴输出：

```bash
lspci -nn | grep -Ei 'vga|3d|display|nvidia'

lspci -nnk | grep -A4 -Ei 'vga|3d|display|nvidia'

dmesg | grep -Ei 'nvrm|nouveau|vfio|pci' | tail -100
```

有了这些信息，我可以判断问题是 **MODS 版本不匹配、PCI ID 错误、驱动占用、VFIO 直通，还是实际的 PCIe/GPU 硬件故障**。

参考资料：

* [NVIDIA 10de:1287 PCI/GPU 识别示例](https://blog.jklug.work/posts/proxmox/?utm_source=chatgpt.com)
* [Linux 内核 TSC 参数](https://kernel.org/doc/html/next/admin-guide/kernel-parameters.html?utm_source=chatgpt.com)
* [PCI 供应商 ID 数据库](https://github.com/evanphx/ulysses/blob/master/src/pci_db.hpp?utm_source=chatgpt.com)

[1]: https://blog.jklug.work/posts/proxmox/?utm_source=chatgpt.com "Proxmox Hypervisor - GPU and Disk Passthrough · blog.jklug.work"
[2]: https://github.com/evanphx/ulysses/blob/master/src/pci_db.hpp?utm_source=chatgpt.com "ulysses/src/pci_db.hpp at master · evanphx/ulysses · GitHub"
[3]: https://kernel.org/doc/html/next/admin-guide/kernel-parameters.html?utm_source=chatgpt.com "The kernel’s command-line parameters — The Linux Kernel documentation"
