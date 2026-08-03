---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi 代理已安装在 lzw@192.168.1.52 上
translated: true
type: note
---

Pi agent已安装在`lzw@192.168.1.52`上并正常运行（警告只是来自没有TTY的`-i`，无碍）。

**已完成的操作：**

1. **Node.js 22.23.2 + npm 10.9.8** 独立安装（无需sudo）至`~/.local/share/pi-node/current/`——与pi自身的安装器规范保持一致。由于远程机器上没有`curl`，因此使用wget下载（安装器自带的node-bootstrap使用了curl，所以我手动完成了这一步）。
2. **PATH持久化**：`~/.local/share/pi-node/current/bin`已添加到`~/.bashrc`和`~/.profile`中。
3. **pi 0.83.0已安装**，通过官方安装器（`pi.dev/install.sh`）：
   - 在没有TTY的情况下运行→自动选择安装，使用npm安装`@earendil-works/pi-coding-agent`（132个包）。
   - 二进制文件位于`~/.local/share/pi-node/current/bin/pi`——已验证`pi --version`→在新登录shell中输出`0.83.0`。

**远程环境摘要：**

- `~/bin/mihomo` + 配置，在tmux会话`mihomo`中运行（通过Hysteria2代理正常工作）
- `~/bin/tmux` 3.5a（AppImage解压版，无root权限）
- `~/.local/share/pi-node/current/bin/pi` 0.83.0

在该机器上打开一个新的SSH会话并运行`pi`即可开始使用。
