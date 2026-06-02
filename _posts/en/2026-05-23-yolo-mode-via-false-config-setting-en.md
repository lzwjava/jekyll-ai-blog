---
audio: false
generated: true
image: false
lang: en
layout: post
title: YOLO Mode via False Config Setting
translated: false
type: note
---

Current status:

- **YOLO flag (--yolo):** Not passed this session
- **HERMES_YOLO_MODE env var:** Not set
- **approvals.mode in config.yaml:** `false`

The `approvals.mode` is set to `false`, which is not one of the valid values (`manual`, `smart`, `off`). Since `false` is falsy, it's likely being treated as "off" — meaning approval prompts are bypassed, effectively YOLO mode.

To be explicit, you could set it to a recognized value:

```bash
hermes config set approvals.mode off      # explicit YOLO
hermes config set approvals.mode manual   # always prompt (default)
hermes config set approvals.mode smart    # LLM decides
```

So yes — you're effectively in YOLO mode right now.
