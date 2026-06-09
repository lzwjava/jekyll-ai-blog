---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent Turn Limit Reached
translated: false
type: note
---

**Your current config:**

```
agent:
  max_turns: 60        ← this is your iteration budget
```

That's why you hit 60/60. Want me to bump it? Common choices:

- `90` — the default
- `120` — comfortable headroom
- `200` — for heavy tasks

Also note line 366 (`delegation.max_iterations: 50`) caps each subagent independently.

Want me to change `max_turns` to a specific value? Just say the number.
