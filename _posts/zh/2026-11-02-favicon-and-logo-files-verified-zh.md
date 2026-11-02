---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Favicon 和徽标文件已验证
translated: true
type: note
---

是的，logo 在浏览器标签页中显示正常。已验证：

**文件存在且有效**
- `logo/favicon.ico` — 有效的 ICO，包含 5 种尺寸（16×16、24×24、32×32、48×48、64×64）
- `logo/deepcompute-icon.png` — 256×256 RGBA PNG（现代浏览器优先选择的 fallback 图标）
- `logo/apple-touch-icon.png` — 180×180，用于 iOS/iPhone

**HTML 中的引用**（`index.html` 和 `portfolio.html` 两者中均有）：
```html
<link rel="icon" href="logo/favicon.ico" sizes="any">
<link rel="icon" href="logo/deepcompute-icon.png" type="image/png">
<link rel="apple-touch-icon" href="logo/apple-touch-icon.png">
```

**`cases/` 中全部 12 个 case 页面**都正确使用了父级相对路径 `../logo/favicon.ico`。

**图标内容** — 非空白/空内容：约 70% 不透明像素（浅灰色，带蓝色/紫色点缀，与 SVG 源文件中的“tower”标记一致），四角为透明背景。

**服务检查** — 本地服务器测试对根页面和 case 页面上的所有图标文件均返回 HTTP 200，且 content type 正确（`image/x-icon`、`image/png`）。

一个小提示：浏览器标签页图标会被强力缓存，因此如果你最近更改了 logo，可能需要强制刷新（Cmd+Shift+R）才能看到更新。