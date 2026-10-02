---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PCI资源修复位置详解
translated: true
type: note
---

是的——这个仓库确实包含了修复方案，但需要明确其具体**位置**。针对 Z170 主板上“PCI Insufficient PCI Resources Detected”错误的修复**不在** `ReBarDxe` 驱动中，而是在 `UEFIPatch/` 目录下的二进制固件补丁中。

## 修复方案所在位置

`/mnt/data/ReBarUEFI/UEFIPatch/patches.txt`

这个文件包含了基于模式匹配的补丁，应用于 AMI Aptio V 固件模块（`PciHostBridge` 和 `PciBus`），直接消除了导致该 POST 错误的人为 MMIO/BAR 限制。

## 针对 Z170（Skylake）的补丁

来自 `patches.txt`：

| 补丁 | 模块 (GUID) | 修复内容 |
| --- | --- | --- |
| `Replace 64GB MMIO region with complete use of 512GB physical address space (Skylake/Kaby Lake/Coffee Lake)` | PciHostBridge `8D6756B9-...` | 将 MMIO 孔径从默认的 16–32GB（或 64GB）窗口扩展到完整的 39 位 / 512GB 范围 |
| `Remove <64GB BAR size limit (Skylake/Kaby Lake/Coffee Lake)` | PciBus `3C1DE39F-...` | 移除固件的 64GB BAR 上限 |
| `Don't downgrade 64-bit BARs to 32-bit` | PciBus `3C1DE39F-...` | 阻止固件将大容量 64-bit BAR 强行压缩到狭窄的 32-bit / 4GB 窗口——这是“Insufficient PCI Resources”最常见直接原因 |
| `Remove 4GB limit for PciRootBridgeIo.Mem` | PciHostBridge `8D6756B9-...` | 移除根桥内存窗口的 4GB 解码限制 |
| `Remove 4GB limit for CpuIo2` | Runtime `CBC59C4A-...` | 移除 CPU I/O 的 4GB 限制 |

README 中的“Working patches”部分确认了 Skylake 专属补丁：

> Increase MMIO space from 16-32GB to full usage of 512GB/39-bit range (Skylake/Kaby Lake/Coffee Lake)

## 这与您的错误如何对应

AMI 的“Insufficient PCI Resources Detected”消息正是 `PciBus`/`PciHostBridge` 在 BAR 分配失败时报告的信息（`NotifyPhase(EfiPciHostBridgeAllocateResources)` 路径返回 `EFI_OUT_OF_RESOURCES`——您可以在 `ReBarDxe/include/PciHostBridgeResourceAllocation.h` 中看到该返回值的明确记录）。当 M40/P100 暴露出一个多 GB 的 BAR1 时，Z170 的默认固件：

1. 限制了 MMIO 区域（16–32GB 或 64GB），和/或
2. 将 64-bit BAR 降级为 32-bit，和/或
3. 将 BAR 大小限制在 64GB 以下

……因此分配空间耗尽，您便看到了这个错误。上述补丁正好解除了这三个限制。

## 重要注意事项

- `ReBarDxe/ReBar.c` **仅仅是 ReBAR 使能器**——它钩住 `PreprocessController` 并编程设置 ReBAR 能力。它本身**不**修复资源分配问题，实际上如果您请求的 BAR 大小超出了未修补固件所能分配的范围，它甚至可能**加剧**问题。
- 这些补丁基于 GUID + 字节模式。只有当 MSI 使用了具有匹配字节模式的 AMI Aptio V 标准模块时，它们才能干净地应用。您需要使用 UEFIPatch 来应用它们，并且必须确认模式匹配成功（并且根据 README 的要求，填充文件未被更改）。
- MMIO 扩展仅在 **Above 4G Decoding 已启用** 时生效（该选项可能在您的主板上被隐藏——请参考 README/wiki 中关于“Enabling hidden 4G decoding”的内容）。
- **CSM 必须关闭**，某些主板还需要 **DSDT 补丁**（Skylake MMIO 补丁注释未标记此项，但 Sandy/Ivy 和 Haswell/Broadwell 的对应补丁有标记——建议在您的主板上核实）。

## 结论

**是的**，`UEFIPatch/patches.txt` 包含针对此类 Z170 PCI 资源分配失败问题的确切修复方案——特别是 Skylake 的“512GB MMIO space”补丁，加上“<64GB BAR limit removal”和“don't downgrade 64-bit BARs”补丁。`ReBarDxe` 模块本身仅负责 ReBAR 部分，而非资源修复。
