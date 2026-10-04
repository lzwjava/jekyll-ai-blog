---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 制作Ubuntu启动U盘
translated: true
type: note
---

磁盘已卸载 ✅。但 `sudo` 需要你的密码，我无法替你输入——**请自己在终端中运行以下命令**：

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync
```

完成后（进度显示 `6139+0 records in/out`），执行弹出：

```bash
diskutil eject /dev/disk12
```

⚠️ **按下回车前请确认设备**：它是 `/dev/rdisk12`——15.7 GB 的外部 USB。如有疑问，用 `diskutil list` 再次核对。写入 `rdisk0` 会破坏你的内置 SSD。

`dd` 完成后，你的 USB 将成为可启动的 Ubuntu 26.04 安装盘；“FD13-LITE” 分区会消失（属于正常现象）。告诉我结果或是否报错。