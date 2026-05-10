---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes模型配置方法
translated: true
type: note
---

问题：如何更改 Hermes Agent 的默认模型？

回答：

更改 Hermes Agent（由 Nous Research 开发）的默认模型有**四种主要方法**：

---

## 方法一：交互式 CLI 命令（推荐）

在终端中运行交互式模型选择器：

```bash
hermes model
```

该命令可让你以交互方式切换提供商和模型。它还能处理需要设置尚未配置的新提供商的情况。

你也可以通过一行命令直接设置模型：

```bash
hermes model set anthropic/claude-opus-4.7 --provider openrouter
```

---

## 方法二：直接编辑 `~/.hermes/config.yaml`

当你通过控制面板或 CLI 保存时，Hermes 会将配置写入 `~/.hermes/config.yaml`。典型的模型配置如下：

```yaml
model:
  provider: openrouter
  default: anthropic/claude-opus-4.7
  base_url: ''
  api_mode: chat_completions
```

在 `model:` 配置部分中，你可以使用 `default:` 或 `model:` 作为模型 ID 的键名——两者效果相同。

编辑后，请重启 Hermes 会话以使更改生效。

---

## 方法三：在运行会话中热切换模型（聊天内）

在聊天中使用 `/model <名称>` 即可热切换当前会话的模型，无需重启。新的会话不会继承此更改——它们会从 `config.yaml` 中读取配置。

你也可以使用 `--global` 标志同时更改运行会话及持久化配置：

```bash
hermes model set anthropic/claude-opus-4.7 --global
```

---

## 方法四：使用模型别名

你可以在 `~/.hermes/config.yaml` 中为常用模型定义简短别名，然后在聊天或 CLI 中使用 `/model <别名>`：

```yaml
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  grok:
    model: grok-4
    provider: x-ai
```

或者通过 CLI 进行设置：

```bash
hermes config set model.aliases.fav anthropic/claude-opus-4.6
```

然后在聊天中使用 `/model fav`。

---

## 重要说明

- 配置的优先级顺序为：**CLI 覆盖 → config.yaml → .env → 默认值**。
- Hermes Agent 要求模型至少拥有 **64,000 token 的上下文**。上下文窗口较小的模型将在启动时被拒绝。
- `.env` 中的 `LLM_MODEL` 环境变量**已不再被读取**——请改用 `hermes model` 或 `hermes setup`。
- 提供商必须拥有有效的凭据（API 密钥、OAuth 或自定义端点 URL）后，才会显示为可用选项。运行 `hermes setup` 来配置新的提供商。

参考链接：

- [Configuring Models | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
- [Configuration | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [AI Providers | Hermes Agent](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [cli-config.yaml.example | GitHub](https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example)
- [Quickstart | Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)