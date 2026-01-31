---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 平衡稀缺数据的速度成本
translated: true
type: note
---

“Nearline”是指介于 **online**（即时访问）和 **offline**（归档，需要手动检索）存储之间的一种存储层级或访问方式。

**Key characteristics:**

- **Access speed**：比 online 存储慢，但比 offline 归档快
- **Cost**：比高性能 online 存储便宜，但比 cold/archival 存储昂贵
- **Use case**：访问频率较低的数据（可能每月或每季度一次），但在需要时必须在几秒到几分钟内完成检索

**Common examples:**

- Google Cloud 的 “Nearline Storage” 或 AWS 的 “Infrequent Access” 层级等云存储服务
- 带有机器人检索系统的 Tape libraries
- 用于备份数据的次级 Disk arrays

该术语源于对数据的区分：数据可以是 “online”（在 primary storage 上即时可用）、“nearline”（可快速检索但非即时访问）或 “offline”（需要物理干预，例如加载磁带）。