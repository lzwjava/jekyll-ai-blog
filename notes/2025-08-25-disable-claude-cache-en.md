---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Cache in Claude Code
translated: false
type: note
---

In **Claude Code**, that snippet

```json
"cache_control": {
  "type": "ephemeral"
}
```

means that the response (or artifact) produced by the model is **not cached for reuse**.

### Why it exists

Normally, Claude Code (and other Anthropic SDKs) may cache responses to speed things up if you send the same prompt again. But when you set `"cache_control": { "type": "ephemeral" }`, you’re telling the API:

* **Don’t persist this result in the cache**.
* **Don’t reuse it** if another identical request comes later.
* Treat the response as **short-lived**—only for this call.

### When to use

This is useful if:

* Your request includes **sensitive or personal data** you don’t want cached.
* You’re sending **one-off queries** that wouldn’t benefit from reuse.
* You want **fresh output** each time, even if the request text is identical.

In short, `"ephemeral"` makes Claude’s output *transient*—private to this interaction, with no caching across calls.

Would you like me to also explain how this differs from the default `cache_control` behavior in Claude Code (e.g. `type: "default"` vs `"none"` vs `"ephemeral"`)?
