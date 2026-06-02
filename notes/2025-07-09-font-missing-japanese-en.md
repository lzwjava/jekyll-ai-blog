---
audio: false
generated: true
lang: en
layout: post
title: Fix Missing Japanese Font Glyphs
translated: false
type: note
---

The errors you're encountering indicate that the font `FandolSong` (both Regular and Bold variants) used in your LaTeX document does not contain the necessary glyphs for certain Japanese characters, such as `ー` (U+30FC, Katakana-Hiragana Prolonged Sound Mark), `専` (U+5C02), `証` (U+8A3C), and `発` (U+767A). This is causing XeLaTeX to report "Missing character" errors when compiling your document, likely `resume-ja.tex` or a related file in `latex/ja/resume-ja/`.

The `FandolSong` font is primarily designed for Chinese text and lacks full support for Japanese characters, which explains the missing glyphs. To resolve this, you need to switch to a font that supports Japanese characters, such as `Noto Sans CJK JP` or `IPAGothic`, as recommended previously. Below, I’ll guide you through fixing the issue by updating your font configuration and ensuring compatibility with your Japanese-translated resume.

### Why This Happens
- **Font Limitation**: `FandolSong` is a Chinese font included in TeX Live for CJK typesetting but does not include all Japanese characters, especially katakana (`ー`) and common kanji used in Japanese.
- **XeLaTeX and xeCJK**: Your document likely uses the `xeCJK` package, which relies on the specified CJK font (`FandolSong` in this case) for Japanese text. When glyphs are missing, XeLaTeX logs errors and may omit the characters in the output PDF.
- **Translated Section**: Since you’re translating sections like `blogposts.tex` to Japanese, the translated text contains Japanese characters that `FandolSong` cannot render.

### Solution: Change the CJK Font
You need to update your LaTeX document’s font configuration to use a Japanese-compatible font. Since your previous message indicated a Linux system and a font configuration block, I’ll assume you’re using XeLaTeX with `xeCJK` and the `ifthenelse` structure for font selection.

#### Step 1: Install a Japanese-Compatible Font
Ensure a font with Japanese support is installed on your Linux system. The recommended font is `Noto Sans CJK JP`, which is widely available and supports all necessary Japanese glyphs.

To install `Noto Sans CJK JP` on Ubuntu/Debian:
```bash
sudo apt-get install fonts-noto-cjk
```
On Fedora:
```bash
sudo dnf install google-noto-cjk-fonts
```
On Arch Linux:
```bash
sudo pacman -S noto-fonts-cjk
```

Alternatively, you can use `IPAGothic` or `IPAexGothic`:
```bash
sudo apt-get install fonts-ipaexfont
```

Verify the font is installed:
```bash
fc-list :lang=ja | grep Noto
```
You should see entries like `Noto Sans CJK JP` or `Noto Serif CJK JP`. If using IPA fonts:
```bash
fc-list :lang=ja | grep IPA
```

#### Step 2: Update LaTeX Font Configuration
Modify the font configuration in your LaTeX document (likely `resume-ja.tex` or a shared preamble file) to use a Japanese-compatible font. Based on your earlier font setup, here’s how to update the configuration:

```latex
\ifthenelse{\equal{\fontsystem}{linux}}{
    % Linux fonts
    \setCJKmainfont{Noto Sans CJK JP} % Main font for Japanese
    \setCJKsansfont{Noto Sans CJK JP} % Sans-serif font for Japanese
    \setCJKmonofont{Noto Sans Mono CJK JP} % Monospace font for Japanese
    \setmainfont{Liberation Serif} % English font
}
```

If `Noto Sans Mono CJK JP` is unavailable, you can use `Source Code Pro` or `DejaVu Sans Mono` for non-CJK monospace text, but ensure Japanese code blocks use a CJK font:
```latex
\setCJKmonofont{Noto Sans CJK JP}
```

If you prefer `IPAGothic`:
```latex
\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{IPAexGothic}
    \setCJKsansfont{IPAexGothic}
    \setCJKmonofont{IPAexMincho} % Or Noto Sans CJK JP for monospace
    \setmainfont{Liberation Serif}
}
```

#### Step 3: Verify xeCJK Usage
Ensure your LaTeX document uses the `xeCJK` package and applies the font settings correctly. A minimal example for `resume-ja.tex` might look like:

