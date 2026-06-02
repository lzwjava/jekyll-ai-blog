---
audio: false
generated: true
image: false
lang: en
layout: post
title: "YOLO Mode On: Config Details"
translated: false
type: note
---

Yes — **YOLO is on**. Your config has:

```yaml
approvals:
  mode: false
```

`mode: false` (aka `"off"`) means all approval prompts are skipped — functionally equivalent to `--yolo`. Dangerous commands pass through without asking, though the **hardline blocklist** (`rm -rf /`, `dd if=... of=/dev/sda`, `shutdown`, etc.) still blocks unconditionally regardless of YOLO.

To turn it off, you can either:
- `/yolo` in-session to toggle (it's a slash command)
- Set `approvals.mode: manual` in `~/.hermes/config.yaml` to always prompt
