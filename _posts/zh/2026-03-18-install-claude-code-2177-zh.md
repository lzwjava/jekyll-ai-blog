---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装 Claude Code 版本 2.1.77
translated: true
type: note
---

**问题：** 如何安装 Claude Code 版本 2.1.77？

**回答：**

## 安装 Claude Code v2.1.77

根据您的安装方法，有两种主要方法。

---

### 方法 1：原生安装程序（推荐） — 安装特定版本

使用原生安装程序安装特定版本时，将版本号作为参数传递给安装脚本：

**macOS / Linux：**
```bash
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.77
```

**Windows (PowerShell)：**
```powershell
irm https://claude.ai/install.ps1 | iex
```
> 注意：Windows PowerShell 方法默认安装最新版本。要在 Windows 上安装特定版本，请使用 WSL 并在其内部运行上面的 Linux 命令。

---

### 方法 2：npm（旧版） — 安装特定版本

npm 方法仍然有效，但不再是推荐方法。如果您需要固定特定版本或在以 npm 为标准包管理器的环境中工作，请使用此方法。

```bash
npm install -g @anthropic-ai/claude-code@2.1.77
```

> **注意：** 这需要 Node.js 18.0+。如果看到 `EACCES` 权限错误，请**不要**使用 `sudo`。请修复您的 npm 权限。

---

### 方法 3：固定版本并禁用自动更新

安装后，如果您想停留在 `2.1.77` 并防止自动更新：

在您的 `settings.json` 文件的 `env` 键中将 `DISABLE_AUTOUPDATER` 设置为 `"1"`，以在固定版本后防止自动更新。

您的 `~/.claude/settings.json` 应如下所示：
```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

---

### 验证安装

```bash
claude --version
```

输出中应确认显示 `2.1.77`。

---

### 重要说明

- 原生安装程序更快，无需依赖项，并在后台自动更新。尽可能使用原生安装方法。
- Claude Code 需要付费账户 — Claude Pro（$20/月）适用于大多数开发者。如果您只需要 API 访问，具有信用的 Anthropic Console 账户也可以。

---

**参考资料：**

- [Claude Code 官方文档 – 高级设置](https://code.claude.com/docs/en/setup)
- [Claude Code 安装 – Vibe Coding With Fred](https://vibecodingwithfred.com/blog/claude-code-installation-guide/)
- [如何安装 Claude Code – morphllm.com](https://www.morphllm.com/install-claude-code)
- [npm – @anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code)