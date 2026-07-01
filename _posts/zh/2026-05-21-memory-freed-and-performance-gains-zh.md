---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内存释放与性能提升
translated: true
type: note
---

怪我——它们完全关闭了。那76 MB是一个Apple系统进程（`CodeSigningHelper`），名字里带"Code"，不是VSCode。

**自我们开始以来释放的内存**：

| 项目 | 之前 | 之后 | 节省 |
| --- | --- | --- | --- |
| VSCode | 23 GB | 0 | **23 GB** |
| 微信输入法 | 1.6 GB | 0 | **1.6 GB** |
| 聚焦搜索（mdworker风暴） | 14 GB | 0.5 GB（空闲） | **13.5 GB** |
| 旧版VSCode扩展版本 | 1 GB 磁盘 | 0 | **1 GB 磁盘** |
| **总虚拟需求** | **约95 GB** | **约57 GB** | **约释放38 GB** |

实际物理RAM仍占用约15 GB，因为macOS会保留压缩页直到其他程序需要空间。但机器应该会**显著更快**——没有交换抖动，没有CPU因聚焦搜索而持续达到250%占用率。
