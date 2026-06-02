---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu系统Node.js升级指南
translated: true
type: note
---

在 Ubuntu 系统上升级 Node.js 有多种方法。最可靠且推荐的方式是使用 **`nvm`（Node 版本管理器）** 或 **NodeSource 软件仓库**。以下是两种方法的详细步骤说明。

---

## **方法一：使用 NVM（推荐）**

NVM 允许您轻松安装和管理多个 Node.js 版本。

### 1. 安装 NVM

打开终端并运行：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

然后重新加载 shell：

```bash
source ~/.bashrc
```

或

```bash
source ~/.zshrc
```

（根据您使用的 shell 选择）

### 2. 安装最新 Node.js 版本

查看可用版本：

```bash
nvm ls-remote
```

安装最新的 LTS 版本（推荐大多数用户使用）：

```bash
nvm install --lts
```

或安装特定版本（例如 20.x）：

```bash
nvm install 20
```

### 3. 设置默认版本

```bash
nvm alias default 20
```

### 4. 验证安装

```bash
node -v
npm -v
```

---

## **方法二：使用 NodeSource 软件仓库**

此方法将全局安装 Node.js。

### 1. 移除旧版 Node.js（如果通过 apt 安装）

```bash
sudo apt remove --purge nodejs npm
sudo apt autoremove
```

### 2. 添加 NodeSource 软件仓库

对于 **Node.js 20.x**（截至 2025 年 8 月的 LTS 版本）：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
```

对于 **Node.js 22.x**（如果可用）：

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

### 3. 安装 Node.js

```bash
sudo apt install -y nodejs
```

### 4. 验证安装

```bash
node -v
npm -v
```

---

## **方法三：使用 Ubuntu 默认仓库（不推荐）**

Ubuntu 默认仓库中的 Node.js 版本通常较为陈旧。若仍需使用：

```bash
sudo apt update
sudo apt install nodejs npm
```

但**不推荐**用于开发环境，因为版本通常较旧。

---

## **如何选择安装方法？**

- **使用 NVM**：若需轻松切换 Node.js 版本或需要最新功能
- **使用 NodeSource**：若需要系统级全局安装的稳定版本
