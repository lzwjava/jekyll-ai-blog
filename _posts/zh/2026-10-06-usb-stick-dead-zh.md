---
audio: false
generated: true
image: false
lang: zh
layout: post
title: U盘无法使用
translated: true
type: note
---

这是决定性的失败。kernel log 中的序列：

```
22:55:30  removed disk12                    ← 从磁盘树中脱落
22:55:35  unable to probe /dev/disk12s1/2/3 ← DiskArbitration 无法读取 media
22:56:24  removed disk12s1 / s2 / s3
22:56:26  removed disk12                    ← 整个磁盘节点消失
```

USB device 仍然物理连接在 bus 上（`OnlyDisk@00130000` 存在于 IORegistry，空闲），但 **media 不再响应** — 与导致 `dd` 挂起的 "medium not present" 行为相同。kernel 完全放弃了它：`Could not find disk for disk12`。

**结论：这个 USB stick 已死亡。** 证据时间线：
1. `dd` 成功写入至 **5.04 GB**，然后在固定 LBA 处遇到 bad media — pipe 停滞，重试数十次，挂起超过 18 分钟。
2. 重新插拔后，`diskutil eraseDisk` **甚至无法打开 device**。
3. DiskArbitration 无法探测任何 partition — flash 现在完全无响应。

这是一个 white-label "OnlyDisk" stick（通用，无品牌），这吻合 — 它们使用最廉价的 flash 和 controller，一旦开始抛出 "medium not present" 错误，就无法恢复。

**建议：停止尝试恢复它。** 您是在一个已经失败两次的 drive 上赌 OS 安装。一个名牌 16 GB+ USB 3.0 stick 只需几美元，并且可以可靠地 flash：

```bash
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdiskX bs=4m status=progress
```

（先用 `diskutil list` 确认 `X`）。如果你 *必须* 最后一次尝试旧 stick，请插拔并检查 `diskutil list` — 但我预计它将保持消失或再次失败。