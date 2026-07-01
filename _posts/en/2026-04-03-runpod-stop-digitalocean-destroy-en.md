---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Stop vs DigitalOcean Destroy
translated: false
type: note
---

Question: For RunPod, is stopping a pod better than destroying a Droplet on DigitalOcean? With DigitalOcean you have to make a snapshot before destroying, while with RunPod you can resume more easily?

Answer:

Yes, **RunPod Stop is significantly more convenient than DigitalOcean Destroy** for the use case of "pause and resume later." Here's a comprehensive breakdown:

---

## RunPod: Stop vs Terminate

RunPod has two distinct actions:

| Action | What happens |
| --- | --- |
| **Stop** | Pod is paused. GPU billing stops. Disk stays alive. Data in `/workspace` is preserved. |
| **Terminate** | Everything is destroyed. Container disk is wiped permanently. |

If you simply stop the pod, you can restart it later, and any data stored in `/workspace` will be preserved. RunPod charges an **Idle Disk Cost** while the pod is stopped.

That idle disk cost is exactly what you see in your screenshot: **$0.006/hr ($0.13/day)** — very cheap compared to keeping the GPU running.

Data stored in the `/workspace` directory survives pod stops and restarts, but is **deleted when the pod is terminated**. This is ideal for storing models, datasets, and checkpoints that you need to access across multiple sessions.

---

## DigitalOcean: Destroy Workflow

On DigitalOcean, destroying a Droplet is **permanent and irreversible**:

If you intend to destroy a Droplet and want the most up-to-date image, you must **power down the Droplet and take a snapshot immediately before destroying it.**

DigitalOcean snapshots are charged at **$0.06/GB per month**, and if you destroy the droplet and create a new one from a snapshot, there is a very strong possibility you will **lose your IP address.**

So with DigitalOcean the workflow is:

1. Power down Droplet
2. Manually take a snapshot (costs time + storage fees)
3. Destroy the Droplet
4. Later, create a **new** Droplet from the snapshot (new IP, new setup steps may be needed)

---

## Side-by-Side Comparison

| Feature | RunPod Stop | DigitalOcean Destroy + Snapshot |
| --- | --- | --- |
| **Data preserved automatically** | ✅ Yes (`/workspace`) | ❌ Must manually snapshot first |
| **Resume speed** | ✅ Fast (same pod restarts) | ❌ Slow (new Droplet from snapshot) |
| **IP / environment preserved** | ✅ Yes | ❌ Usually loses IP |
| **Extra manual steps needed** | ❌ None | ✅ Must create snapshot manually |
| **Idle cost** | ✅ Very low (~$0.006/hr disk only) | ✅ Zero (after destroy) + snapshot storage fee |
| **Risk of losing data** | Low (if you stop, not terminate) | Higher (if you forget to snapshot) |

---

## One Caveat to Watch Out For

If you stop your pod but leave behind a large container disk, you are still billed at **double the normal storage rate** for that disk until you delete it. Stopping a pod doesn't stop the storage meter.

So for long-term "cold storage," the best RunPod strategy is:

- Use a **Network Volume** for your important data
- **Terminate** the pod (not just stop) to avoid the idle disk double-billing
- Reattach the Network Volume to a new pod when you're ready

You can train a model on a pod today, save the checkpoints to a mounted volume, shut down the pod to save money, and next week attach that same volume to a new pod to resume training or run inference.

---

## Summary

For short-to-medium pauses (hours to a few days): **RunPod Stop wins clearly** — no snapshots, no lost IP, no manual steps, instant resume, tiny idle cost.

For very long-term pauses (weeks/months): Consider RunPod **Network Volume + Terminate** to avoid ongoing idle disk costs, which is still easier than the DigitalOcean destroy/snapshot workflow.

References:

- [RunPod Storage Types](https://docs.runpod.io/pods/storage/types)
- [RunPod Pricing Guide](https://flexprice.io/blog/runprod-pricing-guide-with-gpu-costs)
- [RunPod Network Volumes Blog](https://www.runpod.io/blog/network-volumes-on-runpod-secure-cloud)
- [DigitalOcean: Destroy Droplet & Keep Snapshot](https://docs.digitalocean.com/support/how-can-i-destroy-my-droplets-while-maintaining-my-backups/)
- [DigitalOcean Snapshot Costs](https://snapshooter.com/learn/digitalocean/backups)
