---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenWrt Live USB 中缺失的工具
translated: true
type: note
---

Question: 尝试从 USB 启动将 OpenWrt 安装到内部磁盘时，找不到命令（zcat 和 dd）

Answer: 

你已经通过 USB 启动进入了 OpenWrt live 系统（root 登录，无密码），但执行 `lsblk`、`dd` 或 `zcat` 等基础命令时显示 "command not found"。这是因为最近版本的 OpenWrt（特别是 snapshots 或某些 stable builds）中的 **combined .img** 启动环境非常精简 —— 它使用的 busybox 仅包含必要的 applets，为了保持镜像足够小，许多常用工具（包括 `dd`、`lsblk`、`zcat`、`gzip` 等）默认**未包含**在内。

### 首先进行快速检查
运行以下命令确认你的情况：

```
which dd
which lsblk
which zcat
busybox
```

- 如果 `which` 显示未找到或为空 → 则说明这些命令不存在。
- `busybox` 应该会显示支持的命令列表（通常包括 `cat`、`echo`、`mount` 等，但在极简的 initramfs 中**不包含** `dd` 或 `lsblk`）。

### 2026 年的正确及推荐方法（当前官方方法）
由于这种极简工具的问题，OpenWrt 官方 x86 指南对于大多数用户不再建议直接从启动的 OpenWrt USB 镜像内进行安装。相反：

**最佳且最简单的方法：使用常规的 Linux live USB（例如你现有的 Linux Mint Cinnamon USB 或 Ubuntu/Fedora live）来写入镜像**

1. **重启** 笔记本电脑，暂时移除 OpenWrt USB。
2. 从你的 **Linux Mint live USB** 启动（或者下载新的 Ubuntu live ISO 并使用 Rufus/Etcher/dd 制作一个）。
3. 进入 live 桌面后（选择 try without installing）：
   - 打开 terminal。
   - 如果需要，重新下载 OpenWrt 镜像（或预先将其复制到 USB）：
     ```
     wget https://downloads.openwrt.org/releases/24.10.5/targets/x86/64/openwrt-24.10.5-x86-64-generic-ext4-combined-efi.img.gz
     gunzip openwrt-24.10.5-x86-64-generic-ext4-combined-efi.img.gz
     ```
     （如果你喜欢，也可以使用对应的 ImmortalWrt 镜像）
4. 识别你的 **internal** 500GB 磁盘（请小心 —— 选错会抹除数据！）：
   ```
   lsblk -o NAME,SIZE,TYPE,MODEL
   sudo fdisk -l
   ```
   - 内部磁盘通常是 `/dev/sda`（如果是 NVMe SSD，则是 `/dev/nvme0n1`）。
   - USB live 启动盘通常较小，例如 `/dev/sdb`。
5. 写入镜像（这将抹除数据并安装 OpenWrt）：
   ```
   sudo dd if=openwrt-....img of=/dev/sda bs=4M status=progress conv=fsync
   ```
   - 将 `/dev/sda` 替换为你的内部磁盘。
   - 等待完成（可能需要 5-20 分钟）。
6. 
   ```
   sync
   ```
7. 关机，移除 live USB，重启 → 笔记本现在应该直接启动进入 OpenWrt（console 登录：root，初始无密码）。

首次启动后：
- 设置密码：`passwd`
- 连接网络（通常网线连接到 modem 作为 WAN 即可默认工作）
- 访问 LuCI：http://192.168.1.1 → 如果有提示请再次设置密码
- 如果 Web GUI 还没有，运行 `opkg update && opkg install luci`

### 如果你坚持使用 OpenWrt USB live（高级，不推荐）
你需要先安装缺失的工具 —— 但 live 系统默认 **没有 opkg** / package manager，通常也没有 internet（除非你通过 `ifconfig`/`wpa_supplicant` 手动配置 Ethernet/Wi-Fi —— 这很复杂）。

一些旧的论坛帖子建议：
- 如果 `/bin/dd` 以某种方式存在 → 使用它。
- 或者通过 `wget` 获取镜像（如果网络正常）然后通过管道传输到 `cat > /dev/sda` —— 但这种方式不可靠且危险。

大多数人会放弃这种方式并切换到完整的 Linux live USB —— 这种方式更快且拥有所有工具（`dd`、`lsblk`、`wget`、`gunzip` 等）。

### 总结 – 现在该做什么
- 重启 → 改为启动你的 Linux Mint live USB。
- 在那里使用 `dd` 将 .img 写入 `/dev/sda`（内部磁盘）。
- 这是近年来几乎所有在 x86 硬件（笔记本、mini-PCs 等）上安装 OpenWrt 的用户所采用的标准、可靠的方法。

请先备份所有数据（虽然你提到它可以运行 Linux Mint，所以大概没有留下什么关键内容）。如果你告诉我 `ls` 或 `busybox` 显示的具体内容，或完整的错误信息，我可以进一步优化建议。

References:  

- [https://openwrt.org/docs/guide-user/installation/openwrt_x86](https://openwrt.org/docs/guide-user/installation/openwrt_x86)
- [https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430](https://forum.openwrt.org/t/openwrt-x86-on-usb-stick/142430)
- [https://teklager.se/en/knowledge-base/openwrt-installation-instructions](https://teklager.se/en/knowledge-base/openwrt-installation-instructions)