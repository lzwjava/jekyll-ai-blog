---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 --pt 字体大小 Bug
translated: true
type: note
---

## 如何修复 `ww pdf markdown-pdf` 中的 `--pt` 字号 bug

### 问题

CLI 中确实存在 `--pt` 选项，但对实际的 PDF 输出没有任何影响。无论传入什么 `--pt` 值，正文文本始终为 12pt。

### 根本原因（多层叠加）

**Bug 1：LaTeX `article` 类忽略非标准类选项**

原始代码将 `--pt 48` 作为 `-V classoption=48pt` 传递，这会生成 `\documentclass[48pt]{article}`。但 LaTeX 的 `article` 类仅支持 `10pt`、`11pt`、`12pt`——任何其他值都会**静默忽略**并给出警告。因此 `--pt 48` 没有效果。

**修复**：使用 `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` 代替类选项。

**Bug 2：`-V header-includes=` 会折叠换行符**

当我们改用 `-V header-includes=\renewcommand{...}\n\usepackage{titlesec}\n...` 时，pandoc 的 `-V` 选项将整个值视为单个字符串，将 `\n` 折叠为字面字符。多个 LaTeX 命令写在一行 = 语法错误或被忽略。

**修复**：将 header-includes 内容写入一个临时 `.tex` 文件，并使用 `--include-in-header <file>` 代替。Pandoc 会逐字读取该文件，保留所有换行符。pandoc 退出后清理临时文件。

**Bug 3：需要 `titlesec` 包来控制标题**

即使 `\normalsize` 已正确设置为 48pt，LaTeX 的 `\section` 命令仍使用其自身硬编码的字号公式（如 `\Large`、`\large`），这些公式并不引用 `\normalsize`。因此，当正文文本变大时，标题仍保持类的默认值。

**修复**：添加 `\usepackage{titlesec}` 和显式的 `\titleformat` 命令：
```
\titleformat{\section}{\bfseries\fontsize{62}{74}\selectfont}{}{}{}
\titleformat{\subsection}{\bfseries\fontsize{55}{66}\selectfont}{}{}{}
\titleformat{\subsubsection}{\bfseries\normalsize}{}{}{}
```

**Bug 4（最终、最难的那个）：`setspace` 包的 `\setstretch` 覆盖了 `\normalsize`**

这是最隐蔽的 bug。原始代码使用 `-V linestretch=1.5` 设置行间距。Pandoc 的模板生成：
```latex
% 在导言区：
\usepackage{setspace}

% 在 \begin{document} 之后：
\setstretch{1.5}
```

`setspace` 包的 `\setstretch` 命令会在内部**重新定义 `\normalsize`**，将其恢复为类的默认值（12pt）并应用新的拉伸因子。因此执行顺序为：

1. `\documentclass[12pt]{article}` → `\normalsize` = 12pt
2. `\usepackage{setspace}` → 加载包
3. 我们的 `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` → `\normalsize` = 48pt ✓
4. `\AtBeginDocument{\normalsize}` → 在文档开始时应用 48pt ✓
5. `\setstretch{1.5}`（在 `\begin{document}` 之后）→ **将 `\normalsize` 重新定义为 12pt** ✗

第 5 步静默地撤销了所有设置。我们通过编译一个不带 setspace 的最小 .tex 文件确认了这一点——正文文本正确显示为 48pt。重新添加 setspace 后问题复现。

**修复**：在我们自己的 `--include-in-header` 文件中先包含 `\usepackage{setspace}` 和 `\setstretch{1.5}`，**然后再**包含我们的 `\renewcommand{\normalsize}`。从 pandoc 命令中移除 `-V linestretch=1.5`。这样处理顺序为：

1. `\usepackage{setspace}` → 加载包
2. `\setstretch{1.5}` → 设置拉伸，将 `\normalsize` 重新定义为 12pt+拉伸
3. `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` → **覆盖**回 48pt
4. `\AtBeginDocument{\normalsize}` → 在文档开始时应用 48pt
5. 在 `\begin{document}` 之后不再有 `\setstretch` → 48pt 持续有效 ✓

### 验证

- 修复前：9 页（正文文本始终固定在 12pt，无论 `--pt` 是多少）
- 修复后：`--pt 48` 时为 75 页（正文文本真正为 48pt，标题 62pt，子标题 55pt）

### 修改的文件

`~/projects/ww/ww/pdf/pdf_base.py`——`text_to_pdf_from_markdown()` 函数。关键更改：
- 移除 `-V classoption={pt}pt`（无效）
- 移除 `-V header-includes=...`（折叠换行符）
- 移除 `-V linestretch=1.5`（覆盖了 normalsize）
- 添加 `--include-in-header` 以及包含以下内容的临时文件：setspace + setstretch + titlesec + renewcommand normalsize + titleformat 命令