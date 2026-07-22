---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Agent Note Extension
translated: false
type: note
---

Done. Here's a summary of the Pi Agent **note extension** I created at `~/.pi/agent/extensions/note/index.ts`:

---

## What it does

Registers a `/note` command that captures assistant responses and appends them to `~/.config/pi/note_queue.json` as a JSON array — the same queue-based pattern as your Hermes plugin.

## How it works

| Feature | Implementation |
|---|---|
| **`/note`** | Enqueues the last non-empty assistant response |
| **`/note 3`** | Enqueues the 3rd assistant response |
| **`/note --title "My Title"`** | Adds a `title` field to the queue entry |
| **Reasoning tags** | Strips `<thinking>`, `<reasoning>`, `<scratchpad>` tags automatically |
| **Queue file** | `~/.config/pi/note_queue.json` — an array of `{id, timestamp, title?, text}` objects |

## Pi vs Hermes API mapping

| Hermes (Python) | Pi Agent (TypeScript) |
|---|---|
| `ctx.register_command("note", ...)` | `pi.registerCommand("note", { ... })` |
| `cli.conversation_history` | `ctx.sessionManager.getEntries()` (filter by `type: "message"` + `role: "assistant"`) |
| `ctx._manager._cli_ref` | No private field access needed — stable public API |
| Plugin lives in `~/.hermes/plugins/note/` | Extension lives in `~/.pi/agent/extensions/note/index.ts` |

## Using it

Since it's in `~/.pi/agent/extensions/note/index.ts`, Pi Agent auto-discovers it on startup. Run `/reload` in an active session to pick it up, then:

```
/note                              # enqueue last response
/note 2 --title "Refactor plan"    # enqueue 2nd response with a title
```

An external daemon (like your `ww note watch`) can poll `~/.config/pi/note_queue.json` and process new entries.