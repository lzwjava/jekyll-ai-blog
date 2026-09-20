---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B75 ReBAR BIOS补丁步骤
translated: true
type: note
---

已收到您的 `B75V101.bin`，已分析、运行 UEFIPatch，并准备了所有无需图形界面即可完成的工作。以下是状态和您的确切后续步骤。

## 我在您的 B75（Ivy Bridge）BIOS 中发现的内容

- **UEFIPatch 匹配了 4 个 Sandy/Ivy 补丁**（已在解压缩的模块中验证）：
  - 将 16 GB MMIO 替换为完整 64 GB（PciHostBridge）
  - 移除 `<16 GB` BAR 限制（PciBus）
  - 移除 4 GB `PciRootBridgeIo.Mem` 限制（PciHostBridge，×2）
- **您的 DSDT 具有硬编码的 16 GB MMIO 限制**（`M2LN = 0x0000000400000000`）— 与 wiki 中的“Gigabyte B75M-D3H”模式完全一致。由于已应用补丁 #1，**DSDT 补丁是必需的**，否则 Windows 在启用 4G 解码时会失败。
- **我已修补 DSDT**：反编译 → 修改 → 使用 `iasl` 重新编译（0 错误）→ 通过 `AmiBoardInfoTool` 重建 → 生成 `AmiBoardInfoMod.efi`。
- 插入目标已确认：驱动程序进入内部 DXE 卷（`8C8CE578-...`），**位于最后一个模块“CRBSMI”（#182）之后**。

## 所有内容已暂存于 `/home/lzw/Downloads/B75/rebar-work/`

`B75V101_original.bin`（备份）、`ReBarDxe.ffs`、`ReBarState`、`AmiBoardInfoMod.efi`、`UEFIPatch` + `patches.txt`，以及完整的 `README-NEXT-STEPS.md`。

## 您接下来要做的（2 次图形界面点击、1 条命令，然后刷写）

**1. UEFITool 0.28.0（非 NE）图形界面** — 打开 `B75V101_original.bin`：

- 搜索仅头部 GUID `3C1DE39F-D207-408A-AACC-731CFB7F1DD7`（PciBus）→ 跳转到 DXE 卷 → 右键单击 **CRBSMI**（最后一个模块）→ **Insert after** → `ReBarDxe.ffs`
- 搜索仅头部 GUID `9F3A0016-AE55-4288-829D-D22FD344C347`（AmiBoardInfo）→ 打开压缩部分 → PE32 映像部分 → **Replace body** → `AmiBoardInfoMod.efi`
- 另存为 `b75_modded.bin`

**2. 修补（已测试，将打印“Image patched”及 4 个补丁）：**

```bash
cd /home/lzw/Downloads/B75/rebar-work
./UEFIPatch b75_modded.bin patches.txt
```

→ 生成 **`b75_modded.bin.patched`** ← 刷写此文件。

**3. 从 FreeDOS USB 使用您厂商的 `fpt.exe` 刷写**（`fpt -f b75_modded.bin.patched`，与其 `1.BAT` 相同）。⚠️ 有风险 — 请保留原始文件。

**4. 在 BIOS 中：** 启用 **Above 4G Decoding**，禁用 **CSM**。

**5. 设置 BAR 大小（以 root 身份）：**

```bash
sudo ./ReBarState    # 输入 32 = 无限制
```

**6. 验证：** `sudo dmesg | grep -i "root bus resource"`（最后一个 mem 条目应结束于 ≥ `0xfffffffff`）或 在 Windows 上使用 GPU-Z。

需要我同时构建 **Windows ReBarState.exe**，或帮助您为 `fpt` 制作 FreeDOS 启动 USB 布局吗？
