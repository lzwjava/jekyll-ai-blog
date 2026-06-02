---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Actions部署JAR包的SSH密钥配置
translated: true
type: note
---

为 GitHub Actions 生成 SSH 密钥以部署 JAR 文件，请按照以下步骤操作：

1. **生成 SSH 密钥对**：
   - 在本地机器或安全环境中运行：
     ```bash
     ssh-keygen -t ed25519 -C "your_email@example.com" -f github-actions-deploy
     ```
   - 如果系统不支持 Ed25519，请使用：
     ```bash
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f github-actions-deploy
     ```
   - 按 Enter 键接受默认文件位置，并可选择设置密码（建议为了安全）。这将创建两个文件：
     - `github-actions-deploy`（私钥）
     - `github-actions-deploy.pub`（公钥）

2. **将公钥添加到目标服务器**：
   - 复制公钥：
     ```bash
     cat github-actions-deploy.pub
     ```
   - 登录到要部署 JAR 文件的服务器。
   - 将公钥追加到服务器的 `~/.ssh/authorized_keys`：
     ```bash
     echo "your-public-key-content" >> ~/.ssh/authorized_keys
     ```
   - 确保 `authorized_keys` 文件具有正确的权限：
     ```bash
     chmod 600 ~/.ssh/authorized_keys
     ```

3. **将私钥存储在 GitHub Secrets 中**：
   - 转到 GitHub 仓库：`Settings > Secrets and variables > Actions > Secrets`。
   - 点击 **New repository secret**。
   - 命名密钥（例如 `SSH_PRIVATE_KEY`）。
   - 粘贴私钥内容（`github-actions-deploy`）：
     ```bash
     cat github-actions-deploy
     ```
   - 保存密钥。

4. **配置 GitHub Actions 工作流**：
   - 创建或编辑工作流文件（例如 `.github/workflows/deploy.yml`）。
   - 添加一个步骤以使用 SSH 密钥部署 JAR。以下是示例工作流：

{% raw %}
     ```yaml
     name: Deploy JAR

     on:
       push:
         branches:
           - main

     jobs:
       deploy:
         runs-on: ubuntu-latest

         steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Set up Java
           uses: actions/setup-java@v4
           with:
             java-version: '17' # 根据你的 Java 版本调整
             distribution: 'temurin'

         - name: Build JAR
           run: mvn clean package # 根据你的构建工具调整（例如 Gradle）

         - name: Install SSH Key
           uses: shimataro/ssh-key-action@v2
           with:
             key: ${{ secrets.SSH_PRIVATE_KEY }}
             known_hosts: 'optional-known-hosts' # 参见下面的说明

         - name: Add Known Hosts
           run: |
             ssh-keyscan -H <server-ip-or-hostname> >> ~/.ssh/known_hosts
           # 将 <server-ip-or-hostname> 替换为你的服务器 IP 或主机名

         - name: Deploy JAR to Server
           run: |
             scp target/your-app.jar user@<server-ip-or-hostname>:/path/to/deploy/
             ssh user@<server-ip-or-hostname> "sudo systemctl restart your-service" # 根据你的部署流程调整
     ```
{% endraw %}

   - **注意事项**：
     - 将 `target/your-app.jar` 替换为你的 JAR 文件路径。
     - 将 `user@<server-ip-or-hostname>` 替换为你的服务器 SSH 用户和地址。
     - 调整部署命令（例如 `sudo systemctl restart your-service`）以匹配你在服务器上启动或部署 JAR 的方式。
     - `known_hosts` 步骤对于避免 SSH 主机验证问题至关重要。如果你知道服务器的主机密钥，可以在 `shimataro/ssh-key-action` 步骤中预先填充，或使用 `ssh-keyscan` 如上所示。

5. **保护工作流**：
   - 确保私钥永远不会在日志或输出中暴露。
   - 限制仓库权限以防止未经授权访问密钥。
   - 如果为 SSH 密钥使用密码，请将其添加为另一个密钥并在 `shimataro/ssh-key-action` 步骤中包含：
{% raw %}
     ```yaml
     with:
       key: ${{ secrets.SSH_PRIVATE_KEY }}
       passphrase: ${{ secrets.SSH_KEY_PASSPHRASE }}
       known_hosts: 'optional-known-hosts'
     ```
{% endraw %}

6. **测试工作流**：
   - 推送更改到 `main` 分支（或工作流中指定的分支）。
   - 在 GitHub 仓库的 **Actions** 选项卡中监控工作流，确保 JAR 构建和部署正确。

7. **故障排除**：
   - **Permission denied**：验证 SSH 密钥是否正确添加到服务器的 `authorized_keys`，并且用户有权访问目标目录。
   - **Host verification failed**：确保 `known_hosts` 步骤正确配置了服务器的 IP 或主机名。
   - **Build issues**：确认 Java 版本和构建命令与你的项目设置匹配。

此设置将基于 SSH 的部署安全地集成到你的 GitHub Actions 工作流中，用于部署 JAR 文件。如果你需要特定调整（例如针对特定服务器设置或构建工具），请告诉我！
