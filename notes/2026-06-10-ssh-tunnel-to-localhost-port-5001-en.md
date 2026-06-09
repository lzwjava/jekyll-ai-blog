---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Tunnel to Localhost Port 5001
translated: false
type: note
---

Port 5001 is free. Run this in your terminal (foreground, stays open until Ctrl+C):

```
ssh -L 5001:127.0.0.1:5001 amd-cloud -N
```

Then open http://localhost:5001 in your browser. Press `Ctrl+C` to kill the tunnel when done.
