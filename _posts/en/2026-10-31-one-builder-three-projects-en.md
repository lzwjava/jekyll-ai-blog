---
audio: false
generated: true
image: false
lang: en
layout: post
title: One Builder Three Projects
translated: false
type: note
---

Done. Your Marp deck is ready — all code/markdown-driven, fully editable.

## 📊 The PPT (Marp markdown)

**Source: `deck.md`** — plain Markdown, edit in any editor and re-export.

**6 slides · bilingual EN+中文 · dark theme matching the video** (#0a0a0b + gold #e3b341):

1. **Cover** — Three Projects, One Builder / 三个项目 · 一位建造者
2. **Agenda** — 01 Truth Lab · 02 Truth Software · 03 lzwjava.com
3. **Truth Lab 求真实验室** — scratch LMs · 52GB cluster · honest experiments → truthlab.cc
4. **Truth Software 求真软件** — 40+ products · 1B+ tokens/day → truthsoft.dev
5. **lzwjava.com** — AI blog · AI & software portfolios → portfolio links
6. **CTA** — Build something honest · all URLs · contact · token-based pricing

**Exported to `output/`:**

- `announcement.pdf` (6 pages, 16:9, verified Chinese chars render)
- `announcement.html` (browser view)
- `announcement.pptx` (PowerPoint)
- `previews/slide-1..6.png` (quick thumbnails)

## How to tweak

```bash
marp deck.md -o output/announcement.html          # HTML
marp deck.md -o output/announcement.pdf --pdf     # PDF (via Chrome)
marp deck.md -o output/announcement.pptx         # PPTX
```

The deck and the video (`announcement.mp4`, 55s) now share the same content and look — driven respectively by `deck.md` and `scenes.json`. Everything is in `/Users/lzwjava/projects/video-factory` with a README summarizing the build commands.

Want me to translate the deck fully into Chinese-only for a CN audience, add a speaker-notes page per slide, or embed the actual portfolio screenshots (`images/` in truth-software) into the slides?
