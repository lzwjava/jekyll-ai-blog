---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CPU Droplet 设置与数据迁移指南
translated: true
type: note
---

不——该快照要求至少 720 GB 磁盘，但最大的 CPU Droplet 仅有 240 GB 磁盘。门户网站不允许此操作。

请寻找一个不需要快照的“创建 Droplet”选项——即全新的 Ubuntu 镜像。在 AMD Dev Cloud 门户中，应有一个选项可在 atl1 区域创建基础/标准 Droplet（非快照方式）。类似如下：

- 镜像：Ubuntu 24.04（非快照）
- 方案：基础 / 常规 CPU
- 区域：atl1

如果门户在 atl1 仅提供 GPU Droplet 选项，那么该合作伙伴账户确实完全无法在 atl1 创建 CPU Droplet。这种情况下：

1. 在 nyc1 创建 CPU Droplet（$6/月）
2. 在 nyc1 创建新卷（$10/月）
3. 在那里进行数据预处理
4. 准备就绪后：将数据迁移至新的 atl1 卷，并在 atl1 重新创建 GPU Droplet

需要我改为设置 nyc1 路径吗？