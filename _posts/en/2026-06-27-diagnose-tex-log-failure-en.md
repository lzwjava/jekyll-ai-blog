---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnose TeX Log Failure
translated: false
type: note
---

I need to see the actual TeX log to diagnose the failure. You pasted arXiv's generic error page, but the line "The TeX Log appears below" is followed by nothing — the actual log didn't come through.

Two ways forward:

**Option A — paste the log.** Copy everything after "The TeX Log appears below" on that arXiv page. The real error is in there (search for "! " or "Error" or "Fatal").

**Option B — reproduce locally.** Compile your source exactly how arXiv does and read the log yourself:

```bash
# arXiv uses a fixed pipeline. Reproduce it:
cd sec-edgar-gpt-source/

# arXiv runs latexmk with pdflatex (most common for modern submissions)
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex 2>&1 | tee build.log

# Find the real error
grep -n -E "^\!|Error|Fatal|not found|Undefined" build.log
```

If you only have the PDF and lost the `.tex` source, that's the actual problem — arXiv rejects TeX-produced PDFs and wants the source tree.

A few fast checks based on the 5 common causes arXiv listed:

```bash
# 1. Mixed figure formats — pdflatex needs pdf/png/jpg, NOT eps/ps
find . -type f \\( -name '*.eps' -o -name '*.ps' \\) -print
grep -rn '\\includegraphics' *.tex | grep -iE '\.eps|\.ps'

# 2. Absolute/local paths in includegraphics (arXiv FS is case-sensitive)
grep -rn '\\includegraphics' *.tex | grep -E '/Users/|/home/|C:\\\\'

# 3. Filename case mismatches
grep -rn '\\includegraphics' *.tex   # compare against actual `ls` output

# 4. Custom .sty/.cls files not bundled
grep -rn '\\usepackage\|\\documentclass' *.tex
ls *.sty *.cls 2>/dev/null
```

Paste me the actual log (Option A output or `build.log`) and I'll pinpoint the failing line. Without it I'm guessing — the arXiv boilerplate explicitly tells you to scroll past hyperref "Option clash" noise to find the real error, which means your true failure is buried somewhere they didn't include here.
