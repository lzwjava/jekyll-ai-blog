---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guide to /compact in OpenClaw
translated: false
type: note
---

Question: How do I use the `/compact` command with instructions in OpenClaw (AI agent)?

Answer:

## What is `/compact` in OpenClaw?

The `/compact [instructions]` command compacts the session context and reports the remaining context budget. It is a built-in slash command available in your messaging interface (WhatsApp, Telegram, Discord, etc.) that helps you manage the AI's context window before it fills up completely.

---

## Basic Syntax

```
/compact
/compact [your optional instructions here]
```

---

## How It Works

### Without instructions

Sending `/compact` by itself will trigger context compaction and the agent will reply confirming the action, along with how much context budget remains.

### With instructions

You can append custom instructions to guide **what gets preserved or prioritized** during compaction. For example:

```
/compact Focus on the coding task we discussed. Forget the earlier grocery planning.
```

```
/compact Keep the API integration context. Summarize everything else briefly.
```

```
/compact Prioritize my project deadlines and ignore casual conversation history.
```

The instruction text after `/compact` tells the model how to summarize or filter the session history when compressing it.

---

## Why Use `/compact`?

OpenClaw agents accumulate context rapidly during long sessions. Your agent accumulates context fast. Periodically review what it's remembering and flush anything outdated. Do this **before** it hits compaction — once it auto-compacts, you lose control over what gets kept.

Using `/compact` manually (with instructions) gives you control over what the agent retains vs. discards, rather than letting it auto-compact arbitrarily.

---

## Related Session Commands

You can also use `/new` or `/reset` to start a fresh session for that chat (configurable via `resetTriggers`). If sent alone, the agent replies with a short hello to confirm the reset.

| Command | Effect |
| --- | --- |
| `/compact` | Compress context, report remaining budget |
| `/compact [instructions]` | Compress with guidance on what to keep |
| `/new` or `/reset` | Wipe session and start fresh |
| `/status` | Show compact session status (model + tokens, cost) |

---

## Tips

- Use `/compact` **before** the context window is exhausted — once the agent auto-compacts, you lose manual control.
- Always include specific instructions when you want to preserve a particular task thread (e.g., a coding project or ongoing research).
- After compaction, the agent will report how much context budget is remaining, helping you plan when you need to compact again.

References:

- [OpenClaw Personal Assistant Setup (Official Docs)](https://docs.openclaw.ai/start/openclaw)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [How to Deploy Your Own AI Agent – Complete OpenClaw Setup Guide](https://jsmastery.com/blogs/how-to-deploy-your-own-ai-agent-the-complete-openclaw-setup-guide)
