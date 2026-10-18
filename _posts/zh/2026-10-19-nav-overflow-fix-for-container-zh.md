---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 容器导航溢出修复
translated: true
type: note
---

完成。导航在英文中溢出了 1080px 容器（11 个链接 + 2 个按钮），导致 "Truth Software" 被迫换行。`style.css` 中的更改（`index.html` 和 `portfolio.html` 共享）：

1. **`.nav__brand`** — 添加了 `white-space: nowrap`，使品牌永远不会换行成两行，并将字体从 17px 减小到 16px。
2. **`.nav__links`** — 将间距从 18px 减小到 10px。
3. **`.nav__links a`** — 将字体从 14.5px 减小到 13.5px。
4. **新增 `@media (max-width: 1000px)`** — 进一步压缩间距（gap 8px，字体 13px，更紧凑的 CTA 内边距），适用于 800–1000px 的屏幕，此时所有链接仍然可见。低于 800px 时，现有规则已经隐藏了非 CTA 链接。

现在品牌在所有宽度下都保持在一行，完整的链接集在约 800px 宽度内也能容纳。
