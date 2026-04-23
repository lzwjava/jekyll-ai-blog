---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 文档转图片步骤
translated: true
type: note
---

以下是我们使用的流程：

**Markdown → HTML → PDF → PNG**

```bash
# 1. Markdown → HTML (pandoc，使用内联 CSS)
pandoc input.md -o output.html --standalone \
  --metadata title="标题" \
  --variable "css=body{...}"

# 2. HTML → PDF (Chrome headless 模式)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --print-to-pdf=output.pdf \
  --no-pdf-header-footer \
  "file:///absolute/path/to/output.html"

# 3. PDF → PNG 分页 (ImageMagick)
magick -density 150 output.pdf -quality 95 page-%02d.png

# 4. 将所有页面拼接为一张图片
magick page-00.png page-01.png page-02.png page-03.png \
  -append final.png
```

**各步骤的作用：**
- `pandoc` 负责解析 markdown 并生成包含自定义 CSS 的纯净 HTML
- Chrome headless 模式能够精确渲染 HTML（字体、表格、布局），并将其导出为 PDF
- ImageMagick 将 PDF 页面按指定 DPI（`-density 150`）转换为 PNG 位图
- `-append` 将所有页面垂直堆叠成一张长图

**关键注意事项：** Chrome headless 在 `file://` 模式下会阻止加载外部 CDN CSS —— 请通过 `--variable "css=..."` 内联 CSS 样式。