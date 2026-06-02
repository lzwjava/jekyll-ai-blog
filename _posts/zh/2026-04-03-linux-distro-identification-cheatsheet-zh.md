---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux 发行版快速识别指南
translated: true
type: note
---

很简单——我通过 SSH 执行了一条命令：

```
cat /etc/os-release
```

每个 Linux 发行版都有这个文件。它会以标准格式提供操作系统名称、版本和代号等信息。我还运行了 `uname -a` 来查看内核版本，但对于识别发行版而言，`os-release` 是主要依据。

其他检查方式的速查表：
- **`cat /etc/os-release`** —— 发行版信息（几乎适用于所有系统）
- **`lsb_release -a`** —— 另一种方式，但需要安装 `lsb-release` 包
- **`uname -a`** —— 内核版本和系统架构
- **`hostnamectl`** —— 整合主机名、操作系统及内核信息（需要 systemd）
