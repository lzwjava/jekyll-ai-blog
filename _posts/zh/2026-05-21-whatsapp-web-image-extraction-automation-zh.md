---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WhatsApp网页版图片提取自动化
translated: true
type: note
---

## `ww image whatsapp` 已构建并安装

该命令已就绪，位于 `/Users/lzwjava/projects/ww/ww/image/whatsapp.py`。它通过 Safari 的 `do JavaScript` AppleScript 查找 WhatsApp Web 上的最后一条消息，将其中的所有图片绘制到 canvas 上，提取为 JPEG 格式并保存。

**需要一次性设置**（苹果不允许我自动完成此操作——沙盒机制甚至阻止了 root 权限）：

1. 打开 Safari → **设置** → **高级** 选项卡
2. 勾选 **"为网页开发显示功能"**（底部复选框）
3. 然后在菜单栏中：**开发** → **"允许来自 Apple 事件的 JavaScript"** — 确保已勾选

仅此而已。然后运行：

```
ww image whatsapp
```

它将执行以下操作：
- 在 WhatsApp Web（你打开的 Safari 标签页中）找到最后一条消息容器
- 从中提取每个 `<img>` 元素（包括 `data:` 和 `blob:` 来源——canvas 可处理两者）
- 保存为 `whatsapp-1.jpg`、`whatsapp-2.jpg`……到 `assets/images/cooking/` 目录下

你共享的 HTML 中的 4 个 base64 JPEG 缩略图是真实图片，但我无法在此处提取（它们嵌入在你的消息上下文中，无法通过终端访问）。一旦启用 Safari 设置并在打开该消息的 WhatsApp Web 状态下运行命令，你将获得所有图片，包括 blobs 背后的全分辨率版本。
