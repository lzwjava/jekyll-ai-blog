---
audio: false
generated: true
lang: zh
layout: post
title: 获取 Ubuntu 中文件的完整路径
translated: true
type: note
---

在 Ubuntu 系统中，你可以使用 `realpath` 或 `readlink -f` 命令获取文件的完整路径。以 `geckodriver` 为例，可以运行：

```bash
realpath ./geckodriver
```

或

```bash
readlink -f ./geckodriver
```

这两个命令都会输出完整路径，例如：

```
/home/lzw/bin/geckodriver
```

`realpath` 命令功能直观且广泛用于此场景。若系统中未安装该命令，可通过以下指令安装：

```bash
sudo apt install realpath
```

另外，`readlink -f` 通常作为 coreutils 的核心组件默认预装在系统中。
