---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Global Networking Explained
translated: false
type: note
---

**Question:** What does the RunPod "GPU Location / Enable Global Networking" section mean — specifically the Internal hostname, Private IP address, and the toggle?

**Answer:**

This is RunPod's pod networking configuration. Here's what each field means:

**GPU Location** — the physical datacenter region where your pod is running (e.g., US-TX, EU-RO). Relevant for latency and data residency.

---

**Enable Global Networking** — a toggle that, when enabled, gives your pod:

### Internal hostname

A stable DNS name within RunPod's private network, like:

```
<pod-id>-<port>.proxy.runpod.net
```

This lets other pods (or RunPod's infrastructure) reach your pod by name rather than by a dynamically assigned IP. Useful for multi-pod setups — e.g., an inference pod calling a preprocessing pod.

### Private IP address

A stable RFC-1918 IP (like `10.x.x.x`) assigned within RunPod's internal VXLAN/overlay network. Only reachable from within the RunPod network — not the public internet.

---

**Why it matters for your use case:**

| Scenario | Use Global Networking? |
| --- | --- |
| Single pod, SSH in, run training | No — not needed |
| Multi-pod distributed training (NCCL) | Yes — pods need to find each other |
| Inference pod + separate API gateway pod | Yes |
| vLLM server called by an agent pod | Yes |

If you're running a single MI300X pod for training (like your nanoGPT runs), you don't need this. If you're building a multi-node setup or agent infrastructure where pods talk to each other, enable it and use the internal hostname for service discovery instead of hardcoding IPs.

The private IP is ephemeral without Global Networking enabled — it may change on pod restart. With it enabled, the hostname stays stable across restarts.
