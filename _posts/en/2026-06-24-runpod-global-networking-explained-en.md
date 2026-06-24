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

**Question:** What does "Enable Global Networking" mean on RunPod, and what are the internal hostname and private IP address fields for?

**Answer:**

RunPod's **Global Networking** feature connects your pod to a **private overlay network** (like a VPN mesh) spanning all RunPod datacenters globally. Without it, your pod is isolated — only reachable via its public HTTP/TCP proxy ports.

## What it enables

When you turn on Global Networking, your pod gets:

- **Internal hostname** — a stable DNS name (e.g., `<pod-id>-<port>.proxy.runpod.net` or something like `<hostname>.runpod.internal`) that resolves to your pod from **other pods on the same RunPod network**, regardless of which datacenter they're in.
- **Private IP address** — a static private IP (typically in `10.x.x.x` range) assigned to your pod within the overlay network.

## Why it matters for your use case

| Use case | Why Global Networking helps |
|---|---|
| Multi-node training (DDP/NCCL) | Nodes find each other via stable hostname instead of ephemeral IPs |
| Multi-agent systems | Agent pods call each other directly without going through public internet |
| Inference + training split | Separate inference pod calls training pod internally with low latency |
| Ray / vLLM clusters | Head node and worker nodes communicate over private network |

## How it works under the hood

RunPod uses **WireGuard** or similar overlay networking to create a flat L3 network across pods. Your pod gets a virtual NIC with the private IP. DNS resolution of the internal hostname routes within this overlay — never hits the public internet.

## Practical implication

If you're running multi-GPU or multi-node jobs on RunPod (relevant to your MI300X-scale training work), enabling this is essentially required for NCCL `MASTER_ADDR` to work reliably between pods. You'd set:

```bash
export MASTER_ADDR=<internal-hostname>
export MASTER_PORT=29500
```

Without Global Networking, you'd have to punch through public TCP proxy ports, which adds latency and complexity.

**TL;DR:** It's RunPod's private inter-pod network. Enable it whenever pods need to talk to each other directly — multi-node training, distributed inference, agent meshes.
