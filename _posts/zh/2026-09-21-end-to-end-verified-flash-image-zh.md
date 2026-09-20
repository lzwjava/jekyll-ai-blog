---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 端到端验证闪存映像
translated: true
type: note
---

端到端全部验证通过。您的**最终闪存就绪镜像**已准备好：

**`/home/lzw/Downloads/B75/rebar-work/b75_modded.bin.patched`**

## 最终验证（全部在 `.patched` 文件中）

| 检查项 | 结果 |
| --- | --- |
| ReBarDxe 已插入（GUID `A8EE1777…`，DXE 驱动） | ✅ 模块 #183 |
| AmiBoardInfo DSDT 已修补（PE32 = `AmiBoardInfoMod.efi`） | ✅ md5 `3fe6c7c2…` |
| PciBus `<16GB` → `<64GB` BAR 限制已移除 | ✅ |
| PciHostBridge 16GB → 64GB MMIO | ✅ |
| PciHostBridge 4GB `PciRootBridgeIo.Mem` 限制已移除 | ✅ ×2 |

## 剩余操作（在物理机器上）

1. **刷写** — 使用 `fpt.exe` + `fparts.txt` 启动 FreeDOS USB，然后执行：

   ```
   fpt -f b75_modded.bin.patched
   ```

   ⚠️ 请妥善保管 `B75V101_original.bin` — 刷写期间切勿断电。

2. **BIOS 设置** — 启用 **Above 4G Decoding**，禁用 **CSM**。

3. **设置 BAR 大小**（以 root 身份，在此 Linux 机器上）：

   ```bash
   cd /home/lzw/Downloads/B75/rebar-work
   sudo ./ReBarState    # 输入 32（无限制），然后重启
   ```

4. **验证**：

   ```bash
   sudo dmesg | grep -i "root bus resource"   # 最后一个内存窗口结尾应 ≥ 0xfffffffff
   sudo dmesg | grep -i bar
   ```

   或在 Windows 上用 GPU-Z。

如果设置 BAR 大小后无法 POST：**清除 CMOS**（必要时拔掉电池）— 这将禁用 ReBAR。

祝您好运！需要我准备 FreeDOS USB 镜像布局（文件夹结构 + `flash.bat` 中的刷写命令），还是也构建一个 Windows 版 `ReBarState.exe`？
