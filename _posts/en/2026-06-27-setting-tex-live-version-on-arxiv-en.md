---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting TeX Live version on arXiv
translated: false
type: note
---

In the arXiv submission process:

1. Upload your `.tex` file(s)
2. arXiv auto-detects the compiler (usually `pdflatex` or `xelatex`)
3. On the **"TeX Source"** processing page, you'll see a dropdown or radio button labeled **"TeX Live version"** — select **TeX Live 2025** (default) or **TeX Live 2023**

If you don't see the option, it appears after the first auto-compilation attempt. Just proceed with the default (2025) — your paper uses `xelatex` with standard packages, it should compile fine.

If arXiv auto-selects `pdflatex` and fails, you can force `xelatex` by adding this as the first line of your `.tex`:

```
% !TEX program = xelatex
```

Or rename your file to `ms.xelatex` so arXiv picks up the correct compiler.
