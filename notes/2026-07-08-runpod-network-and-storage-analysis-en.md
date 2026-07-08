---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Network and Storage Analysis
translated: false
type: note
---

## Analysis Summary

### 1. Where Was the Pod?

**38.80.152.249** is in **Rancho Cordova, California** (near Sacramento):

| Field | Value |
|-------|-------|
| City | **Rancho Cordova, California** |
| ISP | **Cogent Communications** (AS174) — a major transit provider |
| Data center | Likely a **RunPod Secure Cloud** facility in CA |
| Lat/Lng | 38.5891, -121.3027 |

RunPod routes traffic through Cogent to their data center, then the IP is a NAT on their load balancer — not directly the GPU machine.

### 2. How RunPod Networking Works

RunPod has a **layered architecture**:

```
You (SSH) → RunPod Load Balancer → Docker Container (your pod)
                    ↓
             Internal:
          NFS Network Volume
          Global Networking (pod-to-pod)
```

**SSH / TCP Access (what we used):**
- You connect to `38.80.152.249:30520` — this is the **RunPod load balancer IP**, not the actual GPU server
- Port `30520` is a **TCP tunnel** that maps to port 22 on the pod's container
- On restart, the **port changes** (was `30416` → `30520`), but the IP stays the same (for Secure Cloud)

**The pod itself runs in Docker:**
```
Host machine (NVIDIA H200)
  └── Docker container
       ├── /          → 20G overlay (ephemeral OS)
       ├── /workspace → NFS volume (persistent, 280G in our case)
       └── root user
```

That's why `/` was only 20G (ephemeral container disk) and `/workspace` was 280G (network volume).

**Network Volume (persistent storage):**
```
10.100.232.10:/runpodfs/networkvolumes/7tlpgx7y0n  280G  104G  176G  /workspace
```
- This is an **NFS mount** from RunPod's storage cluster
- Volume ID: `7tlpgx7y0n`
- Survives pod stop/start — data was there when you restarted
- Attachable across multiple pods in the same data center
- **Charged for storage even when pod is stopped**

**Three storage tiers:**
| Type | Location | Persists across | Lifetime |
|------|----------|------------------|----------|
| Container disk (`/`) | Local SSD on host | Nothing | Ephemeral |
| Volume disk (`/workspace`) | Local SSD on host | Stop/start | Until pod terminated |
| **Network volume** | NFS cluster | **Everything** | Until deleted |

You used a **network volume** (based on the NFS mount at 10.100.232.10) — that's why your data survived the stop/restart.

**Community Cloud vs Secure Cloud:**
| | Community Cloud | Secure Cloud (yours) |
|---|---|---|
| GPU availability | Shared, competitive | Guaranteed |
| IP stability | Changes on restart | **Stable IP** |
| Data center access | Anyone | Controlled |
| Network volumes | Yes | Yes |

Since you were on Secure Cloud, the IP `38.80.152.249` stayed the same, but the TCP port changed (`30416` → `30520`) because the Docker container got a new identity on restart.

**Global networking** (optional): private pod-to-pod network via `pod_id.runpod.internal` — useful if running multiple pods that need to talk to each other, but not relevant for a single pod.
