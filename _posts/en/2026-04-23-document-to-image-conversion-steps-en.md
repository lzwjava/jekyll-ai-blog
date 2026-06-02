---
audio: false
generated: true
image: false
lang: en
layout: post
title: Document to Image Conversion Steps
translated: false
type: note
---

Here's the pipeline we used:

**Markdown → HTML → PDF → PNG**

```bash
# 1. Markdown → HTML (pandoc, with inline CSS)
pandoc input.md -o output.html --standalone \
  --metadata title="Title" \
  --variable "css=body{...}"

# 2. HTML → PDF (Chrome headless)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --print-to-pdf=output.pdf \
  --no-pdf-header-footer \
  "file:///absolute/path/to/output.html"

# 3. PDF → PNG pages (ImageMagick)
magick -density 150 output.pdf -quality 95 page-%02d.png

# 4. Stitch pages into one image
magick page-00.png page-01.png page-02.png page-03.png \
  -append final.png
```

**Why each step:**
- `pandoc` handles markdown parsing and produces clean HTML with custom CSS
- Chrome headless renders the HTML faithfully (fonts, tables, layout) and exports to PDF
- ImageMagick converts PDF pages to raster PNG at a chosen DPI (`-density 150`)
- `-append` stacks pages vertically into one tall image

**Key gotcha:** Chrome headless blocks external CDN CSS in `file://` mode — inline the CSS via `--variable "css=..."` instead.
