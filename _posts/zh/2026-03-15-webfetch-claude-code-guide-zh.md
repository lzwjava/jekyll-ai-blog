---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 的 WebFetch 工具指南
translated: true
type: note
---

## Claude Code 中的 WebFetch 工具

`WebFetch` 工具是 Claude Code 的内置工具，它允许 Claude 在代理会话期间 **检索和分析网页内容**。

---

### 它做什么

| 功能 | 详情 |
|---|---|
| **Input** | 一个 URL + 描述要提取内容的提示 |
| **Process** | 获取 URL，将 HTML 转换为 Markdown，然后使用小型/快速模型根据您的提示处理内容 |
| **Output** | 模型关于页面内容的响应 |
| **Cache** | 15 分钟自动清理缓存，以加速重复获取同一 URL |

---

### 关键行为

**✅ 它处理良好的内容：**
- 公共网页（博客、文档、新闻文章等）
- HTTP URL — 自动升级为 HTTPS
- 大型页面 — 如果内容太大，结果可能会被总结
- 重定向 — 通知您重定向 URL，以便您手动发出新请求

**❌ 它无法做的事：**
- 访问 **受认证或私有 URL** (Google Docs、Confluence、Jira、GitHub 私有仓库等) — 它将 **失败**
- 修改任何文件（只读工具）

---

### 优先规则

```
1. 如果有 MCP 提供的 web fetch 工具可用 → 使用那个而不是这个
2. 对于 GitHub URL → 优先使用 Bash 中的 gh CLI (gh pr view、gh issue view、gh api)
3. 对于受认证服务 → 使用专用的 MCP 工具，而不是 WebFetch
4. 对于公共 URL → WebFetch 就可以
```

---

### 实际示例

```
URL:    https://docs.anthropic.com/en/docs/overview
Prompt: "Summarize the main features of Claude's API"
```

Claude 获取页面，将其 HTML 解析为 Markdown，然后快速模型根据提示提取所需内容 — 返回给您干净的摘要。

---

### 为什么关于 Auth URL 的警告？

许多开发者本能地粘贴 Jira 票据、GitHub PR 或 Google Doc URL — 但 WebFetch **没有 session/cookie/token**，因此会撞上登录墙并失败。该工具提前警告您 **首先检查 URL 是否需要认证**，如果是，则找到合适的 MCP 连接器代替（例如 GitHub MCP 工具、Confluence MCP 工具等）。
