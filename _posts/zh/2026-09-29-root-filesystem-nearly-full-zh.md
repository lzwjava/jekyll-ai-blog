---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 根文件系统几乎已满
translated: true
type: note
---

以下是本系统的磁盘使用情况：

| 文件系统 | 大小 | 已用 | 可用 | 使用率 | 挂载点 |
| --- | --- | --- | --- | --- | --- |
| `/dev/nvme0n1p2` | 916G | 814G | **55G** | **94%** | `/` |
| `/dev/sda1` | 1.8T | 1.2T | **590G** | 67% | `/mnt/data` |
| tmpfs | 6.3G | 4.1M | 6.3G | 1% | `/run` |
| tmpfs | 32G | 179M | 32G | 1% | `/dev/shm` |
| `/dev/nvme0n1p1` | 511M | 6.2M | 505M | 2% | `/boot/efi` |

**总结：**

- 根文件系统（`/`）使用率为 **94%**，仅剩 **55G** 可用——空间紧张。
- 你的工作目录 `/mnt/data` 是一个 1.8T 的卷，剩余 **590G**（已用 67%）。
