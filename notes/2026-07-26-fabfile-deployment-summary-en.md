---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fabfile Deployment Summary
translated: false
type: note
---

Done! Here's a summary of what was created and deployed:

### `fabfile.py` at project root

**Usage:**

```bash
# Deploy to remote (rsync + pip install)
fab -H root@36.150.116.206:31005 deploy

# Check deployed version and status
fab -H root@36.150.116.206:31005 status

# Run any command on remote
fab -H root@36.150.116.206:31005 shell -- cmd="ls -la /root/ahl"
```

**What it does:**
- **`deploy`** — Rsyncs the local source tree to `/root/ahl` on the remote, excluding `__pycache__`, `.git`, `*.png`, etc., then runs `pip install -e .` using `/opt/venv/bin/pip` (the remote's virtualenv)
- **`install`** — Alias for deploy
- **`status`** — Shows deployed version, pip package info, and remote file listing
- **`shell`** — Runs any command on the remote via SSH
