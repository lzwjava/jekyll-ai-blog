---
audio: false
generated: true
lang: zh
layout: post
title: 安装XeLaTeX
translated: true
type: note
---

在 Ubuntu 24.04 或 22.04 系统上安装 XeLaTeX 的步骤如下：

1. **更新软件包列表**：
   ```bash
   sudo apt update
   ```

2. **安装 TeX Live（包含 XeLaTeX）**：
   - 完整安装方案（推荐大多数用户使用，包含 XeLaTeX 及众多扩展包）：
     ```bash
     sudo apt install texlive-xetex
     ```
   - 如需最小化安装可改用 `texlive` 基础包，但推荐使用 `texlive-xetex` 以获得完整 XeLaTeX 支持

3. **验证安装**：
   执行以下命令检查 XeLaTeX 是否成功安装：
   ```bash
   xelatex --version
   ```
   终端将显示类似 `XeTeX 3.14159265-2.6-0.999991` 的版本信息（具体版本号可能不同）

4. **可选：安装附加字体包**（如需为 XeLaTeX 配置特殊字体）：
   ```bash
   sudo apt install texlive-fonts-extra
   ```

5. **测试 XeLaTeX**：
   创建测试文件 `test.tex`：
   ```latex
   \documentclass{article}
   \usepackage{fontspec}
   \setmainfont{Liberation Serif}
   \begin{document}
   Hello, XeLaTeX!
   \end{document}
   ```
   使用以下命令编译：
   ```bash
   xelatex test.tex
   ```
   成功执行后将生成 `test.pdf` 文件

**注意事项**：
- `texlive-xetex` 软件包已收录在 Ubuntu 22.04 与 24.04 的官方源中
- 如需最新版 TeX Live，可访问官网手动安装，但 Ubuntu 官方源版本通常已满足需求
- 请确保磁盘空间充足（`texlive-xetex` 约需 1-2 GB，完整版需要更多空间）
- 若遇依赖问题可尝试运行 `sudo apt install -f` 进行修复

如需进一步协助，欢迎随时提出！
