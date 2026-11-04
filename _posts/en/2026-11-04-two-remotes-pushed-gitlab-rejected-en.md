---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two remotes pushed, GitLab rejected
translated: false
type: note
---

Done for the two remotes that pushed cleanly:

| Remote | Push status |
|--------|-------------|
| **origin (GitHub)** | ✅ `f5e6401b..852a5564` pushed |
| **gitea** | ✅ `65f99c8d..852a5564` pushed |
| **gitlab** | ❌ rejected (non-fast-forward) |

**Why GitLab failed:** GitLab's `main` is at commit `735c8c4 "Initial commit"` which is *unrelated* to your local history — it's a completely separate repository tree (local vs remote differ by ~48k files / 4.3M line deletions). This isn't a normal fast-forward; syncing would require a **force push** that overwrites GitLab's existing `main` and its "Initial commit" history.

I did **not** force-push because that would destroy the current GitLab-side history. How do you want to handle GitLab?

- **Force push** — `git push --force gitlab main` (overwrites GitLab's unrelated `main`), or
- **Skip GitLab** — leave it as-is (GitHub + gitea are already synced).

You just need to do.
