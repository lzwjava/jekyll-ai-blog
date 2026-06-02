---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Playwright替代Chrome命令行和ImageMagick
translated: true
type: note
---

完成。以下是变更内容：

```
之前：pandoc → Chrome CLI --screenshot → PNG → ImageMagick -trim → JPG
之后：pandoc → Playwright Chromium → 直接 JPG（精确内容尺寸）
```

使用 Playwright 重写后的改进：
- **无需 ImageMagick 依赖** — Playwright 直接输出 JPEG
- **精确内容适配** — 使用 `document.body.scrollHeight` 精确设置视口高度，无需裁剪
- **字体加载** — `wait_for_load_state("networkidle")` 确保截图前 Google Fonts 已加载
- **更简洁的流程** — 从 3 步减少到 2 步

测试结果：
```
$ ww md md2jpg /tmp/test3.md
[1/2] markdown -> HTML
[2/2] HTML -> JPG (Playwright 截图)
完成：/tmp/test3.jpg

$ file /tmp/test3.jpg
JPEG 图像数据，900x272，20K   ← 精确内容尺寸，无空白区域
```

新增依赖：
- 在 `pyproject.toml` 中添加 `playwright>=1.40.0`
- 通过 `playwright install chromium` 安装 Chromium 浏览器
