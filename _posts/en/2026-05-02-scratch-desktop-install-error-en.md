---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scratch Desktop Installation Error Analysis
translated: false
type: note
---

## Comprehensive Review: Scratch Desktop Installation

### The Request

The user's message was clear in intent but messy in form — a large Q&A block was pasted inline as context. I correctly extracted the actual task: SSH to `xiaoxin@192.168.1.47` and install Scratch Desktop.

---

### What Went Wrong

**1. No pre-flight checks**

Before installing anything, I should have run:

```bash
ssh xiaoxin@192.168.1.47 "
  flatpak --version
  flatpak remotes --user
  flatpak list | grep -i scratch
  df -h ~
"
```

This would have revealed: user has no flathub remote, no existing install, and available disk space — all in one round trip.

**2. Tried system-wide install as a non-root SSH user**

This was predictably going to fail. When you SSH as a regular user, `flatpak install` (system) requires root. I should have known to go `--user` immediately.

**3. Wasted bandwidth from the failed first attempt**

The first attempt downloaded 6 of 7 components before failing (~700MB+). Because it was a system install, nothing was cached for the user install. The second attempt re-downloaded everything. That's roughly **1.4GB** transferred for a ~1GB install.

**4. EOL runtime warning was under-flagged**

The install used `org.freedesktop.Platform 22.08`, which is explicitly end-of-life and no longer receiving security updates. I mentioned it passively. I should have said: *"Scratch Desktop on Flathub is pinned to an EOL runtime — this is a Flathub packaging issue, not something you can fix locally. Worth knowing if this is a shared/child-use machine."*

**5. No post-install verification**

I never confirmed the app actually works:

```bash
ssh xiaoxin@192.168.1.47 "flatpak run edu.mit.Scratch --version 2>&1 | head -5"
```

**6. XDG path warning left unresolved**

The install warned that `~/.local/share/flatpak/exports/share` isn't in `XDG_DATA_DIRS`, so the app won't appear in the application menu. I mentioned it but didn't fix it. The fix is one line in `~/.profile`:

```bash
export XDG_DATA_DIRS="$HOME/.local/share/flatpak/exports/share:$XDG_DATA_DIRS"
```

---

### What I Should Have Done

```bash
# Step 1: pre-flight
ssh xiaoxin@192.168.1.47 "flatpak list | grep -i scratch; flatpak remotes --user"

# Step 2: single correct command
ssh xiaoxin@192.168.1.47 "
  flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo &&
  flatpak install --user -y flathub edu.mit.Scratch
"

# Step 3: fix XDG path
ssh xiaoxin@192.168.1.47 "
  grep -q 'flatpak/exports' ~/.profile || echo 'export XDG_DATA_DIRS=\"\$HOME/.local/share/flatpak/exports/share:\$XDG_DATA_DIRS\"' >> ~/.profile
"

# Step 4: verify
ssh xiaoxin@192.168.1.47 "flatpak run edu.mit.Scratch --version 2>&1 | head -3"
```

---

### Summary

| Issue | Severity |
|---|---|
| No pre-flight checks | Medium |
| Wrong install mode first try | High (caused ~700MB wasted download) |
| EOL runtime not flagged clearly | Low |
| XDG path left broken | Medium |
| No post-install verification | Medium |

The task succeeded, but it took 3 attempts and roughly double the necessary bandwidth.
