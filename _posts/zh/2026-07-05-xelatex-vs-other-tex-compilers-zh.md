---
audio: false
generated: true
image: false
lang: zh
layout: post
title: XeLaTeX与其他TeX编译器
translated: true
type: note
---

**问题：** 比较 XeLaTeX 与其他 TeX 编译器（pdfLaTeX、LuaLaTeX 等）——它们之间的区别是什么，以及何时应使用哪种编译器？

**答案：**

## 引擎概览

实际会遇到四种引擎。它们都在顶层运行相同的宏层（LaTeX）——"编译器"的区别在于底层的*引擎*。

| 引擎 | 输出 | 字体 | Unicode | 速度 | 可扩展性 |
|---|---|---|---|---|---|
| pdfTeX（`pdflatex`） | 直接生成 PDF | 传统字体（Type1/TFM，8 位） | 不支持（通过 `inputenc` 变通） | 最快 | microtype（字符突出与字宽扩展） |
| XeTeX（`xelatex`） | 通过 `xdvipdfmx` 生成 PDF | 系统字体（通过 `fontspec` 使用 OpenType/TrueType） | 原生 UTF-8 | 中等 | 有限；仅支持字符突出，不支持字宽扩展 |
| LuaTeX（`lualatex`） | 直接生成 PDF | 通过 `fontspec`（以 Lua 方式加载）使用系统字体 | 原生 UTF-8 | 冷启动最慢 | 引擎内嵌 Lua 脚本——可完全访问节点列表 |
| (u)pTeX / 经典 `latex`+`dvips` | DVI → PS/PDF | 传统字体 | 不支持（pTeX：日语专用） | 快 | 小众领域（日语排版，PSTricks） |

## 基本原理：真正的区别在哪

核心差异在于**文本如何变为字形**。

**pdfTeX** 本质上是一个 8 位系统。每个"字符"都是一个字节；UTF-8 输入是通过 `\usepackage[utf8]{inputenc}` 将多字节序列解码为宏调用来模拟的。字体是古老的 TFM 度量加上 Type1 世界——你不能直接指向 Mac 上的 `PingFang.ttc`；必须有人将字体打包为 TeX 可用格式（这正是 `lmodern`、`newtx` 等包的作用）。

**XeTeX** 的核心思路：将文本塑形交给操作系统相关的堆栈处理。它读取原生 UTF-8，并使用 HarfBuzz（之前是 ICU）来塑造 OpenType 字体——连字、上下文变体、中日韩文字、阿拉伯文、天城文都能直接使用。在内部，它仍然生成一种扩展的 DVI（`.xdv`），然后由 `xdvipdfmx` 转换为 PDF——正是这种间接性导致一些 pdfTeX 特有的 PDF 原语在 XeTeX 中不存在。

**LuaTeX** 采取了相反的方法：它没有在 TeX 上外挂一个塑形器，而是重写了引擎，嵌入了一个 Lua 解释器，并将 TeX 的内部结构（节点列表、回调函数、字体加载器）以 Lua API 的形式暴露出来。字体加载是通过 *Lua*（`luaotfload`）完成的，因此是可编程的——你可以拦截段落构建器、修改字形节点、在排版时生成内容。这就是为什么 LuaLaTeX 现在被官方推荐为 LaTeX 开发的"现代"引擎；LaTeX 团队的新功能（例如，带标签/可访问的 PDF）首先在它上面实现。

## 实用决策树

```
需要 Lua 脚本、高级 microtype 功能或前沿的 LaTeX 功能？  → lualatex
需要中日韩文字/阿拉伯文/系统字体，且 lualatex 对你来说太慢？ → xelatex
纯英文/拉丁文文档、期刊模板、追求最高速度 + microtype？  → pdflatex
期刊/arXiv 强制使用特定引擎？                          → 按他们的要求来
```

具体场景：

