---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux 上的 GitHub Desktop
translated: true
type: note
---

好的，完整情况如下：

---

## Linux 版 GitHub Desktop —— 你已安装的内容

### 什么是 shiftkey/desktop 分支？

GitHub Desktop（GitHub Inc. 的官方应用）仅支持 macOS 和 Windows。没有官方的 Linux 版本。**shiftkey/desktop** 是事实上的 Linux 移植版——由 Brendan Forster（GitHub 前员工）和社区维护。它紧密跟踪官方上游 desktop/desktop 代码库，并添加了针对 Linux 的补丁，用于：

- 原生文件对话框（通过 GTK）
- Linux 密钥链集成（libsecret/gnome-keyring）
- AppIndicator/托盘支持
- 面向 Debian/Ubuntu 发行版的 .deb 打包

最新版本是 **3.4.13-linux1**（2025 年 2 月）——它虽然是“RC”版，但对大多数用户来说已经非常稳定。底层与 Windows/Mac 上的 GitHub Desktop 3.4.13 是同一个版本。

### 如何使用

| 操作 | 方法 |
| --- | --- |
| **启动** | 在终端中输入 `github-desktop`，或在应用菜单中找到“GitHub Desktop” |
| **首次运行** | 使用 GitHub 账户登录（OAuth 流程会打开浏览器） |
| **克隆仓库** | 文件 > 克隆仓库，或粘贴 URL |
| **打开本地仓库** | 文件 > 添加本地仓库 |
| **推送/拉取/获取** | 顶部的工具栏按钮 |
| **创建 PR** | 分支 > 创建拉取请求（在浏览器中打开） |

### 它能做什么

- 克隆、初始化、添加、提交、推送、拉取、获取仓库
- 可视化审查差异（并排或统一视图）
- 创建和切换分支，管理 PR
- 通过图形界面解决合并冲突
- 查看带有分支图的提交历史
- 暂存/取消暂存更改
- 在一个窗口中管理多个仓库
- 支持 SSH 密钥和 GPG 签名

### 需要注意的事项

1. **非官方 GitHub 产品** —— 它是一个社区分支。运行良好，但可能比上游发布版晚几周。
2. **无自动更新** —— Linux 版本没有内置的更新程序。你需要在新版本发布时手动下载并使用 `dpkg -i` 安装新的 `.deb` 包。
3. **AppIndicator/托盘** —— 它会最小化到系统托盘；如果你的 Mint 面板默认不显示托盘图标，你可能需要一个托盘扩展（例如，`snapd-glib`、`libayatana-appindicator` 在 Mint 上应该已预装）。
4. **GUI 中无 GPG 签名** —— 基于命令行的 GPG 签名可以正常工作，但图形界面在 Linux 上不提供提交签名设置。
5. **密钥链** —— 使用 GNOME Keyring / libsecret 存储凭据。如果你没有设置密钥链，首次保存凭据时系统会要求输入密钥链密码。

### 文件位置

| 路径 | 用途 |
| --- | --- |
| `/usr/bin/github-desktop` | 主二进制文件 |
| `/usr/share/applications/github-desktop.desktop` | 应用菜单项 |
| `~/.config/GitHub Desktop/` | 应用配置和密钥链数据 |
| `/tmp/github-desktop.deb` | 下载的安装程序（如果你想保留以便重新安装，它还在那里） |

### 后续更新

当新版本发布时，使用相同的方法：

```bash
# 从以下地址找到最新的 .deb URL：
#   https://github.com/shiftkey/desktop/releases/latest
cd /tmp
curl -fsSL -O <指向最新的-amd64.deb的链接>
pkexec dpkg -i GitHubDesktop-linux-amd64-*.deb
```

无需运行 `apt install -f` —— 该 `.deb` 包已捆绑了所有 Electron 依赖项。
