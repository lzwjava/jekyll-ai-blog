---
audio: false
generated: true
lang: zh
layout: post
title: 在 Ubuntu 系统下的 LaTeX 中安装 FontAwesome5 图标库
translated: true
type: note
---

在 Ubuntu 系统上安装 LaTeX 的 FontAwesome5 有以下几种方法：

## 方法一：使用 tlmgr（TeX Live 管理器）

如果已安装 TeX Live，可以使用包管理器：

```bash
sudo tlmgr update --self
sudo tlmgr install fontawesome5
```

## 方法二：使用 apt 包管理器

Ubuntu 软件源提供了 FontAwesome5：

```bash
sudo apt update
sudo apt install texlive-fonts-extra
```

这会安装包含 FontAwesome5 在内的完整字体集合。

## 方法三：手动安装

如果上述方法无效，可以手动安装：

1. 从 CTAN 下载 FontAwesome5 安装包
2. 解压到本地 texmf 目录：

```bash
mkdir -p ~/texmf/tex/latex/fontawesome5
cd ~/texmf/tex/latex/fontawesome5
# 在此处解压下载的安装包
```

3. 更新 TeX 数据库：

```bash
texhash ~/texmf
```

## 在 LaTeX 中使用 FontAwesome5

安装完成后，即可在 LaTeX 文档中使用：

```latex
\documentclass{article}
\usepackage{fontawesome5}

\begin{document}
\faHome \quad 主页图标
\faEnvelope \quad 邮件图标
\faGithub \quad GitHub 图标
\end{document}
```

## 故障排除

若遇到问题：

1. 检查 TeX Live 是否是最新版本：

```bash
tlmgr --version
```

2. 验证软件包是否安装成功：

```bash
tlmgr info fontawesome5
```

3. 确保使用 XeLaTeX 或 LuaLaTeX 以获得 FontAwesome5 的完整 Unicode 支持。

最简便的方式通常是使用方法二 `apt install texlive-fonts-extra`，它能自动处理依赖关系。
