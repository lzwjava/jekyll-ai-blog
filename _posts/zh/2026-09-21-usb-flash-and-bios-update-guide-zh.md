---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB闪存与BIOS更新指南
translated: true
type: note
---

USB 已制作并验证完成。以下是最终检查清单：

## ✅ USB 已就绪（已验证）

- FreeDOS 启动文件已存在，安装程序**已跳过** → 直接启动到 `C:\>`
- `fpt.exe` + `fparts.txt`（您的厂商刷写工具）
- `NEWBIOS.BIN`（您修改后的 BIOS）、`OLDBIOS.BIN`（原始 BIOS）、`flash.bat`
- 剩余 5.9 MB 空间 — 足够存放 4 MB 的 `BACKUP.BIN` 备份

## 在 B75 主机上

1. **弹出 USB** 从当前机器，将其插入 B75 主机。
2. **从 USB 启动** — 按下启动菜单键（通常为 **F8 / F11 / F12**，也可尝试 Del/F2 进入 BIOS 查找 "Boot Menu"），选择 **legacy / non-UEFI** 的 USB 启动项。（CSM 仍处于开启状态，因此 legacy 启动可用。）
3. 在提示符下输入：

   ```
   C:\> flash.bat
   ```

4. 该脚本将：
   - 备份当前 BIOS → `BACKUP.BIN`
   - 刷写 `NEWBIOS.BIN`
5. 等待显示 **`FLASH OK`** → 然后关机。

## 接下来（顺序很重要）

1. 进入 **BIOS 设置** → 开启 **Above 4G Decoding**，关闭 **CSM**。
2. 启动进入 Linux → 执行 `sudo ./ReBarState` → 输入 `32` → 重启。
3. 验证：`sudo dmesg | grep -i "root bus resource"`（最后一个 mem window 应 ≥ `0xfffffffff`）或使用 GPU-Z。

⚠️ 如果 `flash.bat` 显示 **FAILED** — 不要关机；只需重新运行 `fpt -f NEWBIOS.BIN`。如果后续主板无法 POST，请清除 CMOS（必要时可拔掉电池）。

祝好运！请告知刷写结果，或者如果您需要我构建一个用于验证的 Windows 版 `ReBarState.exe`，也请随时告知。
