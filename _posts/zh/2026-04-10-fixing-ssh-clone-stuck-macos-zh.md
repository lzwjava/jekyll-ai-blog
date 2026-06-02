---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复在macOS中SSH克隆卡住的问题
translated: true
type: note
---

问题：为什么 Hermes Agent 安装程序在 macOS 上卡在 "Trying SSH clone..."？

回答：

Hermes Agent 安装程序卡在 "Trying SSH clone..." 步骤是因为脚本尝试使用 Git 通过 SSH 克隆 Hermes 仓库，但 SSH 克隆失败（可能是由于认证问题、SSH 密钥缺失或 GitHub SSH 访问问题），且安装程序未能妥善处理该失败。它似乎在等待 SSH 提示、SSH 密码短语或一个未正常触发的超时机制。

### macOS 上常见原因

- **未为 GitHub 设置 SSH 密钥**：Git 尝试使用 SSH (<git@github.com>:...)，但您尚未将 SSH 密钥添加到 GitHub 账户或 ssh-agent。
- **SSH 代理未运行或密钥未加载**：即使您有密钥，它们也可能未被加载。
- **防火墙 / 网络 / VPN 问题**：到 GitHub 的 SSH 连接被阻止或延迟。
- **Git 配置优先使用 SSH**：安装程序或您的全局 Git 配置强制使用 SSH 而非 HTTPS。
- **脚本存在缺陷**：它先尝试 SSH 然后回退到 HTTPS，但 SSH 尝试无限期挂起（常见于因终端问题导致等待不显示的用户输入时）。

### 如何解决

1. **最快修复方法 - 强制使用 HTTPS 克隆**（推荐）：
   - 取消当前安装（按几次 Ctrl+C）。
   - 删除部分安装文件夹：

     ```
     rm -rf /Users/lzwjava/.hermes/hermes-agent
     ```

   - 然后手动使用 HTTPS 克隆：

     ```
     git clone https://github.com/NousResearch/Hermes-Agent.git /Users/lzwjava/.hermes/hermes-agent
     ```

   - 克隆完成后，重新运行安装程序或继续任何剩余的设置步骤。

2. **正确设置 SSH**（如果您偏爱 SSH）：
   - 如没有 SSH 密钥则生成一个：

     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```

   - 将密钥添加到 ssh-agent：

     ```
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_ed25519
     ```

   - 复制公钥并添加到您的 GitHub 账户（Settings → SSH and GPG keys）。
   - 测试 SSH：

     ```
     ssh -T git@github.com
     ```

   - 然后重试安装程序。

3. **其他故障排除步骤**：
   - 确保 Git 已配置您的凭据：

     ```
     git config --global user.name "Your Name"
     git config --global user.email "your_email@example.com"
     ```

   - 更新 Git：

     ```
     brew upgrade git
     ```

   - 尽可能以更详细输出运行安装程序（检查是否有 `--verbose` 参数或查看安装脚本）。
   - 临时禁用 SSH 并强制使用 HTTPS：

     ```
     git config --global url."https://github.com/".insteadOf git@github.com:
     ```

修复克隆后，安装程序应能继续通过该步骤。

如果仍卡住，请提供完整的安装程序输出或安装脚本内容以获得更具体的帮助。

参考：

- 无（基于 macOS 上常见的 Git/SSH 问题）
