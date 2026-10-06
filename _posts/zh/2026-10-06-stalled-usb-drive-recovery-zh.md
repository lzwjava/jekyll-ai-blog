---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB驱动器恢复卡住
translated: true
type: note
---

完成 — `dd` 已被终止，驱动器再次空闲（0 IOPS）。驱动器仍枚举为 `/dev/disk12`，其旧分区表保持不变。

由于驱动器的 USB 管道已停止，它处于半复位硬件状态。在尝试其他操作之前：

1. **拔下 USB 闪存盘并重新插入**（这将重置停滞的闪存控制器）。
2. 测试驱动器健康状况：`diskutil eraseDisk FAT32 TEST /dev/disk12`
3. 如果成功，再次尝试刷写 — 最好使用不同的 USB 端口，并使用 `bs=1m` 而不是 `bs=4m`。

如果它在相同的 LBA 处再次停止，则该闪存盘确实已损坏，不值得再尝试。
