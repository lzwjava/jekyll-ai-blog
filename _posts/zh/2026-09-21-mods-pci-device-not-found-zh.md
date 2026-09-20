---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS PCI设备未找到
translated: true
type: note
---

**问题：** 为什么 MODS（GPU 诊断工具）显示“未找到 PCI 设备”错误？

**回答：**

屏幕显示 MODS GPU 测试（`gputest.js`）失败，并出现 **错误代码 `0x220` — 未找到 PCI 设备**。原因如下：

**根本原因**

关键错误信息为：
```
ERROR: SBIOS assigned incorrect BAR1 – offset 0x0, size 0x0
```

BIOS/UEFI 未能正确为 GPU 分配 **基地址寄存器（BAR）**。BAR1 的大小为 `0x0`，这意味着系统无法将 GPU 映射到 PCI 地址空间 — 因此 MODS 根本无法在 PCI 总线上找到该 GPU 设备。

**可能原因**

1. **未安装独立 GPU** — 该系统（Intel i5-4460，Haswell）可能仅配有集成显卡。MODS 正在寻找一个不存在的 NVIDIA GPU。
2. **GPU 物理接触不良** — 如果已安装 GPU 卡，其 PCIe 插槽连接可能存在问题。
3. **BIOS 中禁用了 Above 4G Decoding（4G 以上解码）** — 某些 GPU 需要启用此选项才能正确分配 BAR。
4. **BIOS 错误或固件过时** — SBIOS 日期为 `12/09/2016`，已相当陈旧。
5. **PCIe 插槽或显卡故障** — GPU 可能已损坏，或插槽已损坏。

**检查要点**

- 确认实际安装了独立 NVIDIA GPU
- 重新插拔 GPU 以确保 PCIe 插槽连接良好
- 在 BIOS 设置中启用 **Above 4G Decoding（4G 以上解码）**
- 如有可能，更新 BIOS 固件
- 在其他机器或插槽上测试该 GPU

**参考资料：**
- [NVIDIA MODS 文档](https://developer.nvidia.com/mods)
- [PCI BAR（基地址寄存器）详解](https://wiki.osdev.org/PCI#Base_Address_Registers)
- [Linux 上的 PCIe BAR 分配问题](https://www.kernel.org/doc/html/latest/PCI/pci-error-recovery.html)