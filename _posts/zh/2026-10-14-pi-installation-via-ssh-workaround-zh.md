---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过SSH变通方法安装Pi
translated: true
type: note
---

完成。Pi 已安装在 `lzw@192.168.1.137` 上，并已验证可正常工作。

## 我做了什么

**障碍：** 官方安装脚本（`curl -fsSL https://pi.dev/install.sh | sh`）要求 Node.js ≥ 22.19 + npm 以及真实终端——在通过 SSH 且没有 TTY 的情况下，它会拒绝安装 Node（“No terminal detected”），而 Debian 13 的 apt 只提供 Node 20.19（过旧），同时 `sudo` 需要密码。因此我以确定性的方式复刻了它的非 sudo 路径：

1. **独立版 Node.js v22.23.3** — 从 `nodejs.org/dist/latest-v22.x` 下载，经 sha256 校验，解压到 `~/.local/share/pi-node/`，并创建了 `current` 符号链接（与官方安装器使用的方法/位置相同；无需 sudo）。
2. **在 PATH 中加入 Node 后运行官方 Pi 安装器** — 它在完全非交互模式下完成：对 **Pi 1.2.0** 进行托管安装，包含 119 个固定版本的依赖，通过冒烟测试验证并已激活。
3. **PATH 设置** — 安装器将启动器放在 `~/.local/bin`（该目录已由 Debian 的 `~/.profile` 为登录 shell 添加）；我在 `~/.bashrc` 中追加了一行带保护判断的配置，使非登录交互式 shell 也能找到 `pi` 以及独立版 Node。

## 结果

```
$ ssh lzw@192.168.1.137
$ pi --version
1.2.0
```

- 二进制：`/home/lzw/.local/bin/pi`（托管安装在 `~/.pi/agent/`）
- Node：`~/.local/share/pi-node/current`（pi 启动器会在运行时将其自动添加到 PATH）
- 已验证：`bash -lc "pi --version"` → 1.2.0，`bash -ic "pi --version"` → 1.2.0
- 之后更新可运行：`pi update`
