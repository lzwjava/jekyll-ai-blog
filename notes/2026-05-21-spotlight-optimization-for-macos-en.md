---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spotlight Optimization for macOS
translated: false
type: note
---

Done. Here's what happened and what to expect:

---

**What was done**

| Action | Effect |
| --- | --- |
| `touch ~/Projects/.metadata_never_index` | Spotlight will never crawl `~/Projects/` — that's your `node_modules`, dev repos, etc. |
| `touch ~/Library/Caches/.metadata_never_index` | Won't index cache files |
| `touch ~/Downloads/.metadata_never_index` | Won't index Downloads |
| `touch ~/Library/Application\ Support/.metadata_never_index` | Won't index app data |
| `sudo mdutil -E /` | Erased the existing index — forces clean rebuild |
| `pkill -9 mdworker mds` | Killed the CPU storm immediately |

**What you'll see**

- The ~250% CPU spike from mdworker will be gone in ~30 seconds
- Spotlight will rebuild its index but **only** for system files, Applications, your Documents, Desktop, etc. — skipping the 50GB+ of garbage it was crawling before
- The rebuild will finish in 1-2 minutes instead of 15+
- After today, **every reboot** will have a near-instant Spotlight rebuild instead of a 15-minute CPU hammering

**What still works**

- `Cmd+Space` search still works
- You can still search Applications, System Settings, Documents, etc.
- Anything inside `~/Projects/`, `~/Downloads/`, `~/Library/Caches/`, `~/Library/Application Support/` just won't show up in search results — which is probably what you want

**To undo** (if you ever want search back in those folders):

```
rm ~/Projects/.metadata_never_index ~/Library/Caches/.metadata_never_index ~/Downloads/.metadata_never_index ~/Library/Application\ Support/.metadata_never_index
sudo mdutil -E /
```
