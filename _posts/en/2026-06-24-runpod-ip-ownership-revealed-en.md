---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod IP Ownership Revealed
translated: false
type: note
---

Now I have the full picture. Here's the deep analysis:

```
=== IP INVESTIGATION: 213.173.102.150 ===

GEO & OWNER
  IP:         213.173.102.150
  City:       Timișoara, Romania
  ASN:        AS202779 — EVOBITS Information Technology SRL
  Company:    evobitsit.com (Cluj-Napoca, Romania)
  Business:   Cloud VPS, Dedicated Servers, Colocation, Private Clouds
  Datacenter: 1.2MW + 3.5MW facilities in Romania (120 racks, 2N power)

NEARBY IPs (213.173.102.0/24 — all EVOBITS)
  .130  → EVOBITS | Timișoara
  .140  → EVOBITS | Timișoara
  .145  → EVOBITS | Timișoara
  .148  → EVOBITS | Timișoara
  .149  → EVOBITS | Timișoara
  .150  → EVOBITS | Timișoara  ← YOUR POD
  .151  → EVOBITS | Timișoara
  .152  → EVOBITS | Timișoara
  .155  → EVOBITS | Timișoara
  .160  → EVOBITS | Timișoara
  .170  → EVOBITS | Timișoara
  .200  → EVOBITS | Timișoara
  .240  → EVOBITS | Timișoara

BROADER EVOBITS RANGE
  213.173.96.0/20  → all EVOBITS, Timișoara
  213.173.112.0/20 → all EVOBITS, Cluj-Napoca

NMAP SCAN (213.173.102.150)
  22/tcp    open     ssh          ← direct SSH on standard port
  10000/tcp open     webmin?      ← management panel
  33880/tcp filtered (your RunPod-mapped port, currently down)

RUNPOD ANALYSIS
  RunPod has NO ASN (zero BGP records on bgp.tools)
  RunPod does NOT own any IP address space
  RunPod is a marketplace/platform, not an ISP
  Community Cloud pods expose the CONTRIBUTOR's real public IP
  RunPod docs confirm: "Public IP may change on Community Cloud
    if Pod migrates" — meaning it's the host's IP, not RunPod's

VERDICT
  213.173.102.150 is NOT a RunPod-assigned IP.
  It belongs to EVOBITS (Romanian hosting company).
  Someone at EVOBITS (or a customer of EVOBITS) is contributing
  their RTX 2000 Ada GPU to RunPod's Community Cloud marketplace.
  RunPod mapped port 33880 → 22 (SSH) on this machine for you.
  The machine itself is likely a VM or bare-metal server inside
  EVOBITS' Timișoara datacenter.
```

In short: RunPod gave you a pod ID and a proxy address, but the underlying IP is the contributor's own — a Romanian hosting company called EVOBITS with real datacenters. The contributor is renting out their GPU through RunPod's peer-to-peer marketplace. When the pod is active, RunPod maps port 33880 to the machine's SSH port 22. When the pod is paused/stopped, that mapping disappears (connection refused), but the machine itself might still be running (port 22 and 10000 are still open right now — someone else's server).
