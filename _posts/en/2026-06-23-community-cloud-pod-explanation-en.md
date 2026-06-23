---
audio: false
generated: true
image: false
lang: en
layout: post
title: Community Cloud Pod Explanation
translated: false
type: note
---

Here's what I found:

IP: 213.173.102.150
Location: Timișoara, Romania
Owner: AS202779 — EVOBITS Information Technology SRL
Type: Hosting/cloud provider (9 year old BGP network, 192 peers)

This is NOT RunPod's own datacenter (Secure Cloud). This is almost certainly a RunPod Community Cloud pod — where someone in Romania is renting out their RTX 2000 Ada workstation through RunPod's peer-to-peer GPU marketplace. That's why:

1. The IP traces to a Romanian hosting company, not RunPod's infra
2. The GPU is an RTX 2000 Ada (professional workstation card, not typical datacenter hardware)
3. The SSH port was non-standard (33880)
4. The connection is now REFUSED — the pod was likely terminated or the host shut it down

RunPod Community Cloud works like this: individuals/orgs contribute their GPUs to RunPod's marketplace, RunPod handles provisioning and billing, and users get cheaper compute. The contributor's own ISP shows up as the IP, not RunPod's.

Current status: Connection refused. The pod is down. Either:
- You paused/stopped it in RunPod dashboard (as you said "I pause")
- It hit an idle timeout and auto-terminated
- The contributor powered off their machine

If you want it back, go to your RunPod dashboard and resume/recreate the pod. Community Cloud pods are ephemeral — the host can disconnect at any time. For more reliable workloads, use RunPod Secure Cloud (enterprise datacenters, higher uptime, slightly more expensive).
