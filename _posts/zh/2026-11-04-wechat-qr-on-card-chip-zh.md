---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 名片芯片上的微信二维码
translated: true
type: note
---

已完成（`3c4bc4c`）——微信二维码现在已放在卡片上。所有四个预览（中文/English × 深色/浅色）均已开放。

## 变更内容

- 二维码来自 `~/Downloads/qrcode.jpg`，自动进行**方形裁剪**（图片原尺寸为747×719），调整大小后放置在左侧面板底部的**白色芯片**上，位于联系人列表正下方。
- 联系人从5行缩减至4行（**TruthSoft · 邮箱 · 微信 · WhatsApp**；GitHub保留在底部水印中），间距收紧以腾出空间。
- 适用于两种主题和两种语言，保持全密度（2倍输出下二维码区域高度为816px —— 易于扫描）。

```bash
ww card --lang zh                    # 二维码来自默认的 ~/Downloads/qrcode.jpg
ww card --lang en --qr /path/q.png   # 任何其他二维码图片
```

已验证二维码已渲染（其区域内包含1,559个深色模块像素）。如果芯片位置/外观需要调整——例如添加"微信 扫码"标题，将其移至右下角，或使用彩色（非白色）背景——请尽管提出。