---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw OpenRouter API 密钥错误
translated: true
type: note
---

问题：这个错误是什么意思，我该如何修复："No API key found for provider 'openrouter'. Auth store: /root/.openclaw/agents/main/agent/auth-profiles.json"？

回答：

该错误来自 AI agent 框架 **OpenClaw**，意味着它无法找到为 **OpenRouter** provider 配置的 API key。以下是具体原因及修复方法：

## 发生了什么

OpenClaw 将 provider 凭据存储在如下路径的 JSON 文件中：

```
/root/.openclaw/agents/main/agent/auth-profiles.json
```

Agent 尝试启动，但在该文件中没有找到 OpenRouter API key，因此在执行回复之前中止了。

---

## 如何修复

### 方案 1：使用 OpenClaw CLI 添加凭据（推荐）

```bash
openclaw agents add main
```

此命令会提示你以交互方式输入 OpenRouter API key 并将其保存到 auth profile。

### 方案 2：手动编辑 `auth-profiles.json`

1. 打开文件：

   ```bash
   nano /root/.openclaw/agents/main/agent/auth-profiles.json
   ```

2. 按预期格式添加你的 OpenRouter key（通常如下所示）：

   ```json
   {
     "openrouter": {
       "api_key": "sk-or-..."
     }
   }
   ```

   *（确切的 schema 可能会有所不同 —— 请查看 OpenClaw 的文档以获取正确的结构。）*

3. 保存并重试运行 agent。

### 方案 3：从 main agent 目录复制 auth

错误信息暗示了这一点：

```bash
cp /root/.openclaw/agents/main/auth-profiles.json \
   /root/.openclaw/agents/main/agent/auth-profiles.json
```

如果你已经在父目录配置了凭据，但它们没有同步到 agent 子目录，请使用此方法。

---

## 获取 OpenRouter API Key

如果你还没有 key：

1. 前往 [https://openrouter.ai](https://openrouter.ai)
2. 注册或登录
3. 导航到账户控制面板中的 **Keys**
4. 创建一个新 key（以 `sk-or-...` 开头）

---

## 检查 Logs

如需了解失败的更多细节，请运行：

```bash
openclaw logs --follow
```

这可能会显示关于 agent 失败时尝试执行的操作的更多上下文。
