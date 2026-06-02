---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载 Google 云端硬盘桌面版
translated: true
type: note
---

**问题：** 我们可以从这个支持页面下载 Google Drive 桌面版吗？

**回答：**

可以。该页面是 Google 官方的 **Google Drive 桌面版**（同步客户端，曾用名 Backup and Sync / Drive File Stream）支持文档。

对于 macOS，该页面上的直接下载链接为：

```
https://dl.google.com/drive-file-stream/GoogleDrive.dmg
```

步骤：
1. 下载 `.dmg` 文件
2. 打开它
3. 按照安装程序操作
4. 在菜单栏图标处使用您的 Google 账号登录

它会在访达中将您的 Google Drive 挂载为虚拟驱动器（默认采用流式传输，而非完整本地副本），并支持可选的离线选择性同步。最多可同时登录 4 个 Google 账号。

由于您使用的是 M2 MacBook Air——该客户端原生支持 ARM 架构，无需 Rosetta 转译。
