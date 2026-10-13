---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 API 密钥复制到远程？
translated: true
type: note
---

完成——`settings.json` 已复制并在远程验证：

```json
{
  "lastChangelogVersion": "1.2.0",
  "theme": "dark",
  "defaultProvider": "openrouter",
  "defaultModel": "xiaomi/mimo-v2.6-flash",
  "hideThinkingBlock": false,
  "defaultThinkingLevel": "high"
}
```

复制后 `pi --version` 仍然显示 1.2.0。

**还差凭据。** 你本地机器从 `~/.bashrc` 获取 `OPENROUTER_API_KEY`（`auth.json` 是空的 `{}` —— 所以这个 key 是唯一的凭据）。远程机器没有凭据，所以 `/model` 在以下情况之一满足前不会显示可用模型：

1. **我来复制 key** —— 我会从你本地的 `~/.bashrc` 中提取 `OPENROUTER_API_KEY`，并追加到 `lzw@192.168.1.137:~/.bashrc`，按 `chmod 600` 的语义处理（这是你的 key、你的机器）。说一声就行。
2. **你自己在那边设置**：`echo 'export OPENROUTER_API_KEY=...' >> ~/.bashrc`
3. **在远程用交互式 `/login`**（会存到 `auth.json`）。

要我执行选项 1 吗？
