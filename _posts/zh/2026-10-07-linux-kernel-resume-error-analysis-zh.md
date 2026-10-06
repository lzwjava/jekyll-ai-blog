---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux内核挂起错误分析
translated: true
type: note
---

**问题：** 这些 Linux 内核启动/恢复日志表明了什么，存在哪些错误？

**答案：**

这是一个在**挂起/恢复周期（S3 睡眠状态）**期间捕获的 Linux 内核日志。以下是发生的事件和值得注意的错误的详细说明。

## 正常恢复序列

- CPU 1–3 离线，然后在 S3 恢复后重新上线
- NVIDIA HDA 控制器重新启用
- OOM 杀手启用，PCI 资源重新分配
- SATA 链路先降速再恢复

## 错误与问题

**1. xHCI USB 错误（严重）**

```
xhci_hcd 0000:03:00.0: xHC error in resume, USBSTS 0x401, Reinit
usb usb3/usb4: root hub lost power or was reset
```

USB 主机控制器在恢复时遇到错误，不得不重新初始化。USB 设备可能需要重新枚举。

**2. PCI 桥资源分配失败（严重）**

```
pci 0000:05:00.0: bridge window [mem ...]: can't assign; no space
pci 0000:05:00.0: bridge window [mem ...]: failed to assign
```

PCI 桥（总线 06）在恢复后无法分配内存/IO 窗口。这可能会影响该总线上的 PCIe 设备。

**3. ACPI BIOS 错误（中等）**

```
ACPI BIOS Error: Could not resolve symbol [\_SB.PCI0.SAT0.PRT3._GTF.DSSP], AE_NOT_FOUND
Aborting method \_SB.PCI0.SAT0.PRT3._GTF due to previous error (AE_NOT_FOUND)
```

ACPI 固件引用了 ACPI 表中不存在的方法/对象（`DSSP`）。这是主板 BIOS 的**固件错误**，但通常不致命。

**4. SATA 链路波动**
大多数 SATA 端口在挂起时关闭并在恢复后重新连接，但这些错误有时会伴随恢复后磁盘检测问题。

## 汇总表

| 问题 | 严重程度 | 可能影响 |
| --- | --- | --- |
| xHCI 恢复错误 | 中等 | USB 设备可能断开 |
| PCI 桥无空间 | 中等 | PCIe 设备可能失灵 |
| ACPI BIOS 符号未找到 | 低—中等 | BIOS 错误，通常无害 |
| SATA 链路关闭/恢复 | 低 | S3 挂起期间正常 |

## 建议

1. **更新主板 BIOS/UEFI** — 修复 ACPI `AE_NOT_FOUND` 错误
2. **在恢复后检查 USB 设备** 是否有断开情况
3. 如果 PCIe 设备在恢复后行为异常，可在内核启动参数中添加 `pci=realloc`
4. 下次恢复后运行 `dmesg | grep -i error` 以跟踪反复出现的问题

---

**参考：**

- [Linux Kernel PCI Resource Allocation](https://www.kernel.org/doc/html/latest/PCI/pci.html)
- [ACPI in Linux - Common Errors](https://www.kernel.org/doc/html/latest/firmware-guide/acpi/index.html)
- [xHCI USB Resume Issues](https://www.kernel.org/doc/html/latest/usb/index.html)
