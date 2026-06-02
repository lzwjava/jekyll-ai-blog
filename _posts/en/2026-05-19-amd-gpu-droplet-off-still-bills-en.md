---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AMD GPU Droplet: Off Still Bills"
translated: false
type: note
---

Question: If my AMD Developer Cloud GPU Droplet is shut down (powered off), does it still cost money?

Answer:

**Yes — powering off does NOT stop billing.**

Even when the droplet is powered off, you are still billed. To stop charges completely, you must **Destroy** the droplet from the dashboard, not just power it off.

---

### Why This Happens

This is standard cloud provider behavior (AMD Developer Cloud runs on DigitalOcean infrastructure). When a droplet is merely "powered off" or "turned off," the underlying resources — the MI300X GPU, storage, and reserved IP — are still allocated to you. You're paying for **resource reservation**, not just active compute time.

---

### What You Should Do

| Action | Still Billed? |
|---|---|
| Power Off / Shut Down | ✅ Yes, still billed |
| **Destroy Droplet** | ❌ No more charges |
| Take a Snapshot first, then Destroy | ❌ No compute charge (tiny storage fee only) |

---

### Recommendation

- If you're **done for good** → **Destroy** the droplet from the dashboard immediately.
- If you want to **resume later** → Take a **Snapshot** first, then Destroy. You can restore from the snapshot when needed.
- At **$1.99/hr**, leaving a powered-off droplet running overnight costs ~**$47/day** unnecessarily.

Go to your [AMD Developer Cloud dashboard](https://devcloud.amd.com/gpus) → select the droplet → choose **Destroy** to fully stop all charges.
