---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepCompute标志推广完成
translated: true
type: note
---

已完成。DeepCompute icon 现在是整个站点使用的 logo。

**我做了什么：**

1. **生成了 logo assets**，在 `logo/` 中基于 `zhiwei_deepcompute_logo_icon_1024px.png`：
   - `deepcompute-icon.png`（256px）——新的 nav logo
   - `favicon.ico`——使用 16/24/32/48/64px 尺寸重新构建
   - `apple-touch-icon.png`（180px）、`icon-192.png`、`icon-512.png`——根据新标识刷新

2. **HTML**（`index.html`、`portfolio.html`）：将 `truthsoft-tower.svg` favicon 链接替换为 `logo/deepcompute-icon.png`。

3. **CSS**（`style.css`）：
   - `.nav__logo` 现在是一个使用 `deepcompute-icon.png` 的方形 28×28 icon（原为 19×32 的高塔 SVG）
   - 移除了 `html[data-theme="dark"] .nav__logo` override，因为同一个 icon 在两种主题下都适用

需要注意一点：该 icon 是一个浅色（白色方块 + 紫色标记）logo，因此在 dark mode 下会显示为白色方块，而在 light mode 下该方块会融入白色 nav，只留下紫色标记可见——两种模式下都清晰可读。

旧的 `truthsoft-tower*.svg` 和 `truthsoft-lockup*.svg` 文件仍在 `logo/` 中，但已不再被任何地方引用。需要我删除它们，还是保留？