---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Jupyter Terminal Instead
translated: false
type: note
---

Port 31154 is **listening inside** the container (that's the SSH daemon we started). But the cloud proxy might not be forwarding traffic to it externally.

**To check if SSH is actually accessible from outside, run this inside the container:**

```bash
# 1. Check if SSH is listening on the right interface
cat /proc/net/tcp | grep "$(printf '%04X' 31154 | sed 's/\\(..\\)\\(..\\)/\2\1/')"

# 2. Check what external IP the container sees
curl -s ifconfig.me 2>/dev/null || echo "no external IP"

# 3. Test SSH locally (from inside the container to itself)
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@localhost -p 31154 "echo SSH_LOCAL_OK"
```

**To test from your Mac (outside):**

```bash
ssh -o ProxyCommand=none -v root@36.150.116.206 -p 31154 2>&1 | head -10
```

But based on my earlier test from my end, the **external port 31154 is still refused** — the cloud proxy hasn't remapped it after the crash.

**Simplest way forward**: just use the Jupyter terminal to run FLUX.1-dev. No need for SSH.
