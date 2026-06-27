---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在arXiv上设置TeX Live版本
translated: true
type: note
---

在arXiv提交过程中：

1. 上传你的 `.tex` 文件
2. arXiv 会自动检测编译器（通常是 `pdflatex` 或 `xelatex`）
3. 在 **"TeX Source"** 处理页面，你会看到一个标签为 **"TeX Live version"** 的下拉菜单或单选按钮——选择 **TeX Live 2025**（默认）或 **TeX Live 2023**

如果你没有看到该选项，它会在首次自动编译尝试后出现。只需使用默认（2025）——你的论文使用 `xelatex` 和标准包，应该能正常编译。

如果 arXiv 自动选择 `pdflatex` 并失败，你可以通过在 `.tex` 文件的第一行添加以下内容来强制使用 `xelatex`：

```
% !TEX program = xelatex
```

或者将文件重命名为 `ms.xelatex`，以便 arXiv 识别正确的编译器。