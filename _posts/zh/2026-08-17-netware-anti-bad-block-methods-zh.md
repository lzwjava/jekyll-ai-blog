---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NetWare反坏块方法
translated: true
type: note
---

正确答案是 **B. 热调整和写后读验证 (Hot Fix and read-after-write verification)**。

解释：

在 Novell NetWare 中，用于防止不可靠磁盘块的两种互补技术是：

1. **Hot Fix（热调整/热修复）** — 磁盘上的一块保留区域（Hot Fix 重定向区域），会自动将数据从坏块重定向出去。当检测到坏块时，数据会被写入该保留区域。

2. **Read-after-write verification（写后读验证）** — 数据写入磁盘后，系统会立即读回并与写入内容进行比较。如果不匹配，该块会被标记为坏块，并通过 Hot Fix 重定向数据。

磁盘镜像（Disk mirroring）和磁盘双工（Disk duplexing）是不同技术——它们用于防止**物理磁盘故障**（整盘冗余），而不是防止单个磁盘内的不可靠块。

因此答案是 **B**。
