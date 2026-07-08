---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Network Volume Resize Tips
translated: false
type: note
---

Question: In RunPod's "Edit network volume" dialog, I'm seeing an existing 200 GB volume being expanded by +100 GB to a total of 300 GB, billed at $0.14/GB/month ($42/mo total, up from $28/mo). What should I know about this case?

Answer:

The $0.14/GB/month rate confirms you're on RunPod's **high-performance network volume** tier, not the standard tier. For reference:

| Tier | Rate (first 1TB) | Notes |
| --- | --- | --- |
| Standard network volume | $0.05–$0.07/GB/mo | Ceph-backed, available broadly |
| **High-performance network volume** | **$0.14/GB/mo** | NVMe-backed, currently limited to Montreal data centers |

Your math checks out: 300 GB × $0.14 = $42/mo, up from 200 GB × $0.14 = $28/mo — a $14/mo delta for the +100 GB.

Things that matter operationally for this resize:

**1. Resize is grow-only.** RunPod network volumes can be expanded but not shrunk in-place. If you overprovision, the only way back down is to create a new smaller volume and migrate data (rsync/rclone), then delete the old one. Don't pad this number "just in case" — it's a one-way ratchet.

**2. Detach before resize.** Network volumes generally need to not be actively mounted to a running pod during a resize operation — check that your pod using this volume is stopped, or the resize call in the dashboard/API may reject or queue.

**3. Billing is hourly, not per-second**, unlike compute: storage is billed per-second for container and volume disks, and hourly for network volumes. So once you commit to 300 GB, you're paying for the full next hour-block regardless of when in the hour you resized.

**4. Stopped-pod trap doesn't apply here** — the 2x-when-stopped penalty is for **Container/Volume Disks** ($0.10 → $0.20/GB), not Network Volumes. Network volume rate stays flat whether attached, detached, or the pod is stopped — that's the whole point of network volumes vs. local disk.

**5. Given your workload (MI300X training runs, checkpoint-heavy MoE work)** — if this 300 GB is holding DeepSeek-v4 MoE checkpoints or nanochat intermediate artifacts, the high-perf tier's NVMe backing is the right call for sustained read/write during training. If it's just cold storage for datasets between runs, you're paying 2x for throughput you don't need — a standard network volume in a non-Montreal region at $0.07/GB would be $21/mo for the same 300 GB.

Quick CLI check to confirm which tier you're actually paying for, via the RunPod API:

```bash
curl -s https://api.runpod.io/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <RUNPOD_API_KEY>" \
  -d '{"query": "query { myself { networkVolumes { id name size dataCenterId } } }"}' \
  | python3 -m json.tool
```

That'll surface `dataCenterId` — if it's not a Montreal-region ID and you're still being charged $0.14, worth a support ticket since that tier is supposed to be geo-gated.

References:

- [Pricing - Runpod Documentation](https://docs.runpod.io/pods/pricing)
- [Understanding Runpod Pricing: A Clear Guide to Costs and Options | Hivenet](https://compute.hivenet.com/post/runpod-pricing-complete-guide-to-gpu-cloud-costs)
- [GPU Cloud Pricing | Runpod](https://www.runpod.io/pricing)
