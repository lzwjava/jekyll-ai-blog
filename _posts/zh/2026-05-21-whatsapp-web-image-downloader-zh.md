---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WhatsApp Web 图片下载器
translated: true
type: note
---

完成。以下是构建内容的摘要：

---

## `ww image whatsapp` — 已创建并准备就绪

**涉及的两个文件：**

1. `/Users/lzwjava/projects/ww/ww/image/whatsapp.py`（新增，195 行）
2. `/Users/lzwjava/projects/ww/ww/main.py`（2 处添加：帮助文本 + 子命令分发）

**工作原理：**

- 在 Safari 的前台标签页中运行 AppleScript `do JavaScript`
- 在 WhatsApp Web 上找到最后一个 `[data-testid="msg-container"]`
- 获取其中的所有 `<img>` 元素
- 将每个图像绘制到新的 `<canvas>` 上，然后调用 `canvas.toDataURL('image/jpeg')`
- 这对 `data:image/jpeg;base64,...` 和 `blob:https://...` 来源都有效，因为 blob 位于同一源上
- 通过 AppleScript 返回 base64 数据
- 解码并将 `.jpg` 文件写入输出目录

**用法：**

```
# Download images from the last message (saves to assets/images/cooking/)
ww image whatsapp

# Custom output directory
ww image whatsapp --dir ~/Desktop/wa-pics

# Open Safari and navigate to WhatsApp Web first (waits 8s for load)
ww image whatsapp --open
```

**现在运行它。**确保 WhatsApp Web 在 Safari 中打开，并且消息可见，然后：

```
ww image whatsapp
```

它将从您展示给我的消息中提取所有图像——图像专辑中的 4 张并排图像——并将它们保存为 `whatsapp-1.jpg` 到 `whatsapp-N.jpg`，保存在 `assets/images/cooking/` 中。