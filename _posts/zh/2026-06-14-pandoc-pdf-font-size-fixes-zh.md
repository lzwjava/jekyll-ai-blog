---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pandoc PDF 字体大小修复
translated: true
type: note
---

PDF 现在正确显示，共 75 页，正文 48pt，标题按比例缩放。`--pt` 标志终于正常工作。

对 `~/projects/ww/ww/pdf/pdf_base.py` 的修复总结：
1. 通过 `\renewcommand{\normalsize}` + `\AtBeginDocument` 设置字号（而非使用仅支持 10/11/12pt 的 classoption）
2. 使用临时文件通过 `--include-in-header` 注入（而非 `-V header-includes=`，后者会折叠换行符）
3. 使用 `titlesec` 控制标题字号
4. **关键**：将 `\usepackage{setspace}\setstretch{1.5}` 移入 header-includes，并移除 `-V linestretch=1.5`——pandoc 在 `\begin{document}` 后添加的 `\setstretch` 会静默覆盖我们的 `\normalsize` 设置，将其重置为 12pt