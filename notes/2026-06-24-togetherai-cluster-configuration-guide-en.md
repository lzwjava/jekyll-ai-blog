---
audio: false
generated: true
image: false
lang: en
layout: post
title: Together.ai Cluster Configuration Guide
translated: false
type: note
---

**Question:** What is the Together.ai cluster configuration UI showing, and how does it work?

**Answer:**

This is Together.ai's **GPU Cluster provisioning UI** — their managed multi-node training infrastructure product. Let me break down every field:

---

## Region

Where the cluster is physically located. Affects latency to your data sources, egress costs, and sometimes GPU availability. Together.ai has US and EU regions.

---

## Shared Volume

A network-attached storage volume (likely NFS or similar) mounted across all nodes in the cluster. Critical for multi-node training — all nodes need to read the same dataset and checkpoint files. Without shared storage you'd have to sync manually across nodes.

---

## Driver Version

**570 (CUDA 12.8)** — the NVIDIA kernel driver version. CUDA 12.8 is current-gen. This matters because:

- Your `torch`, `flash-attention`, `triton` versions must be compatible with this CUDA version
- H100 SXM requires CUDA 11.8+ for full feature support; 12.x unlocks FP8 natively

---

## Enable Autoscaling

Scale node count up/down based on utilization. For training runs you almost always want **No** — you need a fixed topology for NCCL/RDMA collectives. Autoscaling is for inference serving, not training.

---

## Max GPUs

Only relevant if autoscaling is enabled — caps the upper bound.

---

## Use Custom OIDC

Bring your own identity provider (Okta, Azure AD, etc.) for auth into the cluster. Enterprise feature — ignore unless you're at a company with SSO requirements.

---

## Enable Traefik

[Traefik](https://traefik.io/) is a reverse proxy / ingress controller. Enabling this lets you expose HTTP endpoints from within the cluster — useful if you're running an inference server (vLLM, TGI) or a training dashboard (wandb agent, TensorBoard) that needs external access.

---

## GPU Type Table — The Core Choice

| Config | Bandwidth | Nodes | CPU Cores |
| --- | --- | --- | --- |
| 8x H100 SXM | 3.2 Tb/s Infiniband | 1 | 208 |
| 16x H100 SXM | 3.2 Tb/s Infiniband | 2 | 416 |
| ... | ... | ... | ... |
| 64x H100 SXM | 3.2 Tb/s Infiniband | 8 | 1664 |

Key things to understand:

**H100 SXM vs PCIe**: SXM form factor uses NVLink for intra-node GPU-GPU bandwidth (~900 GB/s bidirectional per H100). PCIe H100s are cheaper but NVLink bandwidth drops to PCIe speeds (~64 GB/s). For large model training, SXM is non-negotiable.

**3.2 Tb/s Infiniband**: This is HDR/NDR Infiniband for inter-node communication. At 8 nodes × 8 GPUs, all-reduce collective bandwidth is the bottleneck — 3.2 Tb/s is the rail that NCCL uses for gradient synchronization via `nccl_p2p` or `nccl_net`.

**208 CPU cores per node**: ~26 cores per GPU. Enough for DataLoader workers without CPU bottlenecking your GPU pipeline.

---

## How to Think About Cluster Size for Training

For a model like GPT-2 760M (what you've trained), even 1 node (8x H100) is massive overkill — you'd finish in minutes.

For serious work:

| Model Size | Recommended Config |
| --- | --- |
| 7B (LLaMA-scale) | 8x H100 (1 node), bf16 + Flash Attn |
| 70B | 16–32x H100, tensor parallel + pipeline parallel |
| 405B (LLaMA 3.1) | 64x H100+, FSDP + pipeline parallel |
| DeepSeek v3 671B MoE | 256+ H100s (what they used) |

---

## Cost Intuition

Together.ai H100 SXM pricing is roughly **$2–2.50/GPU/hour** depending on commitment. So:

- 8x H100 ≈ ~$16–20/hr
- 64x H100 ≈ ~$128–160/hr

Compare to your AMD MI300X at ~$2/hr total — vastly different scale and price point. Together.ai is for production training runs, not experimentation.

---

## TL;DR

This UI provisions a **bare-metal multi-node H100 cluster** with shared storage and Infiniband interconnect. You'd use it to run distributed training with frameworks like PyTorch FSDP, DeepSpeed, or Megatron-LM across 8–64 GPUs. The key axis is: how many GPUs do you need for your model to fit in memory and train in a reasonable wall-clock time?
