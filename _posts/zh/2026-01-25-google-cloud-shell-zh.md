---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Shell 简介
translated: true
type: note
---

**Question:** Google Cloud 中的 Cloud Shell 全面指南

**Answer:**

Cloud Shell 是 Google Cloud 提供的一种免费的、基于浏览器的 Shell 环境，让你无需在本地安装任何软件，即可直接从浏览器管理 Google Cloud 资源。

### 什么是 Google Cloud Shell？

Cloud Shell 提供了一个临时的 **基于 Debian 的 Linux VM**（Compute Engine 实例），预装了以下内容：

- Google Cloud SDK (`gcloud`, `gsutil`, `bq` 等) —— 始终保持最新版本
- 常用工具：`docker`, `terraform`, `kubectl`, `helm`, `git`, `node`, `python`, `go`, `java` 等
- 已处理好身份验证（使用你的 Google 账号）
- 5 GB 的持久化 **家目录 (home directory)** 存储 (`/home/<your_username>`)
- 基于 Web 的代码编辑器 (Cloud Shell Editor —— 类似 VS Code 的界面)
- Gemini CLI (终端中的 AI 辅助)

它是进行快速实验、学习 GCP、运行 gcloud 命令、管理 Infrastructure as Code 或进行轻量级开发的理想选择。

### 如何启动 Cloud Shell

1. 访问 Google Cloud Console → https://console.cloud.google.com
2. 点击右上角工具栏中的 **Cloud Shell 图标**（终端符号）
   → 或使用直接链接：https://shell.cloud.google.com
3. 第一次使用时 → 系统会置备机器（大约需要 10–30 秒）
4. 你会在屏幕底部获得一个 Bash 终端（可以弹出到新标签页中）

其他启动方式：

- 许多 GCP 文档页面中的 `cloudshell` 按钮（"Open in Cloud Shell"）
- 带有项目克隆的直接深层链接：`https://shell.cloud.google.com/?show=terminal&cloudshell_git_repo=<url>`

### 持久化存储 (5 GB Home Directory)

只有 `/home/$USER` 在不同会话之间是持久化的。

其他所有位置（`/tmp`, `/usr/local` 等）都是 **临时 (ephemeral)** 的 —— 会话结束时会被删除。

常见的持久化位置：

- `~/` (home)
- `~/.bashrc`, `~/.zshrc`, `~/.gitconfig`
- `~/projects/`, `~/bin/` 等

提示：如果需要，请将较大的文件存储在 **Cloud Storage** bucket 中并挂载它们。

### 会话寿命与机器配置

- 空闲超时：约 **60 分钟**（可通过设置进行一定程度的配置）
- 最长会话时长：**12 小时**（之后会重启）
- 机器类型：通常为 **e2-micro** 或类似规格（1 vCPU, 约 3.75 GB RAM —— 可能会有变动）
- 临时磁盘：约 100 GB（非持久化）

### 配额与限制（截至 2025 年末 / 2026 年初）

- 持久化存储：每个用户 **5 GB**（硬性限制）
- 每周 Cloud Code / Editor 使用时长：**50 小时**（延长使用编辑器的软配额）
- 无法选择自定义机器类型
- 没有用于安装系统包的 sudo 权限（`apt install` 适用于用户空间工具）

### 包含的核心功能与工具

- 全功能的 **gcloud** CLI（自动完成身份验证）
- **Cloud Shell Editor** —— 点击铅笔图标或输入 `cloudshell edit <file>`
- Git 克隆、推送（GitHub, Cloud Source Repositories）
- Docker（构建并运行容器 —— 但没有特权模式）
- Terraform, Pulumi, Ansible 等
- Web 预览：点击端口号 → "Preview on port xxxx"
- 通过 UI 上传/下载文件（齿轮图标）
- 多标签页（在弹出窗口中）
- 自定义提示符、安装 oh-my-zsh 等

### 最佳实践

1. **始终将重要数据存储在持久化的 home 目录或 GCS 中**

   ```bash
   gsutil cp -r important-project gs://my-backup-bucket/
   ```

2. **明智地使用 .bashrc / .zshrc**

   添加 aliases, functions 以及 PATH 修改。

3. **在 ~/bin 中安装用户工具或使用语言包管理器**

   ```bash
   pip install --user awscli
   npm install -g serverless
   go install github.com/...
   ```

4. **对大文件 / 共享数据使用 Cloud Storage**

   ```bash
   gcsfuse my-bucket ~/mnt/bucket
   ```

5. **利用文档/教程中的 "Open in Cloud Shell" 按钮**

6. **对长时间运行的进程使用 tmux / screen**

   （如果你重新连接，即使关闭浏览器会话也会存续）

7. **备份点文件 (dotfiles)**

   将 `~/.*` 配置推送到私有 Git 仓库。

8. **进行重度开发 → 考虑使用 Cloud Workstations 或本地环境**

   Cloud Shell 非常适合快速任务，但不适合全职重度开发。

### 入门常用命令

```bash
# 显示当前项目
gcloud config get-value project

# 列出项目
gcloud projects list

# 设置默认项目
gcloud config set project my-project-id

# 列出 bucket
gsutil ls

# 克隆仓库并打开编辑器
git clone https://github.com/user/repo
cloudshell edit repo/main.py

# 预览 Web 应用
python3 -m http.server 8080   # → 点击 "Preview on port 8080"
```

### 何时不应使用 Cloud Shell

- 重度计算（ML 训练、视频转码）
- 需要 >5 GB 的持久化存储
- 需要 sudo / 内核模块
- 长时间运行的后台进程 (>12h)
- 处理超大文件

对于这些情况 → 请使用 **Compute Engine**, **Cloud Run**, **Cloud Workstations** 或本地机器 + Cloud SDK。

Cloud Shell 仍然是从任何带有浏览器的设备安全地与 Google Cloud 交互的最快方式之一。

**参考资料：**

- [Cloud Shell 文档](https://docs.cloud.google.com/shell/docs)
- [使用 Cloud Shell](https://docs.cloud.google.com/shell/docs/using-cloud-shell)
- [Cloud Shell 工作原理](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works)
- [启动 Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell)
- [Cloud Shell Editor 限制](https://docs.cloud.google.com/code/docs/shell/limitations)