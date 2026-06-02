---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Acpx 插件设置指南
translated: true
type: note
---

**问题：** 如何在此桥上配置 acpx（浏览器控制）插件？

**回答：**

**acpx** 插件是 OpenClaw（以及几个类似本地 AI 代理框架）使用的浏览器控制/自动化桥接，用于赋予代理真正的浏览器功能。

以下是根据您的具体设置配置/安装/启用 **acpx** 浏览器插件的最常见方法：

### 1. 快速推荐方法（大多数用户 — OpenClaw CLI / bridge）

```bash
# Make sure you already have OpenClaw installed & updated
pip install --upgrade openclaw

# Install & register the acpx browser plugin (this downloads a small chromium + extension)
openclaw plugin install acpx

# Alternative longer name people sometimes use:
openclaw plugin install browser-acpx
```

安装后，您通常会看到：

```
Plugin 'acpx' installed successfully.
Browser profile 'openclaw' created.
```

然后重启您的 OpenClaw bridge / server：

```bash
# If you're running the default bridge
openclaw bridge restart

# or if you run it manually / in docker / systemd
# just restart the process that runs openclaw bridge
```

### 2. 手动/高级安装（自动安装失败或您想要自定义 profile 时）

```bash
# 1. Install playwright browsers (acpx uses playwright under the hood)
pip install playwright
playwright install chromium --with-deps

# 2. Install the acpx plugin explicitly from git (latest / bleeding edge)
pip install git+https://github.com/openclaw/acpx.git

# 3. Create / register the managed profile
acpx profile create --name openclaw --theme orange

# 4. Tell OpenClaw to use it (usually automatic, but you can force it)
openclaw config set browser.backend acpx
openclaw config set browser.profile openclaw
```

### 3. 如果您想连接到您的**真实现有浏览器**（Extension Relay 模式）

1. 安装 **OpenClaw Browser Relay** 扩展
   → Chrome Web Store：搜索 "OpenClaw Browser Relay" 或直接访问
   <https://chromewebstore.google.com/detail/openclaw-browser-relay/……>

2. 在 Chrome 中启用开发者模式 → 加载未打包 → 如果手动克隆，请指向文件夹

3. 在扩展弹出窗口 → 点击“Copy WebSocket URL”（看起来像 `ws://127.0.0.1:9222/devtools/browser/xxxx-xxxx`）

4. 将该 URL 粘贴到您的 OpenClaw bridge 配置中或在被询问时：

```bash
openclaw config set browser.backend acpx-relay
openclaw config set browser.websocket ws://127.0.0.1:9222/devtools/browser/……
```

**重要提示**

- 大多数人使用**托管隔离 profile**（`openclaw` profile）能获得良好结果 — 它更安全，避免干扰您的个人登录。
- **relay 模式**更强大（使用您的真实 cookies/会话），但也更具风险 — 仅在您完全信任代理的操作时使用。
- 配置 acpx 后，使用简单命令测试它，例如：
  `openclaw "open google.com and tell me what the Google logo says"`

如果这些步骤后仍出现“acpx 插件未配置”错误，请分享：

- 您运行的确切 OpenClaw 版本（`openclaw --version`）
- 是否使用 docker / pip / binary
- 启动 bridge 时的完整错误消息

这将有助于更快定位问题。

**参考资料：**

- [OpenClaw 浏览器工具文档](https://docs.openclaw.ai/tools/browser)
- [ACPX GitHub 仓库](https://github.com/openclaw/acpx)
- [OpenClaw 插件安装指南](https://docs.openclaw.ai/setup/plugins)
