---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过UEFI补丁启用可调整大小的BAR
translated: true
type: note
---

本项目可在不官方支持**可调整大小 BAR** 的主板/BIOS 上启用该功能。以下是详细的使用指南：

## 总览

该工具包含 3 个主要部分：
1. **ReBarDxe** — 注入到 BIOS 固件中的 UEFI DXE 驱动程序
2. **ReBarState** — 用于在运行时配置 BAR 大小的 Windows/Linux 工具
3. **UEFIPatch** — 用于修复 BIOS 限制（如 BAR 大小限制、MMIO 空间问题等）的补丁

---

## 步骤 1：向 BIOS 添加 DXE 驱动程序

您需要使用 **UEFITool** 或 **AMI CBFS** 等工具将 `ReBarDxe` 插入到主板 UEFI 固件镜像中（详细步骤请参见 [wiki 指南](https://github.com/xCuri0/ReBarUEFI/wiki/Adding-FFS-module)）。

如果您想从源码构建：

```bash
# 首先克隆 EDK2，然后在其中：
git clone https://github.com/xCuri0/ReBarUEFI.git
cd ReBarUEFI/ReBarDxe
python buildffs.py
```

## 步骤 2：应用 UEFI 补丁（可选但推荐）

大多数 BIOS 固件都带有人为限制。请使用 **UEFIPatch**（v0.28.0+）配合 `UEFIPatch/patches.txt` 中的补丁进行修复：

| 补丁 | 目的 |
|------|------|
| `<4GB BAR size limit removal` | Sandy/Ivy Bridge |
| `<16GB / <64GB BAR size limit removal` | 各类芯片组 |
| `Prevent 64-bit BAR downgrade` | Haswell/Broadwell |
| `Increase MMIO space` | Skylake/KBL/CFL, Haswell/Broadwell, Sandy/Ivy Bridge |
| `NVRAM whitelist unlock` | 修复 ReBarState 中的 `GetLastError: 5` 错误 |
| `USB 3 fix` | 修复启用 Above 4G Decoding 后的 USB 端口问题（Ivy/Haswell/Broadwell） |

应用方式如下：

```bash
UEFIPatch your_bios.rom UEFIPatch/patches.txt
```

> **注意**：`X79 Above 4G Decoding fix` 补丁（位于 `UEFIPatch/patch.txt` 中，已注释掉）可能也与 X79 平台相关。

## 步骤 3：刷入修改后的 BIOS

使用您的厂商刷新工具或硬件编程器将修改后的 BIOS 刷入主板。

## 步骤 4：通过 ReBarState 配置

使用修改后的固件启动后：

- 在 BIOS 中启用 **Above 4G Decoding**
- 禁用 **CSM**（兼容性支持模块）
- 启动到 Windows/Linux 并运行 **ReBarState**

### Windows
从 [Releases](https://github.com/xCuri0/ReBarUEFI/releases) 下载。以管理员身份运行：

```
ReBarState.exe
```

### Linux
使用 CMake 构建：

```bash
cd ReBarState
mkdir build && cd build
cmake ..
make
sudo ./ReBarState
```

### 选择 BAR 大小
- **32** = 无限制（如果稳定推荐使用）
- 如果 32 不可用，可使用较小的值（2、4、8、16 GB）

> ⚠️ **如果系统无法启动**：清除 CMOS。可调整大小的 BAR 设置将处于禁用状态。

---

## 额外说明

该工具还在 `tools/` 中提供了辅助脚本：

- **`uuidconv.py`** — 将 UUID 转换为 C 结构体格式（例如，用于驱动程序中使用的 GUID）

有关详细信息，请参阅[项目 wiki](https://github.com/xCuri0/ReBarUEFI/wiki)。