---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用SSH连接GitHub
translated: true
type: note
---

要使用 SSH 连接 GitHub，请根据 GitHub 官方文档遵循以下步骤。本指南假设您从零开始，包含检查现有密钥、生成新密钥、将其添加到 GitHub 以及测试连接。

### 1. 检查现有 SSH 密钥
在创建新 SSH 密钥前，先检查是否已存在密钥：
- 打开终端（macOS/Linux）或 Git Bash（Windows）。
- 运行：
  ```bash
  ls -al ~/.ssh
  ```
- 查找类似 `id_rsa` 和 `id_rsa.pub` 的文件（或其他类似文件，如 `id_ed25519`、`id_ed25519.pub`）。如果存在，说明您可能已有密钥。若想使用现有密钥，请跳至步骤 3；否则继续生成新密钥。

### 2. 生成新 SSH 密钥
如果没有 SSH 密钥或需要新密钥：
- 在终端中生成新 SSH 密钥：
  ```bash
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ```
  - 将 `your_email@example.com` 替换为与 GitHub 账户关联的邮箱。
  - 如果系统不支持 `ed25519`，请使用：
    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
- 出现提示时，按 Enter 将密钥保存到默认位置（`~/.ssh/id_ed25519` 或 `~/.ssh/id_rsa`）。
- 可选：输入密码短语以增强安全性（或直接按 Enter 留空）。

### 3. 将 SSH 密钥添加到 SSH 代理
SSH 代理管理您的身份验证密钥：
- 启动 SSH 代理：
  ```bash
  eval "$(ssh-agent -s)"
  ```
- 将私钥添加到代理：
  ```bash
  ssh-add ~/.ssh/id_ed25519
  ```
  - 如果使用 RSA，请将 `id_ed25519` 替换为 `id_rsa`。
- 如果设置了密码短语，系统会提示您输入。

### 4. 将 SSH 密钥添加到 GitHub 账户
- 将公钥复制到剪贴板：
  - macOS：
    ```bash
    pbcopy < ~/.ssh/id_ed25519.pub
    ```
  - Linux：
    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```
    然后手动复制输出内容。
  - Windows（Git Bash）：
    ```bash
    cat ~/.ssh/id_ed25519.pub | clip
    ```
  - 如果使用 RSA，请将 `id_ed25519.pub` 替换为 `id_rsa.pub`。
- 访问 GitHub：
  - 登录 [GitHub](https://github.com)。
  - 点击右上角头像 → **Settings** → **SSH and GPG keys** → **New SSH key** 或 **Add SSH key**。
  - 在 "Key" 字段中粘贴公钥，为其添加标题（例如 "我的笔记本电脑"），然后点击 **Add SSH key**。

### 5. 测试 SSH 连接
验证 SSH 密钥是否与 GitHub 正常工作：
- 运行：
  ```bash
  ssh -T git@github.com
  ```
- 如果出现提示，请输入 `yes` 确认。
- 您应看到类似消息：
  ```
  Hi username! You've successfully authenticated, but GitHub does not provide shell access.
  ```
  这表明 SSH 连接已成功建立。

### 6. 配置 Git 使用 SSH
确保 Git 仓库使用 SSH 进行身份验证：
- 检查仓库的远程 URL：
  ```bash
  git remote -v
  ```
- 如果 URL 以 `https://` 开头，请更改为 SSH：
  ```bash
  git remote set-url origin git@github.com:username/repository.git
  ```
  - 将 `username/repository` 替换为您的 GitHub 用户名和仓库名称。

### 7. 可选：管理 SSH 密钥密码短语
如果设置了密码短语，可配置 SSH 代理避免重复输入：
- 在 macOS 上，将密钥添加到钥匙串：
  ```bash
  ssh-add --apple-use-keychain ~/.ssh/id_ed25519
  ```
- 在 Linux/Windows 上，SSH 代理通常每个会话仅提示输入一次密码短语。

### 8. 可选：使用 SSH 代理转发或部署密钥
- **SSH 代理转发**：如需部署到服务器，可启用代理转发以安全使用本地 SSH 密钥。在 `~/.ssh/config` 中添加：
  ```bash
  Host example.com
      ForwardAgent yes
  ```
  将 `example.com` 替换为服务器的主机名。
- **部署密钥**：对于自动化脚本，可为每个服务器生成独立的 SSH 密钥，并将其作为部署密钥添加到 GitHub 仓库设置中。

### 故障排除
- 如果 `ssh -T git@github.com` 失败，请确保：
  - 公钥已正确添加到 GitHub。
  - SSH 代理正在运行且密钥已添加（运行 `ssh-add -l` 查看已加载密钥）。
  - 文件权限正确：
    ```bash
    chmod 600 ~/.ssh/id_ed25519
    chmod 644 ~/.ssh/id_ed25519.pub
    ```
- 若问题仍存，请查阅 GitHub 故障排除指南。

现在您可以使用 SSH 安全地与 GitHub 交互，无需重复输入凭据。

[Connecting to GitHub with SSH - GitHub 文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
