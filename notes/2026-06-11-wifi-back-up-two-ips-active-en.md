---
audio: false
generated: true
image: false
lang: en
layout: post
title: WiFi Back Up, Two IPs Active
translated: false
type: note
---

**Question:** If WiFi was DOWN, why can I still reach the machine at 192.168.1.47?

**Answer:**

Because the WiFi came back up — the `state DOWN` in that log was just a snapshot at one moment. NetworkManager auto-reconnects, so now **both NICs are live simultaneously**, and the machine holds **two IPs at once**:

- `192.168.1.47` → WiFi (`wlp3s0`)
- `192.168.1.28` → Ethernet

Both accept inbound SSH. This is normal multi-homing — nothing exclusive about it.

Confirm on the xiaoxin box:

```bash
ip -br addr          # expect UP on both wlp3s0 and enp*, each with its IP
ip route             # look at 'default via ... metric N' lines
```

You'll likely see two default routes with different metrics, e.g.:

```
default via 192.168.1.1 dev enp3s0 metric 100    # ethernet wins (lower metric)
default via 192.168.1.1 dev wlp3s0 metric 600
```

That metric ordering explains the asymmetry you noticed:

- **Inbound**: you can connect to either IP — Linux answers on whichever interface the packet arrives, and replies keep the source IP you dialed (weak host model). So `.47` works fine from your Mac.
- **Outbound**: when the worker initiates the Gloo connection to the master at `.36`, the kernel picks the default route → ethernet → master sees the worker as `.28`.

So: same machine, two doors. You knock on `.47`; the training process walks out through `.28`.

For training stability, make it deterministic instead of metric-dependent:

```bash
# in run_dist_cpu_worker.sh
export GLOO_SOCKET_IFNAME=enp3s0     # exact name from `ip -br link`
# and on the master (.36)
export GLOO_SOCKET_IFNAME=<its ethernet ifname>
```

Otherwise a WiFi flap mid-run can shift routing and hang the allreduce. Wired-pinned on both ends = stable steps.
