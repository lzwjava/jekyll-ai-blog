---
audio: false
generated: true
image: false
lang: en
layout: post
title: Accessing RunPod Port 8080
translated: false
type: note
---

Server running on 8080. The 502 you're seeing is because RunPod doesn't expose ports directly via IP — you need the RunPod proxy URL.

RunPod proxy URL format is typically:

```
https://<pod-id>-8080.proxy.runpod.net
```

You can find it in your RunPod dashboard under the pod's "Connect" tab → HTTP ports. Look for the exposed port 8080 URL there.

Alternatively, access locally via SSH tunnel from your Mac:

```
ssh -p 28484 -i ~/.ssh/id_ed25519 -L 8080:localhost:8080 root@213.173.110.200 -N
```

Then open `http://localhost:8080/v1/models` in your browser. You'll also need to expose port 8080 in the RunPod pod settings (if it's not already set as an HTTP port).
