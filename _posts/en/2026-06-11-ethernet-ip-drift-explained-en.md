---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet IP Drift Explained
translated: false
type: note
---

**Question:** Why does ethernet show 192.168.1.28 when my two machines are 192.168.1.36 and 192.168.1.47, and why does nanochat distributed training connect via that IP?

**Answer:**

Your `xiaoxin` machine has **two network interfaces**, and each gets its **own DHCP lease** because each NIC has a different MAC address:

- WiFi (`wlp3s0`) → was `192.168.1.47` (the IP you remember)
- Ethernet (`enp*`) → `192.168.1.28` (a separate lease from your router)

So `.47` and `.28` are the **same physical machine**. The log shows `wlp3s0` is `state DOWN` — WiFi dropped, so the only live path to that box is now ethernet at `.28`. That's why the agent re-pointed SSH (and got a host-key mismatch — same host, new IP, hence the `ssh-keygen -R`).

Why training "listens" on it: torch.distributed with Gloo does rendezvous via `MASTER_ADDR:MASTER_PORT`. The master at `.36` listens; the worker dials out. The worker's outbound source IP is whatever interface the kernel routing table picks for reaching `.36` — now the ethernet NIC, so the master sees connections from `.28`. Gloo also binds data-plane sockets per interface; if `GLOO_SOCKET_IFNAME` isn't set, it picks the interface of the default route, which changed when WiFi died.

Verify it's the same box:

```bash
ssh xiaoxin@192.168.1.28 "hostname; ip -br addr; ip route get 192.168.1.36"
```

To stop IPs from drifting:

```bash
# 1. Pin the interface Gloo uses (in your run scripts)
export GLOO_SOCKET_IFNAME=enp3s0   # worker's ethernet name from `ip -br link`
export MASTER_ADDR=192.168.1.36

# 2. Better: DHCP reservation in your router for the ethernet MAC,
#    so .28 (or whatever you choose) is stable across reboots.
```

Side benefit: ethernet is the right link for distributed CPU training anyway — Gloo allreduce over WiFi adds latency/jitter that stalls steps. Keep both nodes on wired and pin `GLOO_SOCKET_IFNAME` on both ends.
