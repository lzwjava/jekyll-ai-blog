---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重新设计的网站带有真实品牌标志资源
translated: true
type: note
---

完成。所有资源均可正常解析——以下是我所做的：

**从 `/Users/lzwjava/projects/employment-files/logo/dist` 复制了真实的 TruthSoft logo 资源到 `logo/`：**

- `truthsoft-tower.svg` / `truthsoft-tower-dark.svg`（矢量塔形标志，浅色 + 深色）
- `favicon.ico`、`apple-touch-icon.png`、`icon-192/512.png`（应用/PWA 图标）
- `truthsoft-lockup*.svg`（横向 + 堆叠 lockup，可供后续打印/hero 使用）

**替换了站点中的占位品牌标识：**

- **Favicon** —— `index.html` 和 `portfolio.html` 都将 emoji/data-URI favicon 替换为 `logo/favicon.ico` + 清晰的矢量 `truthsoft-tower.svg`，并为 iOS 添加 `apple-touch-icon.png`。
- **导航品牌标志** —— `style.css` 中通用渐变圆形现已替换为实际的石塔标志（19×32，原生 3:5 比例），并且当站点处于 dark mode 时，它会自动切换为深色调变体（`truthsoft-tower-dark.svg`）。

导航中的 wordmark 文本（“求真软件” ↔ “TruthSoft”）仍作为塔形标志旁边的实时 HTML/CJK 文本保留，因此现有的 `i18n.js` 中/英切换继续有效——只有 `logo/truthsoft-lockup*.svg` 文件将 wordmark 以矢量文本形式内置，所以我按照 logo README 自身的建议，未将它们放入导航中。
