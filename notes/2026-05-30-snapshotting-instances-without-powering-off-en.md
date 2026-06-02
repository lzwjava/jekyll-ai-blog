---
audio: false
generated: true
image: false
lang: en
layout: post
title: Snapshotting Instances Without Powering Off
translated: false
type: note
---

**Question:** For AMD Dev Cloud and DigitalOcean — can you create snapshots of a running instance without powering it off first?

**Answer:**

These two platforms have different behaviors:

## DigitalOcean

**No — you need to power off first for a consistent snapshot.**

DigitalOcean does support "live snapshots" (snapshot while running), but they explicitly warn that this can result in **inconsistent/corrupted filesystem state** — essentially a crash-consistent snapshot, not application-consistent. For anything stateful (databases, in-progress training runs with open files), powering off is the safe path.

Their docs recommend:

```
# Power off cleanly before snapshotting
doctl compute droplet-action power-off <droplet-id> --wait
doctl compute droplet-action snapshot <droplet-id> --snapshot-name "my-snapshot"
```

Live snapshots on DO are essentially "best effort" — fine for stateless machines, risky for active workloads.

## AMD Dev Cloud

The snapshot page at `devcloud.amd.com/images/snapshots` is specific to their environment. AMD Dev Cloud instances (especially MI300X nodes billed at ~$2/hr) are typically **ephemeral compute nodes** where:

- Snapshots/images are captured from a **stopped or idle instance state**
- The UI may let you initiate a snapshot on a running instance, but the underlying orchestration (likely OpenStack or a similar cloud substrate) typically quiesces or pauses the VM briefly

I'd check the actual UI behavior — if the "Create Snapshot" button is greyed out while running, that's your answer. If it's active, it's likely crash-consistent at best.

## Bottom Line

| Platform | Live Snapshot? | Safe for ML workloads? |
|---|---|---|
| DigitalOcean | Technically yes, but risky | Power off first |
| AMD Dev Cloud | UI-dependent, likely needs stop | Stop instance first |

**Practical advice for your use case:** Before snapshotting an AMD Dev Cloud instance mid-training-run, checkpoint your model weights explicitly (they should already be on disk), then stop the instance cleanly before snapshotting. Snapshots are for environment/dependency preservation — not checkpoint state.
