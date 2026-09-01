---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 简化Debian APT仓库设置
translated: true
type: note
---

问题：Debian APT 仓库的设置能否简化？

回答：可以。如果你只需要一个简单的 Debian 13 仓库，可以用旧式的 `sources.list` 格式：

```bash
sudo sh -c 'echo "deb https://deb.debian.org/debian trixie main" > /etc/apt/sources.list'
```

然后：

```bash
sudo apt update
sudo apt install openssh-server
```

如果你还需要安全更新和常规更新，可以用一条紧凑的命令：

```bash
sudo sh -c 'printf "%s\n" \
"deb https://deb.debian.org/debian trixie main" \
"deb https://deb.debian.org/debian trixie-updates main" \
"deb https://security.debian.org/debian-security trixie-security main" \
> /etc/apt/sources.list'
```

针对你的使用场景，**第一条命令就足够开始了**。你可以稍后添加 `trixie-updates` 和 `trixie-security`。

如果你不关心 `sources.list` 的格式，还可以更短：

```bash
echo 'deb https://deb.debian.org/debian trixie main' | sudo tee /etc/apt/sources.list
```

然后：

```bash
sudo apt update && sudo apt install openssh-server
```
