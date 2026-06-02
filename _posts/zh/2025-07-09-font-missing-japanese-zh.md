---
audio: false
generated: true
lang: zh
layout: post
title: 修复日文字体缺字问题
translated: true
type: note
---

您遇到的错误表明 LaTeX 文档中使用的 `FandolSong` 字体（包括常规和粗体变体）缺少某些日语字符所需的字形，例如 `ー`（U+30FC，片假名-平假名长音符号）、`専`（U+5C02）、`証`（U+8A3C）和 `発`（U+767A）。这导致 XeLaTeX 在编译文档（很可能是 `resume-ja.tex` 或 `latex/ja/resume-ja/` 中的相关文件）时报告“缺少字符”错误。

`FandolSong` 字体主要为中文文本设计，缺乏对日语字符的完整支持，这解释了为何会缺少这些字形。要解决此问题，您需要切换到支持日语字符的字体，例如之前推荐的 `Noto Sans CJK JP` 或 `IPAGothic`。下面我将指导您通过更新字体配置并确保与您的日语翻译简历兼容来修复此问题。

### 问题原因
- **字体限制**：`FandolSong` 是 TeX Live 中包含的用于 CJK 排版的字体，但不包含所有日语字符，尤其是片假名（`ー`）和日语中常用的汉字。
- **XeLaTeX 和 xeCJK**：您的文档很可能使用了 `xeCJK` 宏包，它依赖于指定的 CJK 字体（本例中为 `FandolSong`）来处理日语文本。当缺少字形时，XeLaTeX 会记录错误并可能在输出的 PDF 中省略这些字符。
- **翻译部分**：由于您正在将 `blogposts.tex` 等部分翻译成日语，翻译后的文本包含了 `FandolSong` 无法渲染的日语字符。

### 解决方案：更改 CJK 字体
您需要更新 LaTeX 文档的字体配置，以使用兼容日语的字体。根据您之前的消息，您使用的是 Linux 系统，并且有一个字体配置块，我假设您正在使用 XeLaTeX 配合 `xeCJK` 以及用于字体选择的 `ifthenelse` 结构。

#### 步骤 1：安装兼容日语的字体
确保您的 Linux 系统上安装了支持日语的字体。推荐使用 `Noto Sans CJK JP`，它广泛可用并支持所有必要的日语字形。

在 Ubuntu/Debian 上安装 `Noto Sans CJK JP`：
```bash
sudo apt-get install fonts-noto-cjk
```
在 Fedora 上：
```bash
sudo dnf install google-noto-cjk-fonts
```
在 Arch Linux 上：
```bash
sudo pacman -S noto-fonts-cjk
```

或者，您可以使用 `IPAGothic` 或 `IPAexGothic`：
```bash
sudo apt-get install fonts-ipaexfont
```

验证字体是否已安装：
```bash
fc-list :lang=ja | grep Noto
```
您应该看到类似 `Noto Sans CJK JP` 或 `Noto Serif CJK JP` 的条目。如果使用 IPA 字体：
```bash
fc-list :lang=ja | grep IPA
```

#### 步骤 2：更新 LaTeX 字体配置
修改您的 LaTeX 文档（很可能是 `resume-ja.tex` 或共享的前言文件）中的字体配置，以使用兼容日语的字体。根据您之前的字体设置，以下是更新配置的方法：

```latex
\ifthenelse{\equal{\fontsystem}{linux}}{
    % Linux 字体
    \setCJKmainfont{Noto Sans CJK JP} % 日语主字体
    \setCJKsansfont{Noto Sans CJK JP} % 日语无衬线字体
    \setCJKmonofont{Noto Sans Mono CJK JP} % 日语等宽字体
    \setmainfont{Liberation Serif} % 英文字体
}
```

如果 `Noto Sans Mono CJK JP` 不可用，您可以使用 `Source Code Pro` 或 `DejaVu Sans Mono` 处理非 CJK 等宽文本，但要确保日语代码块使用 CJK 字体：
```latex
\setCJKmonofont{Noto Sans CJK JP}
```

如果您更喜欢 `IPAGothic`：
```latex
\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{IPAexGothic}
    \setCJKsansfont{IPAexGothic}
    \setCJKmonofont{IPAexMincho} % 或者使用 Noto Sans CJK JP 作为等宽字体
    \setmainfont{Liberation Serif}
}
```

#### 步骤 3：验证 xeCJK 使用情况
确保您的 LaTeX 文档正确使用了 `xeCJK` 宏包并应用了字体设置。`resume-ja.tex` 的最小示例可能如下所示：

