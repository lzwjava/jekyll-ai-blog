---
audio: false
generated: true
image: false
lang: en
layout: post
title: Delete RunPod Network Volume Guide
translated: false
type: note
---

Question: How do I delete a RunPod network volume when it says I need to remove it from all pods first — do I need to delete the pod?

Answer:

Yes — but "remove" doesn't always mean full deletion, and there's a common gotcha: **serverless endpoints also count as attachments**, not just pods.

**Steps:**

1. **Stop/terminate any Pod using the volume.** If a pod has the network volume mounted, you need to either:
   - Terminate the pod entirely, or
   - Edit the pod and detach the volume (if RunPod's UI allows swapping storage without termination — for GPU pods this is usually not possible in-place; you typically must terminate).

   In practice, on RunPod, network volumes are bound at pod creation time (you pick the volume in the datacenter-locked config), so there's **no live "detach" button** — you must terminate the pod.

2. **Check Serverless endpoints too.** This is the part people miss (see the community threads above — "no pod running" but still blocked). If any **Serverless endpoint** (not a pod) references the volume in its template/worker config, it'll block deletion the same way. Go to Serverless → check each endpoint's template for the volume, and delete/edit those endpoints.

3. **Then delete the volume**, either via UI or API:

```bash
curl --request DELETE \
  --url https://rest.runpod.io/v1/networkvolumes/{networkVolumeId} \
  --header 'Authorization: Bearer <API_KEY>'
```

**Quick checklist before retrying delete:**

- [ ] All pods using this volume are terminated (not just stopped — stopped pods still hold the volume reference)
- [ ] All serverless endpoints referencing this volume are deleted or reconfigured
- [ ] Wait ~30s after termination — RunPod's backend sometimes lags in releasing the lock

If you've confirmed both pods and serverless are clear and it's still blocked, it's a known RunPod backend bug (see the March 2025 thread) — worth pinging their Discord/support since the UI state can get stuck.

References:

- [Delete a network volume - Runpod API Docs](https://docs.runpod.io/api-reference/network-volumes/DELETE/networkvolumes/networkVolumeId)
- [Why can't I delete my storage - RunPod Community](https://www.answeroverflow.com/m/1351866718041145408)
