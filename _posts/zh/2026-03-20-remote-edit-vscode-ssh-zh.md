---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 VS Code SSH 远程编辑文件
translated: true
type: note
---

Question: 如何使用 VS Code 远程编辑服务器上的文件？

Answer: 

使用 **Visual Studio Code** 远程编辑服务器上文件的最佳且最受欢迎的方式是官方的 **Remote - SSH** 扩展。它为远程机器提供完整的 VS Code 体验（IntelliSense、调试、终端、扩展等）。

### 逐步指南（2025–2026 方法）

1. **前提条件**
   - 本地计算机上已安装 VS Code
   - 远程机器上运行 SSH 服务器（几乎所有 Linux 服务器都有）
   - 您已经可以通过终端使用 `ssh user@server-ip` 连接（首先测试非常重要！）

2. **安装 Remote - SSH 扩展**
   - 打开 VS Code
   - 转到扩展视图（`Ctrl+Shift+X` 或 Mac 上 `Cmd+Shift+X`）
   - 搜索 **Remote - SSH**
   - 安装由 **Microsoft** 发布的版本（ms-vscode-remote.remote-ssh）

3. **（推荐）设置 SSH 密钥认证**
   密码登录可行，但密钥更方便且更安全。

   在您的**本地**机器上：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location & no passphrase (or set one)
   ```

   将公钥复制到服务器（最简单的方式）：
   ```bash
   ssh-copy-id user@your-server-ip
   ```

   或手动：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # copy output → paste into server's ~/.ssh/authorized_keys
   ```

4. **在 VS Code 中配置 SSH 连接**
   两种主要方式：

   **方式 A – 快速（推荐大多数人使用）**

   - 按 `Ctrl+Shift+P` → 输入 **Remote-SSH: Connect to Host...**
   - 选择 **Add New SSH Host...**
   - 输入：`ssh user@server-ip -p 22`（如果端口为 22，则只需 `user@server-ip`）
   - 选择配置文件位置（通常 Linux/Mac 上为 `~/.ssh/config`，Windows 上为 `%USERPROFILE%\.ssh\config`）
   - VS Code 会添加类似这样的条目：

     ```text
     Host my-server
         HostName 192.168.1.150     # or domain.com
         User yourusername
         Port 22
         # Optional: IdentityFile ~/.ssh/id_ed25519
     ```

   **方式 B – 手动编辑**（更多控制）

   打开/创建文件 `~/.ssh/config` 并添加：

   ```text
   Host myserver
       HostName 123.45.67.89
       User devuser
       Port 2222                # only if not default 22
       IdentityFile ~/.ssh/id_ed25519
   ```

5. **连接**
   - `Ctrl+Shift+P` → **Remote-SSH: Connect to Host...**
   - 选择您的主机（例如 `myserver` 或 `user@ip`）
   - 首次连接：VS Code 会在远程机器上安装其服务器组件（~/.vscode-server）
   - 等待 30–90 秒（仅首次）

6. **打开文件夹并开始编辑**
   - 连接后 → 左下角看到绿色栏（"SSH: myserver"）
   - `File → Open Folder...` → 浏览远程文件系统 → 选择项目文件夹
   - 或从 Remote Explorer 侧边栏拖入文件夹
   - 现在正常编辑文件 — 保存 = 直接保存到服务器

7. **连接后有用的功能**
   - 集成终端（`Ctrl+``）→ 在服务器上运行
   - 远程安装扩展（查找 "Install in SSH" 按钮）
   - 调试、Git、tasks.json 等均在远程工作
   - 多个主机 → 使用 Remote Explorer 侧边栏

### 快速故障排除提示

- 连接失败？→ 先在终端测试 `ssh user@server`
- 非常慢？→ 检查网络，或添加到 `settings.json`：
  ```json
  "remote.SSH.useLocalServer": true,
  "remote.SSH.connectTimeout": 60
  ```
- 权限被拒？→ 修复 SSH 密钥或密码
- VS Code 服务器安装失败？→ 服务器需要 ~150–300 MB 磁盘空间 + 互联网（仅下载一次）

### 替代方案（如果无法在服务器上安装任何内容）

使用 **SSH FS** 扩展 — 它通过 SFTP/SSHFS 挂载远程文件夹。功能较弱（无完整的远程扩展/调试），但服务器上零安装。

参考资料：  

- [Official VS Code Remote - SSH documentation](https://code.visualstudio.com/docs/remote/ssh)
- [Remote SSH tutorial](https://code.visualstudio.com/docs/remote/ssh-tutorial)