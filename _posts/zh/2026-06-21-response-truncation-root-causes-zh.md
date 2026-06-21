---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 响应截断根因
translated: true
type: note
---

现在情况已经很清楚了。以下是完整分析：

---

## 为什么会出现“Response truncated due to output length limit”

该错误来自 `agent/conversation_loop.py` 中的代理对话循环。当 LLM API 返回 `finish_reason="length"` 时触发——意味着模型在完成响应之前**达到了最大输出 token 限制**。

### 三种触发路径

1. **截断的工具调用（第1714–1777行）：** 模型开始生成工具调用（例如 `write_file(...)`），但 JSON 参数在途中被截断。代理会以提升的 `max_tokens` 重试最多3次。如果所有3次重试仍然截断，则放弃并返回此错误——因为使用格式错误的 JSON 参数执行工具存在危险。

2. **在 JSON 验证期间检测到截断的工具调用（第3900–3922行）：** 在后续循环中，当代理尝试解析工具调用参数时，会检查 JSON 是否不完整（不以 `}` 或 `]` 结尾）。如果截断，则出现相同错误。

3. **在3次继续尝试后文本响应仍截断（第1655–1712行）：** 模型的文本响应被截断。代理尝试通过注入“请继续”提示来继续，最多3次。如果3次后仍然截断，则返回一个略有不同的错误：`"Response remained truncated after 3 continuation attempts"`。

### 根本原因

| 原因 | 发生情况 |
|---|---|
| **`max_tokens` 设置过低** | 模型耗尽了输出预算。常见于长工具调用或冗长响应。 |
| **思考预算耗尽** | 模型将全部输出 token 用于 `` 块，导致实际响应没有空间。单独检测（第1592–1651行），并发出特定的“Thinking Budget Exhausted”消息。 |
| **网络/流中断** | 部分流存根（`PARTIAL_STREAM_STUB_ID`）——连接在响应中途断开。代理会将其与真正的截断区分开。 |
| **Ollama/GLM 的特殊行为** | 某些提供商对于实际是截断的情况返回 `finish_reason="stop"`。代理有一个启发式方法（`_should_treat_stop_as_truncated`）来捕捉这些情况。 |

### 如何应对

- **如果是模型达到 max_tokens：** 在配置中或通过 `/maxtokens` 增加 `max_tokens`。代理在重试时已经自动提升（第1741–1747行：`_tc_boost_base * (retry + 1)`，上限为32768）。
- **如果是思考预算耗尽：** 使用 `/thinkon low` 或 `/thinkon minimal` 减少推理 token 消耗，或切换到非推理模型。
- **如果是网络问题：** 流停滞检测（`_is_stub_stall`）处理此问题——这是瞬时问题，通常在重试时解决。

你遇到的是哪种具体情况？如果提供更多上下文，我可以进一步深入日志或配置。