```latex
\documentclass[a4paper]{article}
\usepackage{xeCJK}
\usepackage{ifthenelse}

% 字体系统检测
\newcommand{\fontsystem}{linux}

\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{Noto Sans CJK JP}
    \setCJKsansfont{Noto Sans CJK JP}
    \setCJKmonofont{Noto Sans Mono CJK JP}
    \setmainfont{Liberation Serif}
}

\begin{document}

% 来自 blogposts.tex 的日语文本
\section{ブログ投稿}
こんにちは、私の名前は李智维です。最新の技術に関する記事を書いています。

% 英语文本
\section{Introduction}
Hello, my name is Zhiwei Li.

\end{document}
```

如果您的简历使用了像 `awesome-cv` 这样的模板，请确保前言部分包含了 `xeCJK` 和上述字体设置。例如，在 `awesome-cv.cls` 或 `resume-ja.tex` 中添加：

```latex
\RequirePackage{xeCJK}
\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{Noto Sans CJK JP}
    \setCJKsansfont{Noto Sans CJK JP}
    \setCJKmonofont{Noto Sans Mono CJK JP}
    \setmainfont{Liberation Serif}
}
```

#### 步骤 4：重新编译文档
导航到日语简历目录并重新编译：
```bash
cd latex/ja/resume-ja
xelatex resume-ja.tex
```

检查日志文件（`resume-ja.log`）中的“缺少字符”错误。如果字体设置正确，这些错误应该消失，并且 PDF 应正确显示 `ー`、`専`、`証` 和 `発` 等日语字符。

#### 步骤 5：如果错误仍然存在，进行调试
如果您仍然看到“缺少字符”错误：
1.  **确认字体名称**：确保字体名称与 `fc-list` 中列出的完全匹配。例如，某些系统列出的是 `Noto Sans CJK JP Regular` 而不是 `Noto Sans CJK JP`。调整 LaTeX 配置：
    ```latex
    \setCJKmainfont{Noto Sans CJK JP Regular}
    ```
2.  **检查 xeCJK 配置**：确保 `xeCJK` 在字体设置之前加载，并且没有其他宏包覆盖 CJK 字体设置。例如，避免加载带有冲突设置的 `fontspec`。
3.  **测试最小文档**：创建一个包含日语文本的最小 LaTeX 文件来隔离问题：
    ```latex
    \documentclass{article}
    \usepackage{xeCJK}
    \setCJKmainfont{Noto Sans CJK JP}
    \begin{document}
    こんにちは、専ー証発
    \end{document}
    ```
    使用 `xelatex` 编译并检查错误。
4.  **备用字体**：如果 `Noto Sans CJK JP` 不起作用，请尝试 `Source Han Sans JP` 或 `IPAexGothic`。使用 `fc-list :lang=ja` 列出可用字体，并相应地更新配置。

#### 步骤 6：更新翻译部分
由于您使用 Python 脚本来翻译 `blogposts.tex` 等部分，请确保翻译后的文件（`latex/ja/resume-ja/blogposts.tex`）通过 `\input{blogposts}` 包含在 `resume-ja.tex` 中。您提供的脚本已经正确替换了文件，因此无需更改。只需在必要时重新运行翻译：
```bash
python translate_section.py --section blogposts.tex --lang ja --kind resume
```

然后重新编译 `resume-ja.tex` 以包含更新后的部分。

### 补充说明
- **字体粗细**：`Noto Sans CJK JP` 支持多种粗细（Regular、Bold 等），因此 `\textbf{}` 应该适用于日语文本。如果使用 `IPAexGothic`，请确保粗体变体（`IPAexGothic Bold`）可用或调整配置。
- **模板兼容性**：如果您使用的是像 `awesome-cv` 这样的模板，请检查它是否在 `.cls` 文件中覆盖了字体设置。您可能需要在主文档（`resume-ja.tex`）中应用 `xeCJK` 设置。
- **PDF 输出**：检查生成的 PDF 以确保日语字符正确渲染。如果字符显示为方框，则字体仍然不正确或未正确嵌入。
- **系统字体缓存**：安装新字体后，更新字体缓存：
  ```bash
  fc-cache -fv
  ```

### 示例输出
应用修复后，您在 `latex/ja/resume-ja/` 中的 `blogposts.tex` 可能包含如下日语文本：
```latex
\section{ブログ投稿}
\item 技術ブログ: 最新のAI技術について書いています。専門的な内容をわかりやすく説明します。
```
当使用 `Noto Sans CJK JP` 编译时，像 `ー`、`専`、`証` 和 `発` 这样的字符应该在 PDF 中正确渲染。

如果您遇到更多错误或需要有关简历模板特定部分的帮助，请分享相关的 LaTeX 代码（例如 `resume-ja.tex` 的前言或模板的字体设置），我可以提供更有针对性的修复方案！
