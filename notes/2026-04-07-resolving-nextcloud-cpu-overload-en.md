---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving Nextcloud CPU Overload Issue
translated: false
type: note
---

Load dropped from **11 → 9** and CPU is 99% idle. Fan should quiet down in a minute.

Now let me check what's broken in that PHP file so it doesn't immediately start looping again:Restart done. Load already dropping. Let me check what's happening with the Nextcloud dashboard + PresetManager loop:Load went from **11 → 3.68** in under 2 minutes. Apache workers are all idle now. Fan should be quiet.

The root problem is **Uptime-Kuma polling `/apps/dashboard/`** — Nextcloud 33's dashboard loads a `PresetManager` that iterates through all apps and their config entries, and something in that chain causes an infinite loop (or extremely slow execution). Every poll triggers it, burning CPU.

Two things to fix:

1. **Change Uptime-Kuma's Nextcloud monitor** from `/apps/dashboard/` → `/status.php` (the proper Nextcloud health endpoint, returns JSON with `{"installed":true}`)
2. **Nextcloud update** — you're on 33.0.0, check if 33.0.1+ has a fix

Want me to check if there's a newer Nextcloud version available, and help you update the Uptime-Kuma monitor URL?
