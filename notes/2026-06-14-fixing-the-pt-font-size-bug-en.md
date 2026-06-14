---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing the --pt Font Size Bug
translated: false
type: note
---

## How the `--pt` font size bug was fixed in `ww pdf markdown-pdf`

### The Problem

The `--pt` flag existed in the CLI but had zero effect on actual PDF output. Body text was always 12pt regardless of what `--pt` value was passed.

### Root Causes (there were multiple, layered)

**Bug 1: LaTeX `article` class ignores non-standard classoptions**

The original code passed `--pt 48` as `-V classoption=48pt`, which becomes `\documentclass[48pt]{article}`. But LaTeX's `article` class only supports `10pt`, `11pt`, `12pt` — any other value is **silently ignored** with a warning. So `--pt 48` did nothing.

**Fix**: Use `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` instead of classoption.

**Bug 2: `-V header-includes=` collapses newlines**

When we moved to `-V header-includes=\renewcommand{...}\n\usepackage{titlesec}\n...`, pandoc's `-V` flag treated the entire value as a single string, collapsing `\n` into literal characters. Multiple LaTeX commands on one line = syntax error or ignored.

**Fix**: Write the header-includes content to a temp `.tex` file and use `--include-in-header <file>` instead. Pandoc reads the file verbatim, preserving all newlines. Temp file is cleaned up after pandoc exits.

**Bug 3: `titlesec` package needed for heading control**

Even once `\normalsize` was correctly set to 48pt, LaTeX's `\section` command uses its own hardcoded size formula (e.g., `\Large`, `\large`) that doesn't reference `\normalsize`. So headings stayed at the class default while body text grew.

**Fix**: Add `\usepackage{titlesec}` and explicit `\titleformat` commands:
```
\titleformat{\section}{\bfseries\fontsize{62}{74}\selectfont}{}{}{}
\titleformat{\subsection}{\bfseries\fontsize{55}{66}\selectfont}{}{}{}
\titleformat{\subsubsection}{\bfseries\normalsize}{}{}{}
```

**Bug 4 (the final, hardest one): `setspace` package's `\setstretch` overrides `\normalsize`**

This was the most insidious bug. The original code used `-V linestretch=1.5` to set line spacing. Pandoc's template generates:
```latex
% In preamble:
\usepackage{setspace}

% After \begin{document}:
\setstretch{1.5}
```

The `setspace` package's `\setstretch` command internally **redefines `\normalsize`** back to the class default (12pt) with the new stretch factor. So the execution order was:

1. `\documentclass[12pt]{article}` → `\normalsize` = 12pt
2. `\usepackage{setspace}` → loads package
3. Our `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` → `\normalsize` = 48pt ✓
4. `\AtBeginDocument{\normalsize}` → applies 48pt at doc start ✓
5. `\setstretch{1.5}` (after `\begin{document}`) → **REDEFINES `\normalsize` back to 12pt** ✗

Step 5 silently undid everything. We confirmed this by compiling a minimal .tex file without setspace — body text was correctly 48pt. Adding setspace back broke it.

**Fix**: Include `\usepackage{setspace}` and `\setstretch{1.5}` in our own `--include-in-header` file, BEFORE our `\renewcommand{\normalsize}`. Remove `-V linestretch=1.5` from the pandoc command. This way:

1. `\usepackage{setspace}` → loads package
2. `\setstretch{1.5}` → sets stretch, redefines `\normalsize` to 12pt+stretch
3. `\renewcommand{\normalsize}{\fontsize{48}{60}\selectfont}` → **overrides** back to 48pt
4. `\AtBeginDocument{\normalsize}` → applies 48pt at doc start
5. No more `\setstretch` after `\begin{document}` → 48pt persists ✓

### Verification

- Before fix: 9 pages (body text stuck at 12pt regardless of `--pt`)
- After fix: 75 pages at `--pt 48` (body text truly 48pt, headings 62pt, subsections 55pt)

### Files changed

`~/projects/ww/ww/pdf/pdf_base.py` — the `text_to_pdf_from_markdown()` function. Key changes:
- Removed `-V classoption={pt}pt` (didn't work)
- Removed `-V header-includes=...` (collapsed newlines)
- Removed `-V linestretch=1.5` (overrode normalsize)
- Added `--include-in-header` with temp file containing: setspace + setstretch + titlesec + renewcommand normalsize + titleformat commands
