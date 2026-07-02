---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大量可用磁盘空间
translated: true
type: note
---

| 文件系统 | 大小 | 已用 | 可用 | 使用率 | 挂载点 |
| ------------ | ------- | ------- | ------- | ------ | --------- |
| `/dev/nvme0n1p3` | **232G** | **11G** | **220G** | **5%** | `/`, `/home` |
| `/dev/nvme0n1p2` | 2.0G | 364M | 1.5G | 20% | `/boot` |
| `/dev/nvme0n1p1` | 599M | 21M | 579M | 4% | `/boot/efi` |
| `/tmp` (tmpfs) | 7.8G | 2.7M | 7.8G | 1% | 内存支持 |
| `/run/user/1000` | 1.6G | 4.1M | 1.6G | 1% | 内存支持 |

空间充足——主分区有 **220GB 可用**（已用 5%），完全没有磁盘压力。
