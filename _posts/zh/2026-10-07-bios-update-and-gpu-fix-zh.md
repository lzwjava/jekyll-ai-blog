---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BIOS更新与GPU修复
translated: true
type: note
---

✅ USB 盘已准备就绪。具体操作如下：

| 步骤 | 结果 |
| --- | --- |
| 擦除 Debian 安装镜像 | ✅ |
| 创建 MBR + 单个 FAT32 分区（`/dev/sdb1`） | ✅ 标签 `USB`，4GB |
| 复制 BIOS 文件 | ✅ `E7978IMS.AA0`（16MB） |
| 安全卸载 | ✅ |

**现在可以安全拔除 USB 盘**（已卸载）。

## 现在刷新 BIOS

1. **从 Debian 机器上拔除 USB**（已卸载，可安全移除）。
2. **重启**机器并反复按 **DEL** 进入 BIOS。
3. 在 BIOS 中，点击 **M-FLASH**（Click BIOS 5 界面底行按钮，或按 F7 进入高级模式 → 位于左侧栏 / “Utilities”）。
4. 系统将重启进入 M-Flash 模式。
5. 选择 **“选择单个文件以更新 BIOS”**。
6. 选择您的 USB 驱动器 → 选中 **`E7978IMS.AA0`**。
7. 确认 **Yes**。⚠️ **请勿断电或中断** — 等待完成（约 1-2 分钟）并自动重启。

## 然后启用 GPU 修复

刷新后，再次进入 BIOS（按 DEL）：

1. **F7** → 高级模式。
2. **Settings → Advanced → PCI Subsystem Settings**（或类似选项）。
3. **“Above 4G Decoding” → Enabled**。
4. **F10** → 保存并退出。

## 最后

启动进入 Debian 并告诉我 — 我将验证 BAR 是否已分配，并运行 `nvidia-smi` 确认 Tesla M40 正常工作。

祝刷新顺利 — 请记住：**不要中断 BIOS 更新**。完成后请通知我，我会继续处理。🚀
