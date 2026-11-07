---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed works grid alignment and CSS
translated: false
type: note
---

Done. I wrote the complete, fixed works grid to:

**`/Users/lzwjava/projects/employment-files/works-grid.html`**

What I fixed:

1. **All 12 text-only cards** (趣标注, 拼我 PingWorld, vToken, 小猿题库·游戏系列, 汉语大词典, BitEDU, FOMOO, 积分兑换平台, 拍照穿越大学 H5, 开学解锁新发型 H5, 课程裂变 H5, 礼包兑换 H5) now have the missing `<div class="work__body">` wrapper, matching every thumbnailed card.
2. **Grid CSS** added `align-items: stretch` + `.card.work { height:100%; display:flex; flex-direction:column }`, and `.work__meta { margin:auto 0 0 0 }` — so every card in a row stretches to the same height and the meta line pins to the bottom. This is the fix for the ragged grid/misalignment.
3. Also added `aspect-ratio: 16/9` on `.work__thumb` so all thumbnails have a uniform height, and a hover overlay style for "查看项目 →".
4. Includes complete CSS (tags, card, grid) inline so you can preview it directly — open it in a browser to see.

You can copy the `<div class="grid grid--3 works">…</div>` block and the CSS into your real page.

Two things so I can finish properly:
- **Where does your actual site live?** If you give me the real file path, I'll apply these changes there instead of the new file.
- You also pasted `.card.person` CSS (avatar circle) earlier — do you want that one fixed too, or were we only dealing with the works grid?
