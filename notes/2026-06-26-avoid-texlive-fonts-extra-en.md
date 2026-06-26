---
audio: false
generated: true
image: false
lang: en
layout: post
title: Avoid texlive-fonts-extra
translated: false
type: note
---

`texlive-fonts-extra` is 629MB and you don't need it. Cancel (Ctrl+C) and run:

```
sudo apt-get install -y texlive-latex-extra texlive-fonts-recommended texlive-xetex
```

That's ~200MB instead of 629MB. Your paper only uses standard fonts (Times New Roman) which are in `texlive-fonts-recommended`, not the extras.

If even that's too slow, the mirror might be throttling. You can switch to a faster mirror:

```
sudo sed -i 's|hk.archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null
sudo sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list.d/ubuntu.sources
sudo apt-get update -qq
sudo apt-get install -y texlive-latex-extra texlive-fonts-recommended texlive-xetex
```

The Aliyun mirror should be much faster from China.
