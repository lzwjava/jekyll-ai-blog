---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 烧录 Ubuntu ISO 到 USB
translated: true
type: note
---

ISO 大小为 6.1 GB，可写入你的 15.7 GB U 盘。请使用以下命令：

```bash
diskutil unmountDisk /dev/disk12   # 首先卸载已挂载的卷
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress
sync                                # 写入完成后刷新缓存再拔下U盘
```

注意事项：
- 在 macOS 上使用 **`/dev/rdisk12`**（原始设备）可加快写入速度——但请 *务必确认* `disk12` 是正确的磁盘。拼写错误（如 `disk1`、`disk3`）会导致你的系统/数据卷被擦除。运行前请用 `diskutil list` 核实。
- 对整个磁盘执行 `dd` 会替换现有的 GPT/分区表，因此当前所有 4 个分区都会被清除——这是预期的正常行为。
- 请等待 `sync` 完成后再拔下 U 盘。U 盘容量为 15.7 GB，因此在 USB 2.0 速度下需要几分钟。
- 无需使用 `--clear` 等效命令；`dd` 直接写入原始 ISO 镜像（混合 ISO），该镜像可直接启动。

完成后，使用 `diskutil list disk12` 验证——你应该看到单个分区，显示为 Ubuntu 安装程序。