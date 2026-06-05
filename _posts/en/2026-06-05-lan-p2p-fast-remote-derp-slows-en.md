---
audio: false
generated: true
image: false
lang: en
layout: post
title: LAN P2P Fast, Remote DERP Slows
translated: false
type: note
---

Question: Why is Tailscale fast when my laptop and the target server are on the same LAN, but the delay is around 500ms when my laptop is outside the LAN?

Answer:

Yes, your observation is correct, and here's why:

1. **Same LAN (Local Network) Scenario**

   * When your laptop and the target server are on the same LAN, Tailscale can often use **direct peer-to-peer (P2P) connections**.
   * Tailscale tries to establish the connection using **LAN routes or NAT traversal** (like UDP hole punching).
   * Since the traffic stays within the local network, latency is minimal—usually just a few milliseconds.

2. **Outside the LAN (Remote Access) Scenario**

   * When your laptop is outside the LAN (e.g., on a home or public network), Tailscale may **not be able to establish a direct P2P connection** due to NATs, firewalls, or symmetric NAT setups.
   * In such cases, traffic is routed via **Tailscale’s DERP (Detour Encrypted Relay Protocol) servers**, which act as relay nodes.
   * These DERP servers can be geographically distant, so packets travel farther, adding **hundreds of milliseconds of latency**, which explains your ~500ms delay.

3. **Other Factors Affecting Latency**

   * Internet connection speed and routing between your laptop and the DERP node.
   * Congestion or packet loss on the public network.
   * VPN encryption overhead is minimal but nonzero.

**Summary:**

* LAN: direct P2P → fast, low latency (~1–10ms).
* Remote: relay via DERP → higher latency (~500ms in your case).

You can check if your Tailscale connection is direct or relayed using:

```bash
tailscale status --json
```

Look for `"via":"derp"` (relayed) or `"via":"direct"` (P2P).

This explains why your speed drops when outside the LAN.

References:

* [Tailscale: How it Works](https://tailscale.com/kb/1017/how-it-works/)
* [Tailscale DERP Explained](https://tailscale.com/blog/derp/)
