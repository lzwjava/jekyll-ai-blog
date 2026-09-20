---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B75 BIOS刷写说明
translated: true
type: note
---

一切准备就绪。以下是具体的刷写方法——我已经准备好了所有文件和一个一键脚本。

## 我准备的内容

在 `/home/lzw/Downloads/B75/rebar-work/` 目录下：

- **`make-usb.sh`** — 一键脚本，用于构建完整的可启动 USB
- **`FD13LITE.img`** — FreeDOS 启动镜像（32 MB）
- **`usb-flash/`** — DOS 刷写文件：
  - `fpt.exe` + `fparts.txt`（你的供应商提供的刷写工具）
  - `NEWBIOS.BIN` = 最终的 `b75_modded.bin.patched`
  - `OLDBIOS.BIN` = 原始 BIOS（USB 上的安全副本）
  - `flash.bat` = 自动备份 + 刷写脚本

## 步骤

**1. 将 U 盘（任意容量）插入这台 Linux 机器**，然后告诉我（或运行）：

```bash
lsblk                          # 找到 U 盘，例如 /dev/sdb
cd /home/lzw/Downloads/B75/rebar-work
sudo ./make-usb.sh /dev/sdb     # <-- 整个磁盘，而不是 /dev/sdb1
```

该脚本会拒绝操作非可移动磁盘（安全机制），写入 FreeDOS，复制刷写文件，并将其修改为**直接启动到 `C:\>` 提示符**（跳过 FreeDOS 安装程序）。在擦除 U 盘之前，它会要求你输入 `YES` 确认。

**2. 将 U 盘移到 B75 电脑上，并从 U 盘启动。**

- 按下**启动菜单键**（通常是 F8 / F11 / F12，取决于主板），选择**非 UEFI / 传统** USB 启动项。DOS 需要传统启动，因此暂时保持 CSM 开启。

**3. 在 `C:\>` 提示符下，输入：**

```
flash.bat
```

该脚本会执行两个操作：

1. 备份当前的 BIOS → `BACKUP.BIN`（保存在 U 盘上）
2. 刷写 `NEWBIOS.BIN`（完整的 4 MB 镜像，使用与你供应商 `1.BAT` 相同的 `fpt -f` 方法）

**4. 等待 `FLASH OK` 提示出现**，然后断电。

## 刷写后（顺序很重要）

1. 开机 → **进入 BIOS 设置**：
   - 启用 **Above 4G Decoding**
   - 禁用 **CSM**（*只有*在刷写完成后才执行此操作——之前需要开启 CSM 才能启动 DOS U 盘）
2. 启动进入 Linux，运行 `sudo ./ReBarState`，输入 `32`，重启。
3. 使用 `dmesg | grep -i "root bus resource"` 或 GPU-Z 验证。

---

⚠️ 两个安全提示：

- 如果 `flash.bat` 报告 **FAILED** —— **不要**断电；只需重新运行 `fpt -f NEWBIOS.BIN`。
- 保管好 `B75V101_original.bin`（以及 U 盘上的 `OLDBIOS.BIN` 副本）——这是你的恢复镜像。

现在插上 U 盘并告诉我设备名称（或粘贴 `lsblk` 输出），我会为你运行脚本。
