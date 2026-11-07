---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Ragged Works Grid Rows
translated: false
type: note
---

I see the real problem now. In this 3-column works grid, the cards are **inconsistent**: most have a `.work__thumb` image at the top, but these **five are text-only** with no thumbnail and no `.work__body` wrapper:

- 趣标注
- 拼我 PingWorld
- vToken
- 小猿题库 · 游戏系列
- FOMOO

That's why the grid looks wrong — the text-only cards are shorter and don't fill the row, so cards don't align across columns and rows look ragged. The fix is two parts:

**1. Make every card equal height + properly structured** (add the missing `.work__body` wrapper and standardize), and

**2. Fix the grid CSS** so text-only cards stretch to match thumbnailed ones.

Here's the corrected grid CSS (this is what's "not right" in your CSS):

```css
/* grid */
.grid--3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  align-items: stretch;   /* key: all cards in a row stretch to the tallest */
}

/* card */
.card.work {
  display: flex;
  flex-direction: column;
  height: 100%;           /* fill the grid cell */
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0, 0, 0, .08);
}

/* body grows / pushes meta to bottom so text-only cards look the same size */
.card.work .work__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
}
.card.work .work__meta {
  margin-top: auto;       /* pins the meta row at the bottom of the card */
}
```

**2a. Fix the 5 text-only cards** to use the same wrapper structure as the rest (wrapping content in `<div class="work__body">`), e.g. for PingWorld:

```html
<article class="card work" data-platform="miniapp">
  <div class="work__body">
    <div class="work__head">
      <h3>拼我 PingWorld</h3>
      <span class="tag tag--miniapp">小程序</span>
    </div>
    <p>人才与时间共享平台，集中分发设计、法务、财税、开发等服务需求。</p>
    <ul class="work__meta">
      <li><b>负责</b>设计、开发、上线</li>
      <li><b>历时</b>2 个月</li>
    </ul>
  </div>
</article>
```

(Apply the same wrapper to 趣标注, vToken, 小猿题库·游戏系列, FOMOO.)

However, I **still can't locate the actual file** in this repo — a `grep` for `趣标注`, `PingWorld`, and `work__head` found nothing, so these cards don't exist in any file here yet.

Give me the file path (or the location where this works grid lives), and I'll apply these fixes directly. Which is it — should I rewrite all these cards/test content into a real file in this repo, or does the page live somewhere else?
