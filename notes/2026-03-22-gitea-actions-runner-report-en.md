---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gitea Actions Runner Setup Report
translated: false
type: note
---

Here's the full rundown, Boss.

---

## Gitea Actions Runner — Setup Report

### Binary
- **Software:** `act_runner` v0.2.6 (official Gitea Actions runner)
- **Location:** `/usr/local/bin/act_runner`

### Registration
- **Instance:** `http://192.168.1.36:3000`
- **Name:** `local-runner`
- **UUID:** `68cf95f8-2e71-4610-87f2-6b7ad65f8273`
- **Runner ID:** 1 (repo-level runner for `lzwjava/blog-source`)
- **Status:** Declared successfully, listening for jobs

### Labels (what jobs this runner can pick up)

| Label | Runtime |
|---|---|
| `ubuntu-latest` | Docker: `node:16-bullseye` |
| `ubuntu-22.04` | Docker: `node:16-bullseye` |
| `ubuntu-20.04` | Docker: `node:16-bullseye` |
| `ubuntu-18.04` | Docker: `node:16-buster` |

### Runtime Dependencies
- **Docker:** v27.5.1 ✅
- **Systemd:** Enabled (`gitea-runner.service`) ✅
- **Survives reboot:** Yes

### Configuration
- **Config file:** `/home/lzw/.gitea-runner/config.yaml` (default)
- **Concurrency:** 1 job at a time
- **Job timeout:** 3 hours
- **Cache server:** Enabled (auto-detected port)
- **Container network:** Auto-created
- **Fetch interval:** Polls every 2s for new jobs

### File Locations

| File | Path |
|---|---|
| Config | `/home/lzw/.gitea-runner/config.yaml` |
| Registration | `/home/lzw/.gitea-runner/.runner` |
| Service unit | `/etc/systemd/system/gitea-runner.service` |

### Useful Commands
```bash
# Check status
sudo systemctl status gitea-runner

# Live logs
journalctl -u gitea-runner -f

# Restart after config change
sudo systemctl restart gitea-runner
```

### Things to Note
- This is a **repo-level runner** (scoped to `lzwjava/blog-source`), not org-wide
- Jobs run in Docker containers pulled from `node:16-bullseye` — first run will be slower while pulling the image
- Default config has placeholder env vars (`A_TEST_ENV_NAME_1/2`) — can clean those up if you want
- Capacity is 1 — if you need parallel jobs, bump `runner.capacity` in the config

Anything you want to tweak?
