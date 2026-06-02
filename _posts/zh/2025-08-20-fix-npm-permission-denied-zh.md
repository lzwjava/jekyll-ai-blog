---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 npm 权限拒绝错误
translated: true
type: note
---

您遇到的 `EACCES: permission denied` 错误意味着当前用户**没有写入** `/usr/local/lib/node_modules` 目录的权限。这是在 Linux 或 macOS 系统上安装全局 npm 包时的常见问题。

### **如何解决此问题**

#### **方案一：使用 `sudo`（不推荐常规使用）**
您可以使用 `sudo` 以 root 用户身份运行命令，但**不推荐**常规使用，因为这可能导致后续出现 npm 包权限问题。

```bash
sudo npm install -g @anthropic-ai/claude-code
```

#### **方案二：更改 npm 的默认目录（推荐）**
最佳实践是配置 npm 使用您具有写入权限的 home 目录中的文件夹。

1. **在 home 目录创建全局 npm 目录：**
   ```bash
   mkdir ~/.npm-global
   ```
2. **配置 npm 使用此目录：**
   ```bash
   npm config set prefix '~/.npm-global'
   ```
3. **将新目录添加到 `PATH` 环境变量：**
   打开您的 shell 配置文件（如 `~/.bashrc`、`~/.zshrc` 或 `~/.profile`）并添加这行：
   ```bash
   export PATH=~/.npm-global/bin:$PATH
   ```
   然后重新加载 shell：
   ```bash
   source ~/.bashrc  # 或 ~/.zshrc, ~/.profile
   ```
4. **重新尝试安装：**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

#### **方案三：修复 `/usr/local` 目录权限（高级方案）**
如果您希望继续使用 `/usr/local` 目录，可以将其所有权更改为当前用户：
```bash
sudo chown -R $(whoami) /usr/local/lib/node_modules
```
然后重新尝试安装。

---

**推荐方案：** 使用**方案二**以避免未来出现权限问题。
