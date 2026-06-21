---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复小米的max_tokens参数
translated: true
type: note
---

好了，在检查了你的配置和代码库之后，以下是完整的情况。

## 你的配置

**配置：** `~/.hermes/config.yaml`
- 模型：`mimo-v2.5-pro`
- 提供商：`xiaomi`
- 基础 URL：`https://token-plan-cn.xiaomimimo.com/v1`
- **没有在任何地方配置 `max_tokens`** —— 既不在 `model:` 中，也不在 `agent:` 中，也不在 `.env` 中

**提供商配置文件：** `plugins/model-providers/xiaomi/__init__.py`
- `default_max_tokens` **未设置**（默认为 `None`）

---

## 根本原因

小米提供商的配置文件中**没有 `default_max_tokens`**。你的配置中也没有设置。因此，当代理调用小米 API 时，**根本没有发送 `max_tokens` 参数** —— 服务器会自行选择默认值。

服务器对 `mimo-v2.5-pro` 的默认输出上限似乎相对较低。当模型生成的响应超过该服务器端限制时，API 会返回 `finish_reason="length"`，Hermes 会报告：

    错误：由于输出长度限制，响应被截断

重试机制（最多 3 次尝试，并提高 `max_tokens`）也帮助不大，因为提高从 `agent.max_tokens` 开始，而该值为 `None`，因此回退到以 `4096` 为基础：

```python
# conversation_loop.py 第1741行
_tc_boost_base = agent.max_tokens if agent.max_tokens else 4096
_tc_boost = _tc_boost_base * (truncated_tool_call_retries + 1)
```

因此重试时会发送 `max_tokens=8192`，然后是 `12288`，再是 `16384` —— 这些值可能仍然低于服务器的实际限制。

---

## 修复

在你的配置中添加 `max_tokens`。`opencode-zen` 插件已经知道 `mimo-v2.5-pro` 支持 **131072** 个完成令牌。在 `config.yaml` 中设置：

```yaml
model:
  default: mimo-v2.5-pro
  provider: xiaomi
  base_url: https://token-plan-cn.xiaomimimo.com/v1
  max_tokens: 131072    # <-- 添加这一行
```

或者更保守一点，如果你想节省令牌：

```yaml
  max_tokens: 32768
```

需要我将其添加到你的配置中吗？