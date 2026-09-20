---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI问题与修复总结
translated: true
type: note
---

**问题：** ReBarUEFI 常见问题与修复 Wiki 页面摘要。

**回答：**

以下是关于 [ReBarUEFI](https://github.com/xCuri0/ReBarUEFI)（一个在不受支持的 UEFI 系统上启用 Resizable BAR 的项目）页面中所列已知问题及其修复的结构化摘要。

---

### 当前已知问题（无修复）

- 许多 **Haswell** 系统缺少 4G 解码选项，因此无法实现全尺寸 ReBarUEFI。
- **LGA1151** 在某些主板上存在显示输出问题（解决方法：将显示器连接到 iGPU）。
- **ASRock Z170 K4/D3**：启用 4G 解码后，Intel SATA 控制器停止工作。
- **32GB BAR** 在 Sandy/Ivy Bridge 上即使有 32GB 内存也无法工作，不过链接的问题中有一个解决方法。

---

### GPU 特定修复

| 问题 | 修复 |
| --- | --- |
| NVIDIA RTX 30 系列 ReBAR 无法工作 | 通过 NVIDIA 官方指南更新 VBIOS |
| AMD GPU — 禁用 CSM 后黑屏 | 恢复原始 VBIOS（或应用 GOP 更新） |
| AMD 不受支持的 GPU — 启用 ReBAR | 使用 Radeon-ID 驱动程序或应用 `.reg` 文件 |
| RX 5600 XT 无法从睡眠中恢复 | 将 BAR 大小设置为 **1GB** 或更低 |
| Intel Arc GPU 无法工作 | 将主图形适配器设置为 **PCI Express** |
| 驱动程序显示 ReBAR 已禁用（GPU-Z 显示工作中） | 重新安装 GPU 驱动程序（通常不需要 DDU） |

---

### 启动 / POST 问题

| 问题 | 修复 |
| --- | --- |
| 禁用 CSM 后 Windows 无法启动 | 将 MBR 磁盘转换为 UEFI GPT |
| LGA1151 在使用 4GB+ BAR 时无法 POST | 将显示器连接到 iGPU |
| 操作系统加载前无视频输出 | 禁用 **Above 4G Decoding Patch** 选项 |
| 无法 POST / 超频失效 | 改用 **MMTool** 而非 UEFITool 重新按照指南操作（UEFITool 会损坏某些固件） |
| 无法启动 Windows / 设备管理器中 GPU 错误 | 按照 **DSDT Patching** 指南操作 |
| HEDT 系统在 VRAM ≥16GB 或多 GPU 时无法启动 | 在 BIOS 中增加 `MMIOH Size` / `MMIO High Granularity Size` |

---

### 软件 / NVRAM 问题

| 问题 | 修复 |
| --- | --- |
| `ReBarState` 显示“Failed to write UEFI variable” | 以管理员身份运行；通过 UEFIPatch 应用 `NvramSmi` 或 `NvramSmiDxe` 补丁 |
| 启用 ReBAR 后游戏崩溃 | 增加 **页面文件大小** |
| Ryzen 上的卡顿 | 已知固件错误；尝试将 `Above 4GB MMIO Limit` 设置为 `512GB` |
| 启用 4G 解码后 HEDT 上的卡顿 | 将 `MMIOH Base` 设置为 `256GB` 或更高 |

---

### 常见问题

- **所需 BAR 大小**：你只需要一个能容纳所有 VRAM 的 BAR 大小——例如，8GB 足够 8GB VRAM。
- **无 4G 解码**：你可能只能使用 1GB BAR。减小 TOLUD 选项可能允许最多 2GB。Linux 用户可以使用 DSDT 补丁来在没有 4G 解码的情况下实现完整 ReBAR。
- **Memory Remap ≠ 4G 解码**：将 Memory Remap 保留在默认设置。
- **GPU-Z 报告**：GPU-Z 常常错误报告 4G 解码和 CSM 值，因此不能完全信任。

---

参考：

- [ReBarUEFI Common Issues and Fixes Wiki](https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-(and-fixes))
