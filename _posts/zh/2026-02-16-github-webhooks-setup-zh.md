---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Webhooks 设置指南
translated: true
type: note
---

**Question:** 如何在 GitHub repository 中使用 webhooks？

**Answer:**

GitHub **webhooks** 允许你的外部服务器、服务或应用程序在 repository 发生特定事件（如 push、创建 pull request、打开 issue 等）时，实时接收 HTTP POST 请求。

以下是使用 GitHub Web 界面设置 repository webhook 的标准方法（最常用的方法）：

### 创建 repository webhook 的逐步指南

1. 进入你在 GitHub 上的 repository
   打开 https://github.com 并导航到你想要添加 webhook 的 repository。

2. 打开 Settings
   点击 **Settings**（你需要是该 repo 的所有者或拥有 admin 权限）。

3. 进入 Webhooks 栏目
   在左侧边栏中，点击 **Webhooks** → 然后点击 **Add webhook**（或 **Create webhook**）。

4. 填写 webhook 配置

   - **Payload URL**
     最重要的字段。输入你的服务器/endpoint 的 HTTPS URL，用于接收 webhook 事件。
     示例：`https://your-app.com/webhook/github` 或 `https://hooks.zapier.com/hooks/catch/123456/abcde/`

   - **Content type**
     选择：
     - `application/json`（最常用且推荐）
     - 或 `application/x-www-form-urlencoded`

   - **Secret**（强烈推荐）
     输入一个随机且安全的字符串（至少 30 个字符以上）。
     GitHub 将使用它创建 HMAC signature，你可以在服务器上进行验证，以确保请求确实来自 GitHub。
     可以轻松生成一个：`openssl rand -hex 20` 或使用在线安全随机生成器。

   - **SSL verification**
     保持启用状态（默认），除非你正在使用自签名证书进行测试（不推荐用于 production）。

   - **Which events would you like to trigger this webhook?**
     - 选择 **Let me select individual events**（推荐）
     - 选择你关注的事件，例如：
       - Pushes（代码被推送）
       - Pull requests（打开、关闭、合并等）
       - Issues（打开、编辑、关闭）
       - Releases
       - Commits comments
       - ……（查看 GitHub docs 中的完整列表）

     或者为了测试简单选择 **Send me everything**（长期不推荐 —— 会产生不必要的流量）。

5. 点击底部的 **Add webhook**。

6. 测试（可选但推荐）
   创建后，GitHub 会显示 **Recent Deliveries** 栏目。
   点击任何事件的 **Edit** → **Redeliver**，或者触发一个真实事件（git push、打开 PR 等），检查你的服务器是否收到了它。

### 你的服务器需要做什么

你的 endpoint 必须：

- 接受 **POST** 请求
- 快速返回 HTTP **2xx** 状态码（GitHub 会重试失败的投递）
-（推荐）使用 secret 验证 signature：

```python
# Python 示例 (Flask + hmac)
import hmac
import hashlib

def verify_signature(payload, secret, signature):
    expected = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

GitHub 发送的 header 为：`X-Hub-Signature-256: sha256=abc123...`

### 常见使用场景

- Continuous deployment (push → 部署到服务器/Vercel/Netlify)
- 在发生 push/PR 时通知 Discord/Slack/Teams
- 自动为 issues 添加 label 或运行 CI checks
- 将 repo 事件同步到外部数据库
- 触发 Jenkins/GitLab CI

### 重要安全事项与最佳实践

- Payload URL 始终使用 **HTTPS**
- 始终设置 **secret** 并验证 signatures
- 快速返回 2xx —— 不要在 webhook handler 中执行繁重的工作（应将其放入 queue）
- 使用 **individual events** 而不是 "everything"
- 监控 **Recent Deliveries** 以查看失败的请求

有关完整详细信息和所有可能事件 → 请参阅官方文档。

**References:**

- [Creating webhooks - GitHub Docs](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks)
- [About webhooks - GitHub Docs](https://docs.github.com/en/webhooks/about-webhooks)
- [Webhook events and payloads - GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
- [Best practices for using webhooks - GitHub Docs](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)
