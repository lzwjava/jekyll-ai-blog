---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 等高的二维码图片
translated: true
type: note
---

完成。现在两张二维码图片都以完全相同的高度渲染（200px），因为布局使用了固定的 `height`，配合 `width: auto` 和 `object-fit: contain`：

- **wechat_group.jpg**（1050×1575）→ 高 200px，宽约 133px
- **whatsapp_group.jpg**（1280×1240）→ 高 200px，宽约 206px

`object-fit: contain` 保留了每张图片的宽高比，因此二维码不会变形——只有高度被固定，两个 flex 项目保持居中并排显示。
