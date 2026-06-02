---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 AI 代理中设置 CDP
translated: true
type: note
---

问题：如何在 Claude Code 或 OpenClaw (AI agent) 中设置 Chrome DevTools Protocol (CDP)？

回答：

## 概述

**Claude Code** 和 **OpenClaw** 都支持 Chrome DevTools Protocol (CDP) 集成，让你的 AI agent 直接控制浏览器——导航页面、点击元素、捕获截图、监控网络请求等。这是两者的完整指南。

---

## 第一部分：在 Claude Code 中设置 CDP

### 方法 A — 官方 Chrome DevTools MCP 服务器（推荐）

`chrome-devtools-mcp` 包让你的 AI 编码代理（Claude、Cursor、Copilot 等）控制并检查实时的 Chrome 浏览器。它充当 Model Context Protocol (MCP) 服务器，为你的 AI 助手提供对 Chrome DevTools 的访问，用于自动化、调试和性能分析。

**步骤 1：将 MCP 服务器添加到 Claude Code**

在终端中运行此命令：

```bash
claude mcp add -- chrome npx -y chrome-devtools-mcp@latest
```

或者，如果你想通过 marketplace 插件系统添加：

```
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
```

然后重启 Claude Code。

**步骤 2：通过 `claude_desktop_config.json` 配置**

将 MCP 服务器添加到你的 Claude Code 配置文件 `~/.config/claude/claude_desktop_config.json` 中：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

**步骤 3：使用远程调试启动 Chrome**

Chrome 需要以启用远程调试的方式运行：

**macOS：**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222
```

**Windows：**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Linux：**
```bash
google-chrome --remote-debugging-port=9222
```

### 方法 B — 使用持久化认证配置文件

标准的 Chrome DevTools MCP 安装会在一个全新的隔离配置文件中启动 Chrome。这适用于基本自动化，但无法用于需要认证的网站。关键是 Chrome 的 `--user-data-dir` 标志——它创建一个单独的配置文件目录，Chrome 在其中保存所有登录会话、cookies 和浏览数据。

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"
```

然后通过 `--browserUrl` 配置 MCP 连接：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://localhost:9222"]
    }
  }
}
```

> ⚠️ **安全注意：** 打开远程调试端口会将你的浏览器暴露给机器上的任何应用程序。只在开发和测试中使用此设置。不要在启用远程调试的 Chrome 实例中浏览敏感网站。

### 方法 C — cdp-cli（轻量级替代方案）

安装一个独立的 CDP CLI 工具作为 MCP 服务器的替代方案——你可以确切看到它在做什么，并且它不会传输完整的 DOM 树，从而节省 tokens：

```bash
npm install -g @myerscarpenter/cdp-cli

# 列出打开的标签页
cdp-cli tabs

# 读取标签页的控制台日志
cdp-cli console "GitHub" --tail 5

# 截取截图
cdp-cli screenshot "GitHub" --output screenshot.jpg
```

---

## 第二部分：在 OpenClaw 中设置 CDP

OpenClaw 集成了 Google 官方的 Chrome DevTools MCP 服务器，让 AI agent 直接操作你的 Chrome 浏览器——读取页面、点击元素、填写表单、记录性能跟踪、分析网络请求，所有这些都通过 CDP。

OpenClaw 提供 **三种浏览器控制模式**：

### 模式 1 — OpenClaw 托管（隔离，默认）

OpenClaw 托管（端口 18800–18899）提供隔离的 Chromium 实例，适用于安全的自动化。这是推荐的起点。

```bash
# 启动托管浏览器
openclaw browser start

# 检查状态
openclaw browser status

# 捕获当前页面的快照
openclaw browser snapshot --interactive --compact --depth 6

# 通过 ref 点击元素
openclaw browser click e12

# 在字段中输入
openclaw browser type e15 "your text"

# 截图
openclaw browser screenshot --full-page
```

### 模式 2 — 现有会话（你的已登录 Chrome）

OpenClaw 使用官方 Chrome DevTools MCP 的 `--autoConnect` 流程。它附加到你现有的 Chrome 会话（带有你的登录状态和 cookies）。

```bash
# 使用你现有的 Chrome 配置文件启动
openclaw browser --browser-profile user start
```

> 注意：此路径的风险高于隔离的 OpenClaw 配置文件，因为它可以在你已登录的浏览器会话中操作。OpenClaw 不会为此驱动程序启动浏览器；它仅附加到现有会话。

### 模式 3 — 远程 CDP（云/外部浏览器）

对于远程 headless Chromium，将以下配置粘贴到你的 `openclaw.json` 中：

```json
"browser": {
  "enabled": true,
  "attachOnly": true,
  "defaultProfile": "remote",
  "profiles": {
    "remote": {
      "cdpUrl": "http://your-browser-host:9222",
      "color": "#FF4500"
    }
  }
}
```

### 安装 Playwright（高级功能所需）

某些功能（navigate、act、AI snapshot、role snapshot、元素截图、PDF）需要 Playwright。如果看到“Playwright is not available”，请安装它：

```bash
npm install playwright
# 然后重启 Gateway
```

---

## 快速比较表

| 功能 | Claude Code (MCP) | OpenClaw |
|---|---|---|
| 协议 | CDP via MCP | CDP via Playwright/Extension |
| 隔离浏览器 | ✅ | ✅ (Managed mode) |
| 使用现有登录会话 | ✅ (with `--user-data-dir`) | ✅ (Existing-session mode) |
| 远程 CDP | ✅ | ✅ |
| 截图 | ✅ | ✅ |
| 元素点击 | ✅ | ✅ |
| 认证支持 | Requires profile setup | Built-in via `user` profile |

参考资料：

- [Chrome DevTools MCP — GitHub (Official)](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [OpenClaw Browser Docs](https://docs.openclaw.ai/tools/browser)
- [Setup Guide: Authenticated Chrome Debugging with Claude Code](https://raf.dev/blog/chrome-debugging-profile-mcp/)
- [cdp-cli for Claude Code](https://icepick.info/2025/10/28/chrome-devtools-cli-for-claude-code/)
- [OpenClaw + Chrome DevTools MCP Guide (Medium)](https://medium.com/@tentenco/openclaw-chrome-devtools-mcp-how-to-give-your-local-agent-full-browser-control-a4e7c723a649)
- [OpenClaw Browser Control Deep Dive](https://blog.laozhang.ai/en/posts/openclaw-browser-control)
