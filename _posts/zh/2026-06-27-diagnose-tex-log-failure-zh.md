---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断 TeX 日志失败
translated: true
type: note
---

我需要查看实际的 TeX 日志才能诊断失败原因。你粘贴的是 arXiv 的通用错误页面，但 "The TeX Log appears below" 这一行后面没有任何内容——实际的日志没有显示出来。

有两种方式可以继续：

**选项 A——粘贴日志。** 复制 arXiv 页面上 "The TeX Log appears below" 之后的所有内容。真正的错误就在其中（搜索 "! " 或 "Error" 或 "Fatal"）。

**选项 B——在本地复现。** 按照 arXiv 的编译方式在你的机器上编译源码，并自行读取日志：

```bash
# arXiv 使用固定的流水线。复现它：
cd sec-edgar-gpt-source/

# arXiv 使用 latexmk 配合 pdflatex（对于现代投稿最常见）
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex 2>&1 | tee build.log

# 找到真正的错误
grep -n -E "^\!|Error|Fatal|not found|Undefined" build.log
```

如果你只有 PDF 而丢失了 `.tex` 源码，那才是真正的问题——arXiv 拒绝 TeX 生成的 PDF，并且需要源码树。

基于 arXiv 列出的 5 个常见原因，这里有几个快速检查方法：

```bash
# 1. 混合的图片格式——pdflatex 需要 pdf/png/jpg，不能是 eps/ps
find . -type f \( -name '*.eps' -o -name '*.ps' \) -print
grep -rn '\\includegraphics' *.tex | grep -iE '\.eps|\.ps'

# 2. includegraphics 中的绝对/本地路径（arXiv 文件系统区分大小写）
grep -rn '\\includegraphics' *.tex | grep -E '/Users/|/home/|C:\\\\'

# 3. 文件名大小写不匹配
grep -rn '\\includegraphics' *.tex   # 与实际的 `ls` 输出对比

# 4. 自定义的 .sty/.cls 文件未打包
grep -rn '\\usepackage\|\\documentclass' *.tex
ls *.sty *.cls 2>/dev/null
```

把实际的日志（选项 A 的输出或 `build.log`）粘贴给我，我就能精确定位出错的行。没有日志我只能猜测——arXiv 的说明中明确告诉你滚动越过 hyperref 的 "Option clash" 噪音来找到真正的错误，这意味着你的实际失败埋藏在其他地方。
