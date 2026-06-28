---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux Mint 22.3 需要更新
translated: true
type: note
---

**问题：** Linux Mint 22.1 是最新版本吗？

**回答：**

不是。让我核实一下当前版本。不是——你的脚本指向的是 22.1，它落后了两个小版本。

最新的稳定版本是 **Linux Mint 22.3 "Zena"**，于 2026 年 1 月 13 日正式发布。Linux Mint 的所有三个版本——Cinnamon、MATE 和 Xfce——均已更新，22.3 是一个长期支持版本，将支持到 2029 年。它仍然基于 Ubuntu 24.04 (Noble)，搭载 Cinnamon 6.6 并改进了 Wayland 支持。

Mint 23 "Alfa" 要到 ~2026 年 12 月才会发布（团队切换到了更长的周期），因此现在你应该使用 22.3。

修正后的命令——将 URL 替换为 22.3 Cinnamon ISO：

```bash
curl -L -o /tmp/linuxmint.iso \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.3/linuxmint-22.3-cinnamon-64bit.iso"
```

烧录流程中的其他步骤保持不变。在运行 `dd` 之前有一件事值得做——将 ISO 与公布的 SHA256 进行校验，以免烧录损坏的镜像：

```bash
curl -L -o /tmp/sha256sum.txt \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.3/sha256sum.txt"
cd /tmp && shasum -a 256 linuxmint.iso && grep cinnamon sha256sum.txt
```

需要我现在在你的 Air 上开始下载 22.3 吗？
