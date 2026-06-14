---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pandoc PDF Font Size Fixes
translated: false
type: note
---

PDF is now correct at 75 pages with 48pt body text and proportional headings. The `--pt` flag finally works properly.

Summary of fixes to `~/projects/ww/ww/pdf/pdf_base.py`:

1. Font size via `\renewcommand{\normalsize}` + `\AtBeginDocument` (not classoption, which only supports 10/11/12pt)
2. `--include-in-header` with temp file (not `-V header-includes=`, which collapses newlines)
3. `titlesec` for heading size control
4. **Critical**: moved `\usepackage{setspace}\setstretch{1.5}` into header-includes and removed `-V linestretch=1.5` — pandoc's `\setstretch` after `\begin{document}` was silently overriding our `\normalsize` back to 12pt
