---
audio: false
generated: true
lang: en
layout: post
title: Install FontAwesome5 in LaTeX on Ubuntu
translated: false
type: note
---

To install FontAwesome5 for LaTeX on Ubuntu, you have several options:

## Method 1: Using tlmgr (TeX Live Manager)

If you have TeX Live installed, you can use the package manager:

```bash
sudo tlmgr update --self
sudo tlmgr install fontawesome5
```

## Method 2: Using apt package manager

Ubuntu provides FontAwesome5 through its repositories:

```bash
sudo apt update
sudo apt install texlive-fonts-extra
```

This installs a comprehensive collection of fonts including FontAwesome5.

## Method 3: Manual installation

If the above methods don't work, you can install manually:

1. Download the FontAwesome5 package from CTAN
2. Extract it to your local texmf directory:

```bash
mkdir -p ~/texmf/tex/latex/fontawesome5
cd ~/texmf/tex/latex/fontawesome5
# Extract the downloaded package here
```

3. Update the TeX database:

```bash
texhash ~/texmf
```

## Using FontAwesome5 in LaTeX

Once installed, you can use it in your LaTeX documents:

```latex
\documentclass{article}
\usepackage{fontawesome5}

\begin{document}
\faHome \quad Home icon
\faEnvelope \quad Email icon
\faGithub \quad GitHub icon
\end{document}
```

## Troubleshooting

If you encounter issues:

1. Check if your TeX Live installation is up to date:

```bash
tlmgr --version
```

2. Verify the package is installed:

```bash
tlmgr info fontawesome5
```

3. Make sure you're using XeLaTeX or LuaLaTeX for full Unicode support with FontAwesome5.

The easiest approach is usually Method 2 using `apt install texlive-fonts-extra` as it handles dependencies automatically.
