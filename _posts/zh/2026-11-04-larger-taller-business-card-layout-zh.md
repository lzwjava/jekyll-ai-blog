---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更大更高名片布局
translated: true
type: note
---

两张名片均已重新生成，采用更高、更大的布局：

- **英文名片**：`card_output/business_card_en.png` (2300×1680)
- **中文名片**：`card_output/business_card_zh.png` (2300×1680)

在 `ww/card/card.py` 中所做的更改：

- **更大的画板**：2300×1680（由2100×1200增大）——更高，确保「About」文本有充足空间。
- **全文字号增大**：更大的「About」正文字体（44/46 vs 38/40），姓名（92），角色（46），联系方式（34），水印（34）。
- **增加行距**：提高了 line-height/间距 和段落间距。
- **左面板稀疏化**：头像更大（480），姓名/角色下移，二维码更大，联系方式位置降低，使高面板不显空旷。

我以编程方式验证了，英文（文本底部约1514）和中文（约1408）的介绍文本都清晰地位于水印（约1590）上方，没有裁剪或重叠。
