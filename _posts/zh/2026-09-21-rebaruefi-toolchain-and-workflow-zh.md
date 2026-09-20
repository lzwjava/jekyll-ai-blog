---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI工具链与工作流程
translated: true
type: note
---

我们现在已经构建了工具链的两个部分：

```
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.ffs   ← 注入 BIOS 的 DXE 驱动
ReBarUEFI/ReBarState/build/ReBarState           ← 配置工具（写入 NVRAM 变量）
```

## ReBarUEFI 的实际作用（根据 README）

`ReBarDxe.ffs` 是一个 **UEFI DXE 驱动**。当放置在固件的 DXE 卷中时，它会在每次启动时运行，并：

1. 钩住 `PciHostBridgeResourceAllocationProtocol` 的 `PreprocessController`
2. 检查 GPU 是否声明支持 Resizable BAR
3. 从名为 `ReBarState` 的 NVRAM 变量（GUID `A3C5B77A-C88F-4A93-BF1C-4A92A32C65CE`）中设置 BAR 大小
4. 随后 `PciBus` 枚举 PCI 设备，并据此分配新的（更大的）BAR

所以完整路径是：**注入驱动 → 刷写修改后的 BIOS → 启用 4G 解码 + 禁用 CSM → 通过 ReBarState 设置 BAR 大小 → 重启**。

## 分步工作流程（来自 README + wiki）

**1. 获取主板 BIOS 镜像** — 从制造商官网下载最新版本（`.cap`/`.rom`/`.bin`）。

**2. 使用 [UEFITool 0.28 (non-NE)](https://github.com/LongSoft/UEFITool/releases/tag/0.28.0) 将 `ReBarDxe.ffs` 插入 DXE 卷**：

- 打开 BIOS，`File → Search`，以 header-only GUID 搜索 `3C1DE39F-D207-408A-AACC-731CFB7F1DD7`（**PciBus** 模块）以定位正确的卷
- 滚动到该卷的最后一个模块 → 右键 → **Insert after** → 选择 `ReBarDxe.ffs`
- 保存镜像
- （如果 UEFITool 无法使用，MMTool 为备选方案）

**3. 应用 UEFIPatch 补丁** — 大多数消费级主板存在 64 位 BAR 的 bug，需要修复：

- 下载 [UEFIPatch](https://github.com/LongSoft/UEFITool/releases/tag/0.28.0)
- 将 `UEFIPatch/patches.txt`（来自仓库）和您的 BIOS 放在同一文件夹，运行 `UEFIPatch <biosfile>`
- 这会移除 `<4GB/<16GB/<64GB` 的 BAR 限制，扩展 MMIO 空间，防止 64 位 BAR 被降级等。输出为 `<biosfile>.patched`
- 如有需要，可额外添加平台特定补丁：`HswAbove4G.txt`（Haswell/Broadwell 的 4G 解码，*此平台必需*）、`IvyUSB3.txt`/`HswUSB3.txt`/`BdwUSB3.txt`（BIOS 中的 USB3 修复），以及 X79 修复（在 `patches.txt` 中取消注释）
- **注意 pad 文件损坏 bug**（主要是 ASUS）——在刷写前用 UEFITool 比较 pad 文件

**4. 使用主板刷写工具/编程器刷写修改后的 BIOS**。⚠️ 这是危险步骤——刷写失败可能导致主板变砖。

**5. 在 BIOS 设置中：启用 Above 4G Decoding，禁用 CSM**。

**6. 启动操作系统，以 root 身份运行 ReBarState**：

```bash
sudo ./ReBarUEFI/ReBarState/build/ReBarState
# 然后输入：32   （无限大——大多数情况下有效）
```

`32` 表示无限大；较小的值设置 `2^x` MB（例如 `10` = 1 GB，`11` = 2 GB）。如果不确定 BIOS 能否处理大 BAR，建议先尝试一个高于 256 MB 的小值。然后**重启**。

**7. 验证**：使用 GPU-Z（Windows）/ `nvidia-smi` / amdgpu（`dmesg | grep -i bar`）。

## 重要说明

- **通常可以保持 Secure Boot 开启**——大多数固件接受未签名/打过补丁的模块。
- 如果设置错误的 BAR 大小后系统无法 POST：**清除 CMOS**（某些情况下需拔下电池）——ReBAR 会被禁用。
- 如果您完全不想修改 BIOS：在 **Linux** 上，开启 4G 解码后，较新的内核加上 `pci=realloc` 会自动调整 GPU BAR 大小——但 **Windows 需要 BIOS 修改**。
- NVIDIA Turing（16/20 系列）需要使用 [NvStrapsReBar](https://github.com/terminatorul/NvStrapsReBar) 代替 `ReBarDxe.ffs`。

需要我进一步获取 DSDT 补丁的 wiki 页面，或者帮助您检查特定的主板 BIOS 镜像（如果您有的话）吗？