```latex
\documentclass[a4paper]{article}
\usepackage{xeCJK}
\usepackage{ifthenelse}

% Font system detection
\newcommand{\fontsystem}{linux}

\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{Noto Sans CJK JP}
    \setCJKsansfont{Noto Sans CJK JP}
    \setCJKmonofont{Noto Sans Mono CJK JP}
    \setmainfont{Liberation Serif}
}

\begin{document}

% Japanese text from blogposts.tex
\section{ブログ投稿}
こんにちは、私の名前は李智维です。最新の技術に関する記事を書いています。

% English text
\section{Introduction}
Hello, my name is Zhiwei Li.

\end{document}
```

If your resume uses a template like `awesome-cv`, ensure the preamble includes `xeCJK` and the font settings above. For example, in `awesome-cv.cls` or `resume-ja.tex`, add:

```latex
\RequirePackage{xeCJK}
\ifthenelse{\equal{\fontsystem}{linux}}{
    \setCJKmainfont{Noto Sans CJK JP}
    \setCJKsansfont{Noto Sans CJK JP}
    \setCJKmonofont{Noto Sans Mono CJK JP}
    \setmainfont{Liberation Serif}
}
```

#### Step 4: Recompile the Document
Navigate to the Japanese resume directory and recompile:
```bash
cd latex/ja/resume-ja
xelatex resume-ja.tex
```

Check the log file (`resume-ja.log`) for "Missing character" errors. If the font is set correctly, these errors should disappear, and the PDF should display Japanese characters like `ー`, `専`, `証`, and `発` correctly.

#### Step 5: Debug if Errors Persist
If you still see "Missing character" errors:
1. **Confirm Font Name**: Ensure the font name matches exactly as listed in `fc-list`. For example, some systems list `Noto Sans CJK JP Regular` instead of `Noto Sans CJK JP`. Adjust the LaTeX configuration:
   ```latex
   \setCJKmainfont{Noto Sans CJK JP Regular}
   ```
2. **Check xeCJK Configuration**: Ensure `xeCJK` is loaded before font settings and that no other package overrides the CJK font. For example, avoid loading `fontspec` with conflicting settings.
3. **Test Minimal Document**: Create a minimal LaTeX file with Japanese text to isolate the issue:
   ```latex
   \documentclass{article}
   \usepackage{xeCJK}
   \setCJKmainfont{Noto Sans CJK JP}
   \begin{document}
   こんにちは、専ー証発
   \end{document}
   ```
   Compile with `xelatex` and check for errors.
4. **Fallback Font**: If `Noto Sans CJK JP` doesn’t work, try `Source Han Sans JP` or `IPAexGothic`. List available fonts with `fc-list :lang=ja` and update the configuration accordingly.

#### Step 6: Update Translated Section
Since you’re using the Python script to translate sections like `blogposts.tex`, ensure the translated file (`latex/ja/resume-ja/blogposts.tex`) is included in `resume-ja.tex` via `\input{blogposts}`. The script you provided already replaces the file correctly, so no changes are needed there. Just re-run the translation if necessary:
```bash
python translate_section.py --section blogposts.tex --lang ja --kind resume
```

Then recompile `resume-ja.tex` to incorporate the updated section.

### Additional Notes
- **Font Weights**: `Noto Sans CJK JP` supports multiple weights (Regular, Bold, etc.), so `\textbf{}` should work for Japanese text. If using `IPAexGothic`, ensure the bold variant (`IPAexGothic Bold`) is available or adjust the configuration.
- **Template Compatibility**: If you’re using a template like `awesome-cv`, check if it overrides font settings in the `.cls` file. You may need to apply the `xeCJK` settings in the main document (`resume-ja.tex`) instead.
- **PDF Output**: Inspect the generated PDF to ensure Japanese characters render correctly. If characters appear as boxes, the font is still incorrect or not embedded properly.
- **System Font Cache**: After installing new fonts, update the font cache:
  ```bash
  fc-cache -fv
  ```

### Example Output
After applying the fix, your `blogposts.tex` in `latex/ja/resume-ja/` might contain Japanese text like:
```latex
\section{ブログ投稿}
\item 技術ブログ: 最新のAI技術について書いています。専門的な内容をわかりやすく説明します。
```
When compiled with `Noto Sans CJK JP`, characters like `ー`, `専`, `証`, and `発` should render correctly in the PDF.

If you encounter further errors or need help with a specific part of the resume template, please share the relevant LaTeX code (e.g., the preamble of `resume-ja.tex` or the template’s font settings), and I can provide a more targeted fix!
