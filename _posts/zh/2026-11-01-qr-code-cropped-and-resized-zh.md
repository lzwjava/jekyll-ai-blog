---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 二维码裁剪与调整
translated: true
type: note
---

完成。QR码已成功裁剪并调整大小。

**结果：** `assets/images/group/gg2-qr.jpg`（44 KB，300×300）

- **定位**了原始1290×2796截图中的QR码（位于x:379–909, y:1135–1665），使用OpenCV的QR检测器
- **裁剪**了中心QR码区域，并保留8px的干净边距
- **正方形** — 裁剪区域本身已是正方形（含边距后为546×546）
- **缩小** — 使用Lanczos重采样调整为300×300
- **验证** — 裁剪后的QR码仍能正确解码为WhatsApp邀请链接：
  `https://chat.whatsapp.com/IHLI78x48IG8Q94eQWVFmO?...`
