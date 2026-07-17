---
audio: false
generated: true
image: false
lang: en
layout: post
title: "SSH Config Cleanup: id_rsa to id_ed25519"
translated: false
type: note
---

The latest config is already correct, verified, and working — `runpod`/`runpod-gpu-*`/`runner` all resolve via `id_ed25519` and bypass the proxy. The one remaining cleanup is to drop `id_rsa` from the `Host *` default so it doesn’t get tried first.

**~/ssh/config line 18–24:**
```
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa     ← change to ~/.ssh/id_ed25519
    LogLevel VERBOSE
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

After that, usage:
- `ssh runner` → `root@213.173.99.50 -p 26246 -i ~/.ssh/id_ed25519`
- `ssh runpod` → `n4pqpw4h5fe3bb-64411f2b@ssh.runpod.io -i ~/.ssh/id_ed25519`
- `ssh runpod-gpu-<podId>` → same RunPod user with any lease IP built in

Timing summary: `runner` 4.8s (direct) vs 5.4s via DMIT proxy. `runpod` direct only. Functionally cleaner — no more manually matching host+user+port every time.
