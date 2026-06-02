---
audio: false
generated: true
lang: en
layout: post
title: Install XeLaTeX
translated: false
type: note
---

To install XeLaTeX on Ubuntu 24.04 or 22.04, follow these steps:

1. **Update the package list**:
   ```bash
   sudo apt update
   ```

2. **Install TeX Live (which includes XeLaTeX)**:
   - For a full installation (recommended for most users, includes XeLaTeX and many packages):
     ```bash
     sudo apt install texlive-xetex
     ```
   - If you want a minimal installation, you can install `texlive` instead, but `texlive-xetex` is preferred for XeLaTeX support.

3. **Verify installation**:
   Run the following command to check if XeLaTeX is installed:
   ```bash
   xelatex --version
   ```
   You should see output like `XeTeX 3.14159265-2.6-0.999991` (version numbers may vary).

4. **Optional: Install additional fonts** (if you need specific fonts for XeLaTeX):
   ```bash
   sudo apt install texlive-fonts-extra
   ```

5. **Test XeLaTeX**:
   Create a simple `.tex` file, e.g., `test.tex`:
   ```latex
   \documentclass{article}
   \usepackage{fontspec}
   \setmainfont{Liberation Serif}
   \begin{document}
   Hello, XeLaTeX!
   \end{document}
   ```
   Compile it with:
   ```bash
   xelatex test.tex
   ```
   This should generate a `test.pdf` file.

**Notes**:
- The `texlive-xetex` package is available in Ubuntu 22.04 and 24.04 repositories.
- If you need the latest TeX Live version, you can install it manually from the TeX Live website, but the Ubuntu package is usually sufficient.
- Ensure you have enough disk space (~1-2 GB for `texlive-xetex`, more for `texlive-full`).
- If you encounter issues, check for missing dependencies with `sudo apt install -f`.

Let me know if you need further assistance!