- **中文文档**：`ctex` 包两者都支持，但 `xelatex` 历来是 `ctexart` 的默认选择，并且在中日韩文字方面经过充分验证。`lualatex` + `luatexja` 现在也能很好地工作。
- **arXiv / 许多期刊**：pdfLaTeX 仍然是最安全的投稿目标；arXiv 支持 XeLaTeX，但要求更严格。
- **使用自定义品牌字体的 Beamer 演示**：XeLaTeX 或 LuaLaTeX（你需要 `fontspec`）。
- **使用系统字体的简历/求职信**：XeLaTeX 是经典选择（大多数简历模板如 moderncv/awesome-cv 都假定使用它）。

## 最小工作示例

pdfLaTeX（传统字体世界）：

```latex
\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}  % 在现代 LaTeX 中无实际作用，为清晰起见保留
\usepackage{lmodern}
\usepackage{microtype}       % 仅在 pdftex/luatex 上发挥全部功能
\begin{document}
Hello, world.
\end{document}
```

XeLaTeX / LuaLaTeX（同一源码适用于两者）：

```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Source Serif 4}       % 任意已安装的 OpenType 字体
% 中日韩文字：
% \usepackage{xeCJK}               % xelatex
% \setCJKmainfont{PingFang SC}
\begin{document}
Hello, 你好, مرحبا — 全部是原生 UTF-8。
\end{document}
```

在可移植导言区中进行引擎检测：

```latex
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}\usepackage{lmodern}
\else
  \usepackage{fontspec}
\fi
```

构建命令（在 M2 Air 上，`brew install --cask mactex-no-gui`）：

```bash
latexmk -pdf doc.tex          # pdflatex
latexmk -xelatex doc.tex
latexmk -lualatex doc.tex
```

## 值得注意的陷阱

- **速度**：pdfLaTeX 在冷编译时比 LuaLaTeX 快约 2–5 倍；LuaLaTeX 的 Lua 字体加载器占用了启动时间。对于持续不断地重建文档的 CI 流水线来说，这一点很重要。`lualatex --luaonly` 缓存和 `luahbtex`（自 TeX Live 2020 以来的默认二进制文件，使用 HarfBuzz 塑形）缩小了差距。
- **microtype**：字宽扩展（为更好的对齐而对字形进行细微拉伸）在 pdfTeX 和 LuaTeX 上有效，但在 *XeTeX* 上*无效*——XeTeX 只能使用字符突出。如果你关心排版灰度，LuaLaTeX > XeLaTeX。
- **`\special`/PDF 原语**：进行底层 PDF 操作的包（某些 tikz 外部化设置、`pdfpages` 的边界情况、媒体嵌入）在 XeTeX 上表现不同，这是由于 `.xdv` → PDF 的间接性。
- **XeTeX 的未来**：它处于维护模式——稳定，但新的开发精力（LaTeX3、带标签的 PDF、`luametatex`/ConTeXt）都集中在 Lua 这一侧。对于新的长期项目，除非你有 XeTeX 特定的需求（比如对 `xeCJK` 的操作习惯），否则优先选择 LuaLaTeX。
- **Tectonic**：值得在你的 CLI 代理工作流中一试——一个用 Rust 封装的 XeTeX，具有自动依赖获取、单一二进制文件、可重现构建等特点。`brew install tectonic; tectonic doc.tex`，它会只下载所需的包。非常适合自动化，无需 5GB 的 TeX Live 安装。

## 针对你的配置的 TL;DR

对于你的博客/笔记 PDF 流水线：**LuaLaTeX** 如果是全新开始（面向未来、可脚本化——你甚至可以通过 Lua 生成内容，这符合你的自动化风格），**XeLaTeX** 如果你在做中文文档并使用现有的 `xeCJK` 模板，**pdfLaTeX** 仅当期刊或 arXiv 强制要求时使用。**Tectonic** 如果你希望将整个工具作为一个干净的 CLI 依赖项集成到代理流水线中。