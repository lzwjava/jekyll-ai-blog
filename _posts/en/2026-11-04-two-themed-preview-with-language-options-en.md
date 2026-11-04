---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two-Themed Preview with Language Options
translated: false
type: note
---

Done — a second theme is ready (`b0cae23`), and all four previews opened side by side: **dark (espresso)** and **light (cream)**, in both 中文 and English.

## New `--theme` option

```bash
ww card --lang zh --theme dark    # 暖咖深色（默认）
ww card --lang en --theme light   # 奶油浅色
```

**light theme** (matched to the avatar's warm tones):

| Element | Color |
| --- | --- |
| Background | `(247, 240, 230)` cream |
| Left panel | `(219, 200, 175)` warm beige |
| Accent | `(180, 116, 52)` dark caramel |
| Text | `(62, 45, 32)` espresso |
| Muted/watermark | `(133, 110, 92)` warm gray-brown |

Verified: background, panel, name text, and accent divider all render at the expected colors. Dark theme is unchanged (still the default). Invalid `--theme` values are rejected with the available options listed.

Take a look at the previews and tell me which you prefer — I can also:

- make `light` the default if you like it more
- adjust specific colors (e.g. lighter beige panel, stronger caramel)
- add a third theme (e.g. a neutral gray, or something cooler to offset the warm photo)
