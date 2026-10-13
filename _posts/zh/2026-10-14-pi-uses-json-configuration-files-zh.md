---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 树莓派使用JSON配置文件
translated: true
type: note
---

已检查。关键发现：**pi 不使用 `config.yaml`** —— 在 agent 目录 `~/.pi/agent/` 中全都是 JSON 文件。当前状态如下：

## 远程机器（`192.168.1.137`）——尚无模型配置

```
~/.pi/agent/
├── install/managed-install.json   ← 安装标记（当前唯一存在的文件）
└── bin/pi
```

- **没有 `settings.json`**、**没有 `models.json`**、**没有 `auth.json`** —— 这是一个全新安装；我们只运行过 `pi --version`，从未进行过完整会话。
- **没有 provider 凭据**：已设置 0 个 provider/API 密钥环境变量（`OPENAI_*`、`ANTHROPIC_*`、`OPENROUTER_API_KEY`……）。
- 因此目前 pi 启动时会使用**自动/内置模型目录，但没有可用的认证** —— `/model` 会显示没有可用模型，直到你 `/login` 或设置 API 密钥环境变量。

## 参考：本机的配置（“已配置”的样子）

`~/.pi/agent/settings.json`:
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
- `models.json`：不存在（没有自定义 endpoints）
- `auth.json`：空的 `[]` —— 本机通过 `OPENROUTER_API_KEY` 环境变量对 OpenRouter 进行认证，而不是存储的凭据

## 模型配置存放位置（文档：`configuration.md` / `settings.md`）

| 文件 | 用途 |
|---|---|
| `~/.pi/agent/settings.json` | `defaultProvider`、`defaultModel`、`defaultThinkingLevel`、`enabledModels`、主题 |
| `~/.pi/agent/models.json` | 自定义/兼容 endpoints（Ollama、vLLM、代理……） |
| `~/.pi/agent/auth.json` | 由 `/login` 写入的凭据（或使用环境变量） |

需要我将你的 `settings.json` **复制到远程机器**吗（OpenRouter / `xiaomi/mimo-v2.6-flash` / 思考级别 `high`）？你仍然需要在该主机上提供 `OPENROUTER_API_KEY` —— 要么在它的 shell 配置文件中导出，要么在那里运行 `pi` → `/login` 进行交互式登录。