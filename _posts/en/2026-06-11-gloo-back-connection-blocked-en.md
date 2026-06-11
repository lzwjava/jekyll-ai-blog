---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gloo back connection blocked
translated: false
type: note
---

All clean now. Here's what happened:

The Gloo error is clear:
```
failed to connect ... local=[192.168.1.36]:20614, remote=[192.168.1.28]:56711, error=Connection timed out
```

The TCPStore rendezvous on port 29500 works fine (worker→master). But for the actual Gloo data transport, the master needs to connect BACK to the worker on an ephemeral port — and that's blocked. The worker (192.168.1.28 / xiaoxin) has a firewall blocking incoming connections on high ports, and you don't have sudo to open it.

Three options:

1. **Open firewall on the worker** — need sudo or physical access to run `sudo ufw allow from 192.168.1.36` or `sudo iptables -I INPUT -s 192.168.1.36 -j ACCEPT`

2. **Single-node multi-process** — run both ranks on 1.36 (has 62GB RAM, plenty for 2 CPU workers of d8):
   ```
   torchrun --nnodes=1 --nproc_per_node=2 --master_port=29500 ...
   ```

3. **Use `GLOO_SOCKET_IFNAME` + explicit port range** — set `GLOO_PORT_RANGE` on the worker to a known range, then open just those ports (still needs sudo)

Option 2 is the fastest path — want me to set that up? The 1.36 machine has 62GB RAM so two d8 workers (~80M params each) should fit fine. It won't be as fast as true 2-node but it'll actually run.
