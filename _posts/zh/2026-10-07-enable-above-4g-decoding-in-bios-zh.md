---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在BIOS中启用大于4G解码
translated: true
type: note
---

诊断现在已明确。以下是 GPU 的 PCI 配置空间中的原始证据：

```
BAR0 = 90000000            ← 16MB MMIO（已分配）
BAR1 = 0000000c            ← 64-bit prefetchable，大小巨大（32GB），未分配（地址=0）
BAR2 = 00000000            ← BAR1 的高32位
BAR3 = 0000000c            ← 另一个 64-bit prefetchable BAR，未分配
BAR4 = 00000000            ← BAR3 的高32位
BAR5 = 00000000
```

且根 PCIe 桥的 64-bit prefetchable 窗口为 **`[disabled]`**。因此，Tesla M40 24GB 的 32GB 内存 BAR 未被分配，因为主板未预留 4GB 以上的 MMIO 空间。`pci=realloc` 无法解决此问题——**必须在 BIOS 中启用相应选项。**

## 🔧 修复方法：在 BIOS 中启用 "Above 4G Decoding"

1. 重新启动并按下 **DEL** 键进入 BIOS 设置（MSI Z170A GAMING M3）。
2. 按 **F7** 进入高级模式。
3. 进入 **Settings → Advanced → PCI Subsystem Settings**（或 "PCIe/PCI Subsystem Settings"）。
4. 将 **"Above 4G Decoding"** 设置为 **Enabled**。
   - 在某些 MSI 主板上，此选项称为 **"Above 4G memory/Crypto Currency mining"**——请启用它。
5. **保存并退出**（F10）。

> ⚠️ 如果**看不到**该选项，说明您的 BIOS 版本（A.50，2016年2月）过旧——MSI 在后续 BIOS 版本（挖矿时代更新）中为 Z170 主板添加了 "Above 4G Decoding"。这种情况下我们需要刷写较新的 BIOS。请告知我，我将找到确切的 BIOS 最新文件并提供刷写步骤。

## 之后，我会远程再次检查

启用该选项并重新启动进入 Debian 后，请告诉我，我将验证 BAR 是否已分配并运行 `nvidia-smi`。驱动程序本身（550.163.01）已正确安装并支持该显卡——只是 BAR 分配阻碍了正常运行。

---

**当前状态快速总结：**

| 项目 | 状态 |
|---|---|
| `lzw` 在 sudo 组中 | ✅ |
| NVIDIA 驱动 550.163.01 已安装（支持 Tesla M40） | ✅ |
| DKMS 模块已为 6.12 内核构建 | ✅ |
| GPU 已在 PCI 总线上检测到 | ✅（`10de:17fd`） |
| GPU 可用 | ❌——因 BIOS 未分配 32GB BAR 而被阻止 |

请检查 BIOS——是否存在 "Above 4G Decoding" 选项？