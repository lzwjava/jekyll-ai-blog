---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯智能体完成钩子概述
translated: true
type: note
---

以下为摘要。

---

**是的，Hermes 完成后会触发钩子。** 共有三个系统：

### 1. 网关事件钩子（`agent:end`）

当代理处理完一条消息时，会触发 `agent:end` 事件。仅适用于网关（Telegram、Discord 等），不适用于 CLI。在 `~/.hermes/hooks/<name>/` 下创建钩子目录，内含 `HOOK.yaml` 和 `handler.py`。

```yaml
# HOOK.yaml
events:
  - agent:end
```

`context` 字典包含 `platform`、`user_id`、`session_id`、`message` 和 `response`。

文档：<https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks#gateway-event-hooks>

### 2. 插件钩子（CLI + 网关）

这些钩子在所有环境中均有效。与“代理完成”最相关的钩子如下：

| 钩子 | 触发时机 |
| ------ | ---------- |
| `post_llm_call` | 单轮工具调用循环完成后 |
| `transform_llm_output` | 时机同上，但可以**替换**回复文本 |
| `on_session_end` | 会话结束时 |
| `on_session_finalize` | CLI/网关拆除会话（刷新、保存、统计） |

在插件中通过 `ctx.register_hook("post_llm_call", my_callback)` 注册。

### 3. Shell 钩子（CLI + 网关）

与插件钩子的事件相同，但在 `config.yaml` 中定义，并以 shell 子进程方式运行。也可以编写脚本——标准输入接收 JSON，标准输出输出 JSON。

```yaml
# ~/.hermes/config.yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
```

---

**用户无需取消或中断。** 在 CLI 中，提示循环（cli.py 中的 `process_loop`）会在每次代理回复后自然返回等待输入。`_agent_running` 在 `finally` 块（cli.py 第 13555 行）中被设为 `False`，循环回到 `_pending_input.get()`。你输入的下一条消息只是开始下一轮。

如果你想在代理完成时收到通知以便知道该你回复了，可以启用终端提示音：

```bash
hermes config set display.bell_on_complete true
```

这样每当代理完成回复时，就会播放 `\a`（终端提示音）——SSH 连接下同样生效。
