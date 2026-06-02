---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设置ML数据卷
translated: true
type: note
---

**快速解答：**

**存储大小：** 200GB

**配置：** 自动格式化并挂载

**文件系统：** Ext4

**名称：** `ml-data`

就是这样。理由如下：

- **自动格式化并挂载** — 省去 `mkfs` + `fstab` 步骤，DigitalOcean 会帮你完成
- **Ext4** — 久经考验，广泛支持，除非你有超过 16TB 的大文件或特定吞吐量需求，否则没有理由使用 XFS。对于模型检查点和 token 二进制文件，Ext4 完全够用
- **200GB** — 如上计算，覆盖分词数据 + 3 个检查点 + 余量

Droplet 启动后，卷将在 `/mnt/ml-data` 就绪 — 只需 `cd /mnt/ml-data` 即可开始工作。
