---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Monitoring Loop Fix
translated: false
type: note
---

Here's the full post-mortem:

---

## 🔍 Root Cause — What Happened

### The Chain of Events

1. **Uptime-Kuma** (your uptime monitor) was polling `GET /apps/dashboard/` on Nextcloud every ~6 minutes
2. This triggered Nextcloud's Dashboard app to load → which calls `PresetManager::refreshPresetApps()`
3. `PresetManager` iterates through **every installed app** and all their config entries, cloning config objects and rebuilding defaults for each of 10+ "lexicon presets"
4. Somewhere in this chain (possibly a third-party app or a lexicon config bug in Nextcloud 33.0.0) it hit an **infinite loop** — every request ran for 3600+ seconds before PHP's `max_execution_time` killed it
5. Each time Uptime-Kuma polled, a **new Apache worker** picked up the request and joined the loop
6. Over ~1.5 hours, **9 Apache workers** all saturated at 55-65% CPU each → load hit **11** → fan at full blast

### Why it wasn't obvious

- The parent Apache process (PID 4561) showed 0% CPU — it just managed workers
- All the hot processes were inside the **Nextcloud container** (docker namespace)
- `top` on the host saw them, but they appeared as containerd-shim processes, not named Apache

---

## ✅ The Fix — What We Did

### 1. Emergency — Stop the bleeding
```
docker restart nextcloud-app-1
```
Cleared all 9 stuck Apache workers immediately. Load dropped from 11 → 3.68 in seconds, fan quieted.

### 2. Root cause — Uptime-Kuma polling the wrong URL
- Changed monitor from `http://192.168.1.36:8080/apps/dashboard/` → `http://192.168.1.36:8080/status.php`
- `/status.php` is Nextcloud's dedicated health endpoint — returns `{"installed":true,"maintenance":false}` instantly, no app loading, no PHP heavy lifting

### 3. Patch the wound — Upgrade Nextcloud 33.0.0 → 33.0.2
- Downloaded new Nextcloud tarball
- Used `rsync` to overlay new source files onto the volume (preserving `config/`, `data/`, `custom_apps/`, `themes/`)
- Ran `php occ upgrade` — migrated DB schema, updated 13 apps
- Backed up DB first with `pg_dump`

---

## 🛡️ How to Prevent This

### For Nextcloud specifically:

| Do | Don't |
|---|---|
| Use `/status.php` for health checks | Poll `/apps/dashboard/` or any UI route |
| Set Uptime-Kuma interval ≥ 60s for PHP apps | Rapid polling of PHP apps |
| Monitor container CPU individually | Only look at host `load average` |

### General fan/noise prevention:
1. **Set up alerting on container CPU** — run this cron to alert before it gets bad:
{% raw %}
   ```
   docker stats --no-stream --format "{{.Name}}: {{.CPUPerc}}" | awk -F: '$2>80 {print $1" high CPU"}'
   ```
{% endraw %}
2. **Rotate logs** — prevent log files in containers from filling disk and causing swap pressure
3. **Restart containers periodically** — many PHP apps (Nextcloud, LibreChat) benefit from occasional restarts to clear memory leaks

---

## 🔧 Quick Diagnostic Commands

{% raw %}
```bash
# Find what's hottest
docker stats --no-stream

# See all processes inside a container
docker top <container>

# Watch container CPU in real time
watch -n2 'docker stats --no-stream --format "{{.Name}} {{.CPUPerc}}"'

# Nextcloud health
curl -s http://localhost:8080/status.php

# Full system load
uptime && top -b -n1 | head -8
```
{% endraw %}

Any container at sustained >50% CPU for more than a few minutes = investigate immediately.