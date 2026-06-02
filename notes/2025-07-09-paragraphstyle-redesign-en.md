---
audio: false
generated: true
lang: en
layout: post
title: Redefine Paragraph Style for Medium Weight
translated: false
type: note
---

To change the whole `cvparagraph` environment to use `\mdseries` instead of `\bodyfontlight`, you need to redefine the `\paragraphstyle` command. Add this to your preamble after loading the awesome-cv class:

```latex
\renewcommand*{\paragraphstyle}{\fontsize{11pt}{1em}\mdseries\upshape\color{text}}
```

This will change the paragraph style from:

- `\bodyfontlight` (which is light weight)

to:

- `\mdseries` (which is medium weight, similar to the description style)

This way, your entire `cvparagraph` environment will use the medium weight font series like the `\descriptionstyle` does.
