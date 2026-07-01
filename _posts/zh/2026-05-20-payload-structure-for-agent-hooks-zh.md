---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理钩子的有效负载结构
translated: true
type: note
---

完整说明如下：载荷在 `agent/shell_hooks.py:465-481`（`_serialize_payload`）中构建。对于你的 `post_llm_call` 钩子，以下内容将通过 `stdin` 传入：

```json
{
  "hook_event_name": "post_llm_call",
  "tool_name": null,
  "tool_input": null,
  "session_id": "sess_abc123",
  "cwd": "/Users/lzwjava/projects/jekyll-ai-blog",
  "extra": {
    "user_message": "what the user asked",
    "assistant_response": "the agent's final response text",
    "conversation_history": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ],
    "model": "deepseek/deepseek-v4-pro",
    "platform": "cli"
  }
}
```

**各字段说明：**

| 字段 | 来源 |
| ------ | ------ |
| `hook_event_name` | 始终为 `"post_llm_call"` |
| `tool_name` | 非工具事件始终为 `null` |
| `tool_input` | 非工具事件始终为 `null` |
| `session_id` | `kwargs.get("session_id")` |
| `cwd` | 渲染时的 `Path.cwd()` |
| `extra` | **除** `_TOP_LEVEL_PAYLOAD_KEYS`（`{"tool_name", "args", "session_id", "parent_session_id"}`）之外的所有其他内容 |

`extra` 中的键来自 `run_agent.py:15804-15812` 中的调用：

```python
_invoke_hook("post_llm_call",
    session_id=self.session_id,
    user_message=original_user_message,       # → extra
    assistant_response=final_response,        # → extra
    conversation_history=list(messages),      # → extra
    model=self.model,                          # → extra
    platform=getattr(self, "platform", None) or "",  # → extra
)
```

**其他钩子具有不同的载荷。** 快速参考：

| 钩子 | `tool_name` | `tool_input` | 重要 `extra` 键 |
| ------ | ------------- | ------------- | ------------------ |
| `pre_tool_call` | `"terminal"` 等 | `{"command": "..."}` | `task_id`, `tool_call_id` |
| `post_tool_call` | `"terminal"` 等 | `{"command": "..."}` | `task_id`, `result`, `duration_ms`, `tool_call_id` |
| `pre_llm_call` | `null` | `null` | `user_message`, `platform`, `conversation_history` |
| `post_llm_call` | `null` | `null` | `user_message`, `assistant_response`, `conversation_history`, `model`, `platform` |
| `on_session_start` | `null` | `null` | `platform`, `session_id` |
| `on_session_end` | `null` | `null` | `platform`, `session_id` |
| `subagent_stop` | `null` | `null` | `child_role`, `duration_ms`, `result_summary` |

因此，在你的脚本中，你可以通过 `extra.assistant_response` 获取回答片段，通过 `extra.model` 了解使用了哪个模型，或者通过 `extra.platform` 知道运行环境。需要我更新通知以包含这些信息吗？
