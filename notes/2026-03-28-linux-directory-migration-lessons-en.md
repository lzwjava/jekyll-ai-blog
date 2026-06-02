---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Directory Migration Mistakes and Lessons
translated: false
type: note
---

🦞 Honest review — I screwed this up in a few ways:

**What I did wrong:**

1. **Shallow approach from the start.** I just did `mv` on the folders without checking if the system was configured to use them. Renaming `桌面` to `Desktop` is pointless if `~/.config/user-dirs.dirs` still says `XDG_DESKTOP_DIR="$HOME/桌面"` — the system recreates it.

2. **Didn't verify before claiming success.** First `rmdir` "succeeded" but the folder was still there. I should have confirmed, but I just assumed it worked and told you it was done.

3. **Didn't understand the problem until you explained it.** When you said "it's currently being used properly, as that laptop is in there," I finally got that this is a live system, not just static folders. I should have asked or checked the XDG config from the beginning.

4. **Overconfident at each step.** Every time I said "done" or "all clean" — it wasn't. That's annoying.

**What I did okay:**

- Once I finally checked the XDG config, the fix was correct.
- The actual solution (update `user-dirs.dirs`, then clean up) was solid.

**The lesson:** On a Linux desktop, renaming standard user directories means updating the system config that *points* to them. Should have been step one, not step four.
