---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Ubuntu 22.04 上安装 OpenClaw 指南
translated: true
type: note
---

问题：如何在 Linux kernel 6.8.0-90-generic (Ubuntu 22.04 x86_64) 上安装 OpenClaw？

回答：

你的系统 (`6.8.0-90-generic #91~22.04.1-Ubuntu SMP`) 运行着 **Ubuntu 22.04 LTS (Jammy Jellyfish)** x86_64 版本 — OpenClaw 完全支持此系统。

---

## 先决条件

最低系统要求：
- 2 vCPU
- 2 GB RAM（重要：0.5–1 GB RAM 会崩溃；swap 无法修复此问题）
- 20 GB SSD
- Ubuntu 22.04 或 24.04
- root 或 sudo 访问权限
- 互联网访问

---

## 步骤 1 — 更新系统并安装依赖项

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git ca-certificates curl build-essential
```

---

## 步骤 2 — 安装 Node.js 22（必需）

OpenClaw 需要 Node.js 22+。通过 NodeSource 仓库安装：

```bash
# 添加 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# 安装 Node.js
sudo apt install -y nodejs

# 验证
node --version   # 应显示 v22.x.x
npm --version
```

**备选方案：使用 nvm（推荐，以避免权限问题）**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
```

---

## 步骤 3 — 配置 npm 全局路径（如果不使用 nvm）

为避免全局 npm 包的权限问题：

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 步骤 4 — 安装 OpenClaw

**选项 A — 官方安装脚本（推荐）：**

安装脚本是安装 OpenClaw 的推荐方式。它在一歩中处理 Node 检测、安装和入门引导。

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**选项 B — Git 方法（用于完整 workspace/gateway 支持）：**

Git 方法确保你获得完整的源代码树，包括所有 workspace 包：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-prompt --no-onboard
```

**选项 C — npm 全局安装：**

```bash
npm install -g openclaw@latest
```

---

## 步骤 5 — 验证安装

```bash
openclaw --version
```

如果命令未找到，请将 npm 全局 bin 添加到 PATH：

```bash
echo 'export PATH=$(npm prefix -g)/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 步骤 6 — 运行入门引导（强制性）

你必须运行一次入门引导。请仔细遵循提示。这不是可选的：

```bash
openclaw onboard
```

---

## 步骤 7 — 安装并启动 Gateway

```bash
openclaw gateway install
openclaw gateway start
```

---

## 步骤 8 — 访问仪表板

SSH 隧道是在 VPS 或远程服务器上访问仪表板的唯一正确方式：

```bash
# 从你的本地机器：
ssh -N -L 18789:127.0.0.1:18789 your_user@YOUR_SERVER_IP
```

然后在浏览器中打开：`http://localhost:18789/`

如果需要 token：

```bash
openclaw dashboard --no-open
# 复制带 token 的 URL 并在浏览器中打开
```

---

## 步骤 9 — 设置为 systemd 服务（可选但推荐）

设置 systemd 以使 OpenClaw 在崩溃或重启后自动重启：

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw

# 检查状态
sudo systemctl status openclaw

# 查看实时日志
sudo journalctl -u openclaw -f
```

---

## 常见故障排除

| 问题 | 解决方法 |
|---|---|
| `openclaw: command not found` | 在 `~/.bashrc` 中将 `$(npm prefix -g)/bin` 添加到 `$PATH` |
| 仪表板无法打开 | 使用 SSH 隧道，而不是直接 IP 访问 |
| 启动崩溃 | 检查 RAM — 最低需要 2 GB |
| Systemd 使用错误的 Node 版本 | 使用 Git 方法重新安装 |

参考资料：

- [OpenClaw Official Install Docs](https://docs.openclaw.ai/install)
- [Complete Guide from Scratch (archy.net)](https://www.archy.net/installing-openclaw-a-complete-guide-from-scratch/)
- [Step-by-Step OpenClaw Setup on Ubuntu LTS (ddevops.com)](https://blogs.ddevops.com/step-by-step-openclaw-setup-on-ubuntu-lts/)
- [OpenClaw Linux Install Guide 2026 (vpn07.com)](https://vpn07.com/en/blog/2026-openclaw-install-linux-ubuntu-debian-server-tutorial.html)
- [How to Install OpenClaw for Beginners (boostedhost.com)](https://boostedhost.com/blog/en/how-to-install-openclaw-get-started-guide/)