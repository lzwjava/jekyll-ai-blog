---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Tunnel for MLflow Access
translated: false
type: note
---

Done. SSH tunnel is live:

```
http://localhost:5001
```

This is now showing the **remote** MLflow runs from amd-cloud (the MI300X training data), not the local copy. The tunnel command was:

```
ssh -L 5001:127.0.0.1:5001 amd-cloud -N -f
```

- `-L 5001:127.0.0.1:5001` — forward local:5001 to remote:5001
- `-N` — no remote command, just tunnel
- `-f` — background after auth

To kill the tunnel later: `pkill -f "ssh -L 5001"`
