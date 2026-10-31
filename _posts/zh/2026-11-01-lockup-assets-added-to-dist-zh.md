---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 锁仓资产已添加至分配
translated: true
type: note
---

完成 — 已将完整标识（tower + "TruthSoft 求真软件" wordmark）添加到 `dist/`，保留仅 tower 的集合不变。

**`dist/` 中的新标识组合资源：**

- `truthsoft-lockup.svg` — 水平布局（tower 在左，wordmark 在右），矢量，206×90
- `truthsoft-lockup.png` / `truthsoft-lockup-3x.png` — 1 倍和 retina PNG
- `truthsoft-lockup-dark.svg/.png/-3x` — 深色变体，用于深色背景
- `truthsoft-lockup-stacked.svg/.png` + `-dark` — 堆叠布局（tower 在上，文字在下），170×158

**详情：**

- Wordmark 与 mockup 完全一致：*TruthSoft* 使用 Playfair Display Bold 30px（#2C1A0E / 深色时 #FAF0E0），求真软件使用 Inter Light 12px，字间距 0.26em（#8B6B50 / #9C7A5A）
- Wordmark 已作为矢量文本直接嵌入 SVG，因此无需加载网络字体即可使用 — 但工具链是项目本地的（`fonts/` + `fonts.conf` + 源 SVG 文件），因此可以随时重新渲染/编辑文本
- CJK“求真软件”通过 PingFang/Hiragino 后备字体渲染（与浏览器行为一致）
- `preview.html` 和 `README.txt` 已更新 — README 中显示了用于头部品牌的 `<img src="/dist/truthsoft-lockup.svg" width="206" height="90">`

提示：对于实际网站，最清晰的做法是在桌面端使用 SVG，仅当需要栅格后备时使用 3× PNG。在浏览器中打开 `dist/preview.html` 可同时查看所有变体 — 标识组合部分现紧邻仅 tower 的图标。
