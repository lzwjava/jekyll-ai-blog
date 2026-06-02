---
audio: false
generated: true
image: false
lang: en
layout: post
title: System Status and Optimization Plan
translated: false
type: note
---

Here's your system status and optimization plan:

---

## System Health

| Metric | Value |
|---|---|
| **RAM** | 16 GB (Apple Silicon) |
| **Active** | 7.5 GB / 16 GB — **47% used** |
| **Swap** | 218 MB used — low, healthy |
| **CPU** | Mostly idle (< 5% outside bursts) |
| **User processes** | **476** — quite high |
| **Free disk** | 54 GB |

---

## Top RAM Consumers

| App | RAM | Notes |
|---|---|---|
| **Safari WebContent (x5)** | **~3.0 GB** | Each tab = dedicated WebKit process. TabsKiller limits this. |
| **Safari** (main) | 315 MB | |
| **WeChat + WeChatAppEx** | **513 MB** | Heavy for a chat app |
| **Python (x2)** | 292 MB | One at 11% CPU — check what it's running |
| **Zed** | 143 MB | |
| **WindowServer** | 110 MB | macOS compositor |
| **GitHub Desktop** | 109 MB | |
| **Finder** | 65 MB | |
| **Ghostty** | 93 MB | |
| **mihomo** (proxy) | 36 MB | |

---

## Recommendations (sorted by impact)

### 1. TabsKiller already helping — verify setting

You said it's keeping 10 tabs. Each closed tab = one ~300-800 MB WebContent process freed. This is your biggest lever.

### 2. Release Safari WebContent memory

These 5 processes eating **3 GB** are your biggest RAM hog. Open the TabsKiller popup and confirm `maxTabs` is set where you want it. Also consider:

- Safari → Settings → Tabs → set "When closing a tab" → "Close automatically"
- Safari → Develop → Empty Caches (if Develop menu is on)

### 3. WeChat cleanup

WeChat + WeChatAppEx = **513 MB**. If you don't use mini-programs (WeChatAppEx), you can reduce this:

- WeChat → Settings → General → uncheck "Keep WeChat in background when closing window" if you don't need it
- Or quit it entirely when not chatting

### 4. Python processes

Two Python 3.11 processes using **292 MB**, one at **11% CPU**. Check what's running:

```bash
# Find what started them
ps aux | grep -m2 python
```

If it's an idle Jupyter kernel or a stalled script, kill it.

### 5. mihomo proxy

Running at only 36 MB / 0.9% CPU — fine, no action needed.

### 6. General cleanup (quick wins)

```bash
# Clear system caches (safe)
sudo purge

# Brew cleanup
brew cleanup -s

# Clear user logs
rm -rf ~/Library/Caches/* 2>/dev/null

# Check launch agents (services starting at login)
brew services list
```

### 7. Disk — 54 GB free isn't critical but worth watching

```bash
# Find big files
du -sh ~/Library/Caches ~/Downloads ~/.Trash 2>/dev/null
```

---

**Bottom line:** Your biggest wins are (1) TabsKiller keeping tabs ≤ 10 (each tab avoided = ~500 MB saved), and (2) closing WeChat when not in use saves ~500 MB. Together that's ~1.5 GB freed up, which keeps you well within 16 GB without needing swap.
