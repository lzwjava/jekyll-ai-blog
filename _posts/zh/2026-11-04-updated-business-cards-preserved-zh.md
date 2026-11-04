---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新后的名片已保留
translated: true
type: note
---

两个版本都保留。`card_output/` 已被 gitignore，没有额外内容需要提交。

## 当前布局

```
card_output/
├── business_card_zh.png   ← 新：二维码在职位下方，无“中国广州”
├── business_card_en.png   ← 新：二维码在职位下方，无位置
├── avatar.jpg
└── original/              ← 原始版（保留）
    ├── business_card_zh.png   ← 旧：有“中国广州”，无二维码
    ├── business_card_en.png   ← 旧：有位置，无二维码
    └── avatar.jpg
```

- **新版**（`card_output/`）: 移除"中国广州"、二维码放大后放到职位正下方、联系区上移填满。
- **原始版**（`card_output/original/`）: 保留了加入二维码之前的设计版本（含"中国广州"/Guangzhou, China、无二维码、暖咖主题、加粗正文），从 git 历史（commit `2a54b02`）重新渲染出来，与新版并存。

两个版本都是 4200×2400、2× 密度、暖咖深色主题。如果你想要的"original"是另一个历史版本（比如浅色主题版、或某种早期排版），告诉我具体是哪个时间点/样式，我再补一份。