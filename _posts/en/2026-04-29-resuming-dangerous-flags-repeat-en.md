---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resuming Requires Repeating Dangerous Flags
translated: false
type: note
---

Question: Do I still need to pass `--dangerously-skip-permissions` when resuming a previous Claude session with `--resume`?

Answer:

Yes — in most CLI designs (including Claude Code-style tools), you still need to explicitly pass `--dangerously-skip-permissions` again when you resume a session.

### Why this is required

* **Flags are not persisted for safety reasons**
  Security-related flags like `--dangerously-skip-permissions` are treated as *explicit consent per execution*, not stored in session state.

* **Resume restores conversation, not execution policy**
  `--resume <session-id>` typically reloads:

  * chat history
  * tool context
  * previous outputs

  But it does **not automatically re-enable bypassed permission modes**, because that would create a risk where a previously safe session becomes implicitly unsafe.

* **Design principle: “re-consent per run”**
  Especially for flags that:

  * bypass file system restrictions
  * allow unsafe tool execution
  * disable sandbox protections

  The CLI usually requires re-declaring them every time the process starts.

### Practical implication

So your command is correct:

```bash
claude --resume d79629a0-c3a2-40e7-8f36-b21bf7d0d53c --dangerously-skip-permissions
```

If you omit the flag, the resumed session will likely:

* fall back to default permission checks, or
* block operations that previously worked

### Mental model

Think of it like:

* `--resume` = “reload memory”
* `--dangerously-skip-permissions` = “start with elevated privileges”

They operate on different layers, so both must be specified.

References:

* [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code) (general CLI behavior patterns)
