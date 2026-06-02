---
audio: false
generated: true
image: false
lang: en
layout: post
title: WW Host Naming Justification
translated: false
type: note
---

Good question. Here's my take:

**`ww host`** is the right name.

Why it fits:

- Standard SSH/DevOps terminology for "a compute endpoint you interact with"
- Covers all three: local Mac, self-built desktop, cloud VPS
- Short, single syllable, easy to type
- `ww host local`, `ww host workstation`, `ww host dmit` — reads naturally

Why others don't:

- `machine` — too vague, could mean anything physical
- `computer` — excludes cloud VPS conceptually (it's not "your computer")
- `box` — too informal
- `node` — implies distributed cluster membership
- `target` — implies deployment, not general access
- `remote` — local isn't remote

Usage reads well:

```
ww host              # list all
ww host local        # current machine
ww host workstation  # GPU box
ww host dmit         # cloud
ww host local workstation  # both
```

If you want to rename it, the main change is the Click command name + the help text. The internal class/function names can stay as-is or update for consistency. Want me to do the rename?
