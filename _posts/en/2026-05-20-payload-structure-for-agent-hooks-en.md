---
audio: false
generated: true
image: false
lang: en
layout: post
title: Payload Structure for Agent Hooks
translated: false
type: note
---

Here's the complete picture. The payload is constructed in `agent/shell_hooks.py:465-481` (`_serialize_payload`). For your `post_llm_call` hook, this is what gets piped to `stdin`:

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

**What goes where:**

| Field | Source |
|-------|--------|
| `hook_event_name` | Always `"post_llm_call"` |
| `tool_name` | Always `null` for non-tool events |
| `tool_input` | Always `null` for non-tool events |
| `session_id` | `kwargs.get("session_id")` |
| `cwd` | `Path.cwd()` at render time |
| `extra` | **Everything else** not in `_TOP_LEVEL_PAYLOAD_KEYS` (`{"tool_name", "args", "session_id", "parent_session_id"}`) |

The `extra` keys come from the invocation in `run_agent.py:15804-15812`:

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

**Other hooks have different payloads.** Quick reference:

| Hook | `tool_name` | `tool_input` | Notable `extra` keys |
|------|-------------|-------------|----------------------|
| `pre_tool_call` | `"terminal"` etc. | `{"command": "..."}` | `task_id`, `tool_call_id` |
| `post_tool_call` | `"terminal"` etc. | `{"command": "..."}` | `task_id`, `result`, `duration_ms`, `tool_call_id` |
| `pre_llm_call` | `null` | `null` | `user_message`, `platform`, `conversation_history` |
| `post_llm_call` | `null` | `null` | `user_message`, `assistant_response`, `conversation_history`, `model`, `platform` |
| `on_session_start` | `null` | `null` | `platform`, `session_id` |
| `on_session_end` | `null` | `null` | `platform`, `session_id` |
| `subagent_stop` | `null` | `null` | `child_role`, `duration_ms`, `result_summary` |

So in your script, you can access `extra.assistant_response` to show a snippet of the answer, `extra.model` to know which model was used, or `extra.platform` to know where it ran. Want me to update the notification to include any of those?