---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 VS Code 中编辑远程文件
translated: true
type: note
---

**Question:** 如何像 Andrej Karpathy 在视频中那样，使用 VS Code 连接到主机并编辑服务器文件？

**Answer:**

Andrej Karpathy 在访谈中（例如 Lex Fridman podcast）提到过，他喜欢在**本地使用 VS Code**（在他的 Mac 上），但通过 **Remote-SSH** 连接，直接编辑远程 Linux server/cluster 上的文件。这能提供完整的本地级 VS Code 体验（IntelliSense、debugging、extensions、terminal 等），而实际的文件则存储在远程机器上。

这是目前开发者（包括许多 AI/ML 研究人员）在远程服务器上编辑代码的标准且最常用的方式。

### 分步设置（2026 当前最佳实践）

1. **安装 VS Code**
   从官网下载并安装：https://code.visualstudio.com/ （如果尚未安装）。

2. **安装 Remote - SSH 扩展**
   - 打开 VS Code
   - 进入 Extensions 视图（Ctrl+Shift+X 或 Mac 上的 Cmd+Shift+X）
   - 搜索 **Remote - SSH**
   - 安装由 Microsoft 发布的官方扩展 (ms-vscode-remote.remote-ssh)

3. **设置 SSH 访问服务器**
   确保你已经可以通过 terminal 连接：
   ```
   ssh username@your-server-ip-or-domain
   ```
   最佳实践：使用 SSH key 认证（强烈推荐）：
   - 如果没有密钥对，生成一个：`ssh-keygen -t ed25519`
   - 将公钥拷贝到服务器：`ssh-copy-id username@your-server-ip-or-domain`
   - 或者手动将 `~/.ssh/id_ed25519.pub` 的内容添加到服务器的 `~/.ssh/authorized_keys` 中。

   可选但非常有用：在本地 `~/.ssh/config` 文件中创建一个条目：
   ```
   Host my-server
       HostName your-server-ip-or-domain
       User your-username
       Port 22                # 如果使用非标准端口请修改
       IdentityFile ~/.ssh/id_ed25519
   ```
   → 之后你只需使用 `ssh my-server` 即可，无需每次输入完整详情。

4. **从 VS Code 连接**
   两种最简单的方法：

   **方法 A – Command Palette（推荐）**
   - 按下 Ctrl+Shift+P (Mac 上为 Cmd+Shift+P) → 输入 **Remote-SSH: Connect to Host...**
   - 选择 **+ Add New SSH Host...**（首次连接）或选择现有主机
   - 输入：`username@your-server-ip-or-domain`（或如果你使用了 ssh config，直接输入 `my-server`）
   - 选择要更新的配置文件（通常选默认的 ~/.ssh/config）
   - VS Code 开始连接 → 它会自动在远程机器上安装 VS Code Server（自动执行，一次性约 30-60 秒）
   - 连接后，打开任何文件夹：**File → Open Folder...** 然后导航到服务器上的项目路径（例如 `/home/username/projects/my-repo`）

   **方法 B – 从状态栏连接**
   - 点击左下角的绿色 **><** 远程指示图标
   - 选择 **Connect to Host...**

5. **现在你正在远程编辑**
   - 你打开/编辑/保存的所有文件都物理存在于服务器上
   - Terminal (Ctrl+`) 在服务器上运行
   - Extensions（Python、GitLens、Jupyter 等）可以安装在远程侧
   - Debugging、tasks、git 操作都像在本地一样工作
   - 你可以获得完整的 IntelliSense、保存时自动格式化等功能

### 技巧与常见问题

- 首次连接可能需要 1-2 分钟（在远程安装 VS Code Server）
- 确保远程服务器可以访问互联网（需要下载一次 VS Code Server）
- 如果连接断开 → 直接重新连接即可（VS Code 通常恢复得很好）
- 对于非常大的项目，考虑通过 `.vscode/settings.json` 排除文件夹 → `"files.exclude"` 或 `"search.exclude"`
- 想要更快的体验？如果你的工作流允许，可以使用 **Remote - Tunnels** 或 **GitHub Codespaces**
- 替代方案（如果你确实不想在远程安装 VS Code Server）：使用 sshfs + SFTP 扩展，但这比 Remote-SSH 更慢且稳定性较差

这正是 Karpathy 所描述的配置——本地 VS Code 窗口 + 通过 SSH 连接远程文件夹。这对于在 GPU server、cluster、cloud VM 等环境下工作极其高效。

**References:**

- [Remote Development using SSH - Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh)
- [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
