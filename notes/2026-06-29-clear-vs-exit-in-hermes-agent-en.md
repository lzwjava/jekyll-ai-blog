---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clear vs Exit in Hermes Agent
translated: false
type: note
---

Question: When exiting Hermes agent, I've been using Ctrl+C to quit, but that's slow. Is it better to use a `clear` command to clear the current session instead?

Answer:

I can't verify the specifics here — "Hermes agent" isn't a tool I can confidently identify (there are several things called Hermes: the NousResearch Hermes models, various CLI agents, etc.), and I don't have your particular tool's docs in context. So I'll answer the general pattern, then tell you how to find the authoritative answer for your exact tool.

The distinction you're drawing is real and correct in principle:

- **`Ctrl+C`** sends `SIGINT`. In a well-behaved REPL/agent loop it interrupts the *current operation* (a running generation, a tool call). Many agents trap it to cancel an in-flight turn rather than quit. To actually *exit*, you often need `Ctrl+C` twice, or `Ctrl+D` (EOF), or a `/exit` command. The slowness you're feeling is likely the process catching the signal, tearing down async tasks / HTTP sessions, flushing state, and waiting on cleanup handlers.

- **`clear`** (if the agent supports it as a slash command like `/clear`) typically wipes the *conversation context* but keeps the process alive — no teardown, no restart, instant. That's why it feels faster: you're not killing and respawning the runtime, you're just zeroing the message history.

So they're not substitutes — they do different things:
- `clear` → reset context, stay in the session (fast, what you want between tasks)
- exit → actually terminate the process (only when you're done)

If your goal is "start a fresh conversation without the old context bleeding in," `clear` is strictly better than quit-and-restart: no cold start, no reloading config/model/tools.

To find your tool's exact commands, the fastest path:

```bash
# Find the binary and read its help
which hermes
hermes --help

# Inside the session, try the usual slash-command discovery
/help        # or
/?
```

Look specifically for whether `clear` is a shell command vs a slash command (`/clear`), and what the documented exit is (`/exit`, `/quit`, `Ctrl+D`). `Ctrl+D` is usually the cleanest fast-exit — it signals EOF to stdin, which most REPLs handle as an immediate graceful shutdown without the double-interrupt dance.

If you tell me which Hermes this is (repo URL or `pip`/`npm` package name), I'll read its source and give you the exact keybindings and what each one tears down.
