---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Completion Hooks Overview
translated: false
type: note
---

Here's the summary.

---

**Yes, there are hooks that fire after Hermes finishes.** Three systems:

### 1. Gateway event hooks (`agent:end`)

The `agent:end` event fires when the agent finishes processing a message. Only works in the gateway (Telegram, Discord, etc.), not the CLI. Create a hook directory at `~/.hermes/hooks/<name>/` with `HOOK.yaml` + `handler.py`.

```yaml
# HOOK.yaml
events:
  - agent:end
```

The `context` dict includes `platform`, `user_id`, `session_id`, `message`, and `response`.

Docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks#gateway-event-hooks>

### 2. Plugin hooks (CLI + Gateway)

These work everywhere. The most relevant ones for "agent finished":

| Hook | When |
| ------ | ------ |
| `post_llm_call` | After the tool-calling loop completes for one turn |
| `transform_llm_output` | Same timing, but can **replace** the response text |
| `on_session_end` | Session is ending |
| `on_session_finalize` | CLI/gateway tears down session (flush, save, stats) |

Register in a plugin via `ctx.register_hook("post_llm_call", my_callback)`.

### 3. Shell hooks (CLI + Gateway)

Same events as plugin hooks, but defined in `config.yaml` and run as shell subprocesses. Writing a script is also an option — JSON piped to stdin, JSON on stdout.

```yaml
# ~/.hermes/config.yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
```

---

**The user doesn't need to cancel or interrupt.** In the CLI, the prompt loop (`process_loop` in cli.py) naturally returns to waiting for input after every agent response. `_agent_running` is set to `False` in a `finally` block (line 13555 in cli.py), and the loop goes back to `_pending_input.get()`. The next message you type just starts the next turn.

If you want to be notified when the agent is done so you know it's your turn to respond, you can enable the terminal bell:

```bash
hermes config set display.bell_on_complete true
```

This plays `\a` (terminal bell) whenever the agent finishes a response — works over SSH too.
