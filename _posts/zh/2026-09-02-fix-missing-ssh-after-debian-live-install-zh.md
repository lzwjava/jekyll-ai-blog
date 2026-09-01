---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复安装Debian Live后缺失SSH的问题
translated: true
type: note
---

问题：你通过 `debian-live-13.6.0-amd64-xfce.iso` 安装了 Debian，但 `openssh-server` 不可用。

答案：是的——这就能解释原因了。**Live XFCE ISO 可以在没有配置 APT 网络镜像的情况下安装一个可用的桌面环境**，尤其是在安装过程中你跳过了镜像配置。

首先检查：

```bash
cat /etc/apt/sources.list
```

在现代 Debian 13 中，还要检查：

```bash
ls -l /etc/apt/sources.list.d/
cat /etc/apt/sources.list.d/* 2>/dev/null
```

### 最简单的修复方法

如果你的机器可以访问互联网，请创建一个 Debian 13 仓库配置：

```bash
sudo tee /etc/apt/sources.list.d/debian.sources >/dev/null <<'EOF'
Types: deb
URIs: https://deb.debian.org/debian
Suites: trixie trixie-updates
Components: main

Types: deb
URIs: https://security.debian.org/debian-security
Suites: trixie-security
Components: main
EOF
```

然后执行：

```bash
sudo apt update
sudo apt install openssh-server
```

启动 SSH：

```bash
sudo systemctl enable --now ssh
```

验证：

```bash
systemctl status ssh
```

接着，在局域网内的另一台电脑上：

```bash
ssh your_user@DEBIAN_LAN_IP
```

查找 IP 地址：

```bash
hostname -I
```

例如：

```bash
ssh zhiwei@192.168.1.123
```

**重要提示：** Debian 13 默认使用较新的 `.sources` 仓库格式，因此如果 `/etc/apt/sources.list` 为空也不必担心。实际配置可能位于 `/etc/apt/sources.list.d/` 目录下。

如果你粘贴以下命令的输出：

```bash
cat /etc/apt/sources.list
ls -l /etc/apt/sources.list.d/
```

我就能准确告诉你当前安装的具体情况。