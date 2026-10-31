---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 石塔标志图形资产导出
translated: true
type: note
---

已完成。我从HTML mockup中提取了Stone Tower的logo标志，并将一组可直接使用的资源导出到了`/Users/lzwjava/projects/employment-files/logo/dist/`：

**矢量（推荐——在任何尺寸下都清晰）**
- `truthsoft-tower.svg` — 浅色塔，3:5比例（54×90 viewBox）
- `truthsoft-tower-dark.svg` — 暗色变体
- `truthsoft-square.svg` — 塔中心对齐在90×90画布上（favicon源）

**PNG图标（方形画布，透明填充）** — `icon-16 … icon-512.png`，尺寸分别为16、32、48、64、128、192、256、512像素，以及`apple-touch-icon.png`（180×180，iOS主屏幕）和`icon-dark-512.png`（用于暗色模式UI）

**多尺寸ICO** — `favicon.ico`包含256/128/64/48/32/16帧

**自然3:5 logo PNG** — `truthsoft-logo-90x150.png`、`truthsoft-logo-180x300.png`（2倍用于视网膜屏），以及`-dark`变体

**其他**
- `preview.html` — 在浏览器中打开以预览所有尺寸
- `README.txt` — 复制粘贴`<head>`代码片段、PWA的`site.webmanifest`以及header-brand标记

注意：mockup中的wordmark（"TruthSoft" Playfair Display + "求真软件"）依赖于Google Fonts，因此我只导出了塔标部分——你需要在HTML/CSS中自行渲染文字，与SVG一起构成完整logo。使用方法：将`/favicon.ico`指向`dist/favicon.ico`，在header中使用`dist/truthsoft-tower.svg`，PNG用于PWA/Apple图标。