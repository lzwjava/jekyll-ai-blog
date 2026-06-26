---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 避免 texlive-fonts-extra
translated: true
type: note
---

`texlive-fonts-extra` 体积为 629MB，但您并不需要它。请取消（按 Ctrl+C）并运行：

```
sudo apt-get install -y texlive-latex-extra texlive-fonts-recommended texlive-xetex
```

这样只需约 200MB，而非 629MB。您的论文仅使用标准字体（Times New Roman），这些字体包含在 `texlive-fonts-recommended` 中，而非额外的字体包。

如果即便如此速度仍然过慢，可能是镜像服务器限速。您可以切换到更快的镜像源：

```
sudo sed -i 's|hk.archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null
sudo sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list.d/ubuntu.sources
sudo apt-get update -qq
sudo apt-get install -y texlive-latex-extra texlive-fonts-recommended texlive-xetex
```

从中国访问阿里云镜像通常会快很多。
