---
audio: false
generated: true
image: false
lang: en
layout: post
title: Idempotent Git Pull Updates
translated: false
type: note
---

Yes, exactly. Each repo is an independent `git pull` — there's no shared state or transaction. If you cancel at repo 30 of 60:

- Repos 1-30: already pulled, done
- Repos 31-60: untouched, still at old state

Re-running `ww projects update` just pulls all 60 again — the already-updated ones will say "Already up to date" in ~1 second each, and the remaining 30 get their actual updates. `git pull` is idempotent, so re-running is always safe.

No checkpoint/resume logic needed — that's the beauty of it.