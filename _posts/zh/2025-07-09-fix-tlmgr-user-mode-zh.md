---
audio: false
generated: true
lang: zh
layout: post
title: 修复TeX Live tlmgr用户模式
translated: true
type: note
---

错误信息表明您的 Debian/Ubuntu 系统上未初始化 `tlmgr` 用户模式。这是从 Ubuntu 仓库安装 TeX Live 时的常见问题。以下是解决方法：

## 解决方案 1：初始化 tlmgr 用户模式

首先初始化用户模式：

```bash
tlmgr init-usertree
```

如果上述命令无效，请尝试：

```bash
tlmgr --usermode init-usertree
```

## 解决方案 2：使用 apt 安装（Ubuntu 系统推荐）

由于您使用的是 Ubuntu/Debian 系统，使用系统包管理器通常更简便：

```bash
sudo apt update
sudo apt install texlive-fonts-extra
```

这将安装 FontAwesome5 及其他字体包。

## 解决方案 3：检查是否已安装 FontAwesome5

您可能已经安装了该字体包。可通过创建简单 LaTeX 文件进行测试：

```latex
\documentclass{article}
\usepackage{fontawesome5}

\begin{document}
\faHome
\end{document}
```

使用以下命令编译：

```bash
pdflatex test.tex
```

## 解决方案 4：如需最新版本

如果您特别需要最新版 FontAwesome5，可以：

1. 从 CTAN 手动下载安装包
2. 将其安装到本地 texmf 目录：

```bash
mkdir -p ~/texmf/tex/latex/fontawesome5
# 将下载的安装包解压到此目录
texhash ~/texmf
```

## 快速检查

查看当前已安装的 TeX 软件包：

```bash
dpkg -l | grep texlive
```

对于大多数用户而言，`sudo apt install texlive-fonts-extra` 是最简单的解决方案，能完全避免 tlmgr 用户模式的问题。
