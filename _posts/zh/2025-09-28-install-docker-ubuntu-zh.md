---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: Ubuntu系统安装Docker指南
translated: true
type: note
---

根据您的 Ubuntu 系统输出，您有几种安装 Docker 的方式。以下是推荐方案：

## 方案一：安装 Docker Engine（推荐）

最常见且推荐的方式是从 Docker 官方仓库安装 Docker Engine：

```bash
# 更新软件包索引
sudo apt update

# 安装必备组件
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 再次更新软件包索引
sudo apt update

# 安装 Docker Engine
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 方案二：通过 APT 快速安装（更简单）

根据终端显示的选项，您可以直接使用：

```bash
sudo apt install docker.io
```

## 安装后设置

安装完成后，建议执行以下操作：

1. **启动并启用 Docker 服务：**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

2. **将用户添加到 docker 用户组**（以便无需 sudo 即可运行 Docker）：
```bash
sudo usermod -aG docker $USER
```

随后请注销并重新登录，或执行：
```bash
newgrp docker
```

3. **验证安装：**
```bash
docker --version
docker run hello-world
```

## 如何选择安装方案？

- **方案一** 可让您直接获取 Docker 官方提供的最新版本
- **方案二** 更简单便捷，但可能使用的是 Ubuntu 仓库中的稍旧版本

对大多数用户而言，方案二（`sudo apt install docker.io`）完全够用且操作更简单。常规使用场景下版本差异通常微乎其微。

需要我详细解释某个步骤吗？
