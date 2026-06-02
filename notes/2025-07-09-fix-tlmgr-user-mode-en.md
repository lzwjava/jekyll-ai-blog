---
audio: false
generated: true
lang: en
layout: post
title: Fixing TeX Live tlmgr User Mode
translated: false
type: note
---

The error indicates that `tlmgr` user mode is not initialized on your Debian/Ubuntu system. This is a common issue with TeX Live installations from Ubuntu repositories. Here's how to fix it:

## Solution 1: Initialize tlmgr user mode

First, initialize the user mode:

```bash
tlmgr init-usertree
```

If that doesn't work, try:

```bash
tlmgr --usermode init-usertree
```

## Solution 2: Use apt instead (Recommended for Ubuntu)

Since you're on Ubuntu/Debian, it's often easier to use the system package manager:

```bash
sudo apt update
sudo apt install texlive-fonts-extra
```

This will install FontAwesome5 along with other font packages.

## Solution 3: Check if FontAwesome5 is already installed

You might already have it installed. Test by creating a simple LaTeX file:

```latex
\documentclass{article}
\usepackage{fontawesome5}

\begin{document}
\faHome
\end{document}
```

Compile it with:
```bash
pdflatex test.tex
```

## Solution 4: If you need the latest version

If you specifically need the latest FontAwesome5 version, you can:

1. Download the package manually from CTAN
2. Install it in your local texmf directory:

```bash
mkdir -p ~/texmf/tex/latex/fontawesome5
# Extract the downloaded package to this directory
texhash ~/texmf
```

## Quick check

To see what TeX packages you currently have installed:

```bash
dpkg -l | grep texlive
```

For most users, `sudo apt install texlive-fonts-extra` is the simplest solution that avoids the tlmgr user mode issues entirely.
