---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 标题生成中的API密钥错误
translated: true
type: note
---

**问题：** 为什么会出现“辅助标题生成失败：HTTP 401：无效 API 密钥”？

**回答：**

我追踪了完整的代码路径。以下是具体情况：

## 流程

1. 在第一次用户/助手对话后，`maybe_auto_title()` 触发一个后台线程 (agent/title_generator.py)
2. 它调用 agent/auxiliary_client.py 中的 `call_llm(task="title_generation", main_runtime=main_runtime)`
3. `_resolve_task_provider_model()` 读取配置 `auxiliary.title_generation`——您的配置设置为 `provider: auto`，且 model/base_url/api_key 为空
4. `_resolve_auto()` 会选取您的主 provider (xiaomi) + model (mimo-v2.5-pro) + base_url (https://token-plan-cn.xiaomimimo.com/v1)
5. 它会创建一个 OpenAI 客户端，并使用来自您 `.hermes/.env` 文件的 `XIAOMI_API_KEY`
6. 如果该密钥无效或已过期 → 小米 API 返回 HTTP 401

## 为什么主聊天正常但标题生成失败（或反之亦然）

密钥的解析路径略有不同：

- **主聊天**：在 agent 初始化时，使用凭据池/env 中的 API 密钥创建一个 OpenAI 客户端
- **标题生成**：在后台线程中通过 `resolve_provider_client()` 创建一个*独立*的缓存客户端，并从 `XIAOMI_API_KEY` 环境变量或凭据池中重新解析 API 密钥

如果密钥最近被轮换、过期，或者凭据池中有过期条目，一个路径可能使用缓存的有效客户端，而另一个路径则解析了一个新的（现在无效的）密钥。

## 来自您日志的证据

根据 `errors.log`，在 2026-05-29，两条路径都失败了：
```
10:13:25 API 调用失败 ... provider=xiaomi ... 摘要=HTTP 401: Invalid API Key
10:13:55 API 调用失败 ... provider=xiaomi ... 摘要=HTTP 401: Invalid API Key
10:14:13 API 调用失败 ... provider=xiaomi ... 摘要=HTTP 401: Invalid API Key
```

这些是主对话循环调用，而不仅仅是标题生成。您的 `XIAOMI_API_KEY` 当时已无效。在您更新密钥后，一切恢复正常——最近的日志（6 月 14 日-21 日）显示了成功的 title_generation 调用。

## 如果现在正在发生

401 错误意味着您 `~/.hermes/.env` 中的 `XIAOMI_API_KEY` 无效。请验证：

```bash
# 直接检查密钥是否有效
curl -s https://token-plan-cn.xiaomimimo.com/v1/models \
  -H "Authorization: Bearer *** | head -5
```

如果返回 401，请前往 https://platform.xiaomimimo.com 重新生成密钥，并更新 `~/.hermes/.env`。

## 如何抑制警告（如果密钥正常且只是瞬时波动）

您可以配置 title_generation 使用不同的 provider：
```yaml
auxiliary:
  title_generation:
    provider: xiaomi
    model: mimo-v2.5
    timeout: 30
```

或者，通过在 config.yaml 中设置 `auxiliary.title_generation.provider: none` 来完全禁用自动标题功能。