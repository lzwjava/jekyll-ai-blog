---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 故障U盘
translated: true
type: note
---

dd 现在正在退出（挂起的 I/O 放弃后，其状态显示为“exiting”）——它随时会带着 I/O 错误返回你的 shell。给它几秒钟。

所以情况总结如下：

**你的 USB 闪存盘（`OnlyDisk`，15.7 GB）存在缺陷/故障。** 在大约 5.04 GB 处遇到了坏区，返回“介质不存在”并挂起了 USB 通道，导致写入停滞。这不是命令问题——闪存介质或控制器已经失效。

**一旦 dd 退出，下一步操作：**

1. **不要尝试从该闪存盘启动**——镜像不完整，尾部扇区已损坏。
2. **测试驱动器本身**：运行 `diskutil eraseDisk FAT32 TEST /dev/disk12` ——如果该命令挂起或报错，则闪存盘已报废，需要换一个。
3. 如果擦除成功，可能是端口不稳定——**尝试其他 USB 端口**，并用较小的块大小重新刷写：`sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=1m status=progress`。
4. 每次刷写后，务必执行 `sync` 并用 `diskutil list disk12` 验证（如果仍然显示异常，则该驱动器不可靠，不值得用于安装操作系统）。

需要我等待并检查 dd 是否真正干净退出，或者在你运行擦除测试时监控结果吗？