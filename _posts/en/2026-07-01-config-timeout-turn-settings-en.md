---
audio: false
generated: true
image: false
lang: en
layout: post
title: Config Timeout & Turn Settings
translated: false
type: note
---

Since the timeout expired, here's a summary of the current situation:

**Current config** (`~/projects/config/hermes/config.yaml`):

```
agent.max_turns: 60        ← main interaction budget
goals.max_turns: 20
```

**`max_turns: 60`** means the agent stops after 60 turns per session — so 60 back-and-forth exchanges between you and the AI. Once you hit that, the session ends.

To increase it, just tell me what value you want. Common values:

- **100** — moderate bump
- **200** — for heavy coding sessions
- **unlimited** (set to `null`) — no limit

If you have the other laptop accessible (maybe via the same github config repo but with different commits pushed from there), I can try to pull from origin to see if a different version was pushed.
