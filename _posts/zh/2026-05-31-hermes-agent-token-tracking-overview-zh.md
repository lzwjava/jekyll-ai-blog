---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯代理令牌追踪概述
translated: true
type: note
---

现在我有了完整的图景。以下是 Hermes Agent 中 token 跟踪的工作方式：

---

Token 跟踪共有三个层次：

## 1. 每次 API 调用的累积（agent/conversation_loop.py，约第 1780-1886 行）

每次 API 调用后，响应的 `usage` 对象通过 `agent/usage_pricing.py` 中的 `normalize_usage()` 规范化为 `CanonicalUsage` 数据类：

```python
CanonicalUsage(
    input_tokens=...,      # 原始输入（不包括缓存）
    output_tokens=...,     # 生成的 token
    cache_read_tokens=..., # 缓存命中
    cache_write_tokens=...,# 缓存写入
    reasoning_tokens=...,  # 思考/推理 token
)
```

这些值累加到 `AIAgent` 实例的会话计数器上（定义在 `run_agent.py` 第 625-636 行）：

```
agent.session_input_tokens      += canonical_usage.input_tokens
agent.session_output_tokens     += canonical_usage.output_tokens
agent.session_cache_read_tokens += canonical_usage.cache_read_tokens
agent.session_cache_write_tokens+= canonical_usage.cache_write_tokens
agent.session_reasoning_tokens  += canonical_usage.reasoning_tokens
agent.session_total_tokens      += total_tokens
agent.session_api_calls         += 1
agent.session_estimated_cost_usd += cost
```

同时通过 `SessionDB.update_token_counts()`（`hermes_state.py`）持久化到 SQLite。

## 2. /usage 斜杠命令

在 CLI 或网关中，输入 `/usage`。它会：

- 读取活动代理的实时会话计数器（在回合中）或缓存代理（回合之间）
- 调用 `agent/account_usage.py` 中的 `fetch_account_usage()` 获取提供商级别的速率限制
- 调用 `agent/usage_pricing.py` 中的 `estimate_usage_cost()` 进行成本估算
- 显示：模型、输入 token、缓存读/写、输出 token、总计、API 调用次数、成本、上下文窗口百分比

网关处理器：`gateway/run.py` 第 13194 行（`_handle_usage_command`）。

## 3. 关键文件搜索/阅读

| 你想要的内容 | 文件 | 搜索内容 |
|---|---|---|
| Token 累加逻辑 | `agent/conversation_loop.py` | `session_input_tokens`, `canonical_usage` |
| 会话计数器初始化 | `run_agent.py` | `session_total_tokens = 0`（第 625 行） |
| 规范化原始 API 用量 | `agent/usage_pricing.py` | `normalize_usage`, `CanonicalUsage` |
| 成本估算 | `agent/usage_pricing.py` | `estimate_usage_cost`, `PricingEntry` |
| SQLite 持久化 | `hermes_state.py` | `update_token_counts`（第 938 行） |
| /usage 命令（网关） | `gateway/run.py` | `_handle_usage_command`（第 13194 行） |
| /usage 命令（CLI） | `cli.py` | 在 `process_command` 中搜索 `usage` |
| 账户级别限制 | `agent/account_usage.py` | `fetch_account_usage` |
| 提供商特定解析 | `agent/gemini_native_adapter.py` | `usageMetadata`, `promptTokenCount` |
| 随时间变化的洞察 | `agent/insights.py` | `InsightsEngine` |

## 快速检查当前会话 token 的方法

在 CLI 交互式会话中，只需输入：

```
/usage
```

或者在调用 `chat()` 之后以编程方式检查：

```python
agent = AIAgent(...)
agent.chat("hello")
print(f"In: {agent.session_input_tokens}, Out: {agent.session_output_tokens}, Total: {agent.session_total_tokens}")
print(f"API calls: {agent.session_api_calls}, Cost: ${agent.session_estimated_cost_usd:.4f}")
```

`/insights` 命令（第 13331 行）可提供跨会话的历史分析，数据来自 SQLite 数据库。
