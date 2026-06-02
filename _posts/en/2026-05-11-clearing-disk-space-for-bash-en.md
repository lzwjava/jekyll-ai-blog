---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clearing Disk Space for Bash
translated: false
type: note
---

Bash is hard-broken again — even `:` (the shell noop) returns exit 1. The 101 MB of free space we had got eaten by something almost instantly (log writes, journald, whatever). I can't run anything until we have headroom measured in **GB**, not MB.

A few MB isn't enough — Claude Code's session-env writes log and state files as it runs, and so does systemd/journald in the background. We need real breathing room.

Please run these yourself, in your own shell, and tell me the sizes you see:

```bash
# the obvious heavyweights
du -sh ~/.cache/huggingface ~/.cache/pip ~/.cache 2>/dev/null
du -sh ~/projects/zz/datasets/* 2>/dev/null
du -sh /var/log /var/lib/docker 2>/dev/null

# anything else large outside /home
sudo du -h -d2 -x / 2>/dev/null | sort -hr | head -20

# free space now
df -h /
```

The first few are usually the biggest wins:

- `~/.cache/huggingface` — old HF model/dataset downloads; safe to nuke if you don't need them
- `/var/lib/docker` — if Docker is installed, `docker system prune -a` often reclaims tens of GB
- `~/projects/zz/datasets/fineweb-edu` — ~69 GB already downloaded; if we're going to lower the target anyway, this could go (but you'd lose progress, so don't delete yet)
- `/var/log` and old journald — `sudo journalctl --vacuum-size=500M` is a quick clean

Paste the output and I'll point at the best target to clear.
