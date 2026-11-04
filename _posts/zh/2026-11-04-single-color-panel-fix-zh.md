---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 单色面板修复
translated: true
type: note
---

两张卡片均已重新生成，并带有干净的单一颜色左侧面板：

- `card_output/business_card_en.png` (2300×1680)
- `card_output/business_card_zh.png` (2300×1680)

问题：我引入的一个scaling bug使得accent divider延伸至整个左侧面板（巨大的金色块），而不是一条细线——这就是造成“双色”外观的原因。我完全移除了accent divider线，因此左侧面板现在是一个纯色的暖棕色，右边只有黑色背景。通过pixel sampling确认面板是均匀的。