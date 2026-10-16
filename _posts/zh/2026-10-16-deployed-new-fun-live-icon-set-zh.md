---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已部署新的Fun-Live图标集
translated: true
type: note
---

已完成。已将网站图标替换为新的 fun-live 图标集：

**变更内容：**

1. **`public/logo.png`** — 已用 `fun-live-icon-256.png` 覆盖（`/logo.png` 的 favicon 及分享/logo 引用现在都会显示新图标）
2. **`static/logo.png`** — 已同步更新（这是 git 跟踪的副本，已由 nginx 提供）
3. **`public/fun-live-icon/`** — 已复制完整图标集（32/48/64/128/160/256/512/1024 PNG + SVG）
4. **`public/apple-touch-icon.png`** — 已生成 180×180 版本（从 256 PNG 调整大小），用于 iOS 主屏幕图标
5. **`index.html`** — 已添加正确的 favicon 链接：SVG 图标优先，然后是 PNG 各尺寸图标（32–256px），外加 apple-touch-icon，并保留 `/logo.png` 作为回退

注意：`deploy.sh` 运行 `vite build`（outDir `static`），因此下次部署时会自动从 `public/` 重新生成 `static/` — 直接更新 `static/logo.png` 只是覆盖当前线上文件。
