---
audio: false
generated: true
lang: zh
layout: post
title: 中重字体段落样式重构
translated: true
type: note
---

要将整个 `cvparagraph` 环境从使用 `\bodyfontlight` 改为 `\mdseries`，你需要重新定义 `\paragraphstyle` 命令。将此代码添加到加载 awesome-cv 类后的导言区：

```latex
\renewcommand*{\paragraphstyle}{\fontsize{11pt}{1em}\mdseries\upshape\color{text}}
```

这将把段落样式从：

- `\bodyfontlight`（细字体）

改为：

- `\mdseries`（中等字体，与描述样式类似）

这样，你的整个 `cvparagraph` 环境将使用与 `\descriptionstyle` 相同的中等字重字体系列。
