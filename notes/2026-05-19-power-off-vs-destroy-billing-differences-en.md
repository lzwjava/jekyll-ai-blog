---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Power Off vs. Destroy: Billing Differences"
translated: false
type: note
---

Question: What is the point of shutting off a GPU Droplet if it still costs money? Why not just keep it running?

Answer:

Honestly? **For billing purposes alone — there is no point.** You pay either way.

---

### The Only Real Reasons to Power Off (Not Destroy)

| Reason | Explanation |
|---|---|
| **Safety / Security** | A powered-off machine can't be attacked, hacked, or have runaway processes consuming resources |
| **Avoid accidental usage** | Prevents services or scripts from running unexpectedly and consuming GPU memory |
| **Thermal/process hygiene** | Stops all background processes cleanly before doing maintenance |
| **Before taking a Snapshot** | Some providers recommend powering off first to get a clean, consistent snapshot |

---

### So Should You Just Keep It Running?

**Yes, if you're actively using it within the same day or session** — there's zero benefit to powering it off and back on repeatedly. You're charged the same $1.99/hr regardless.

**No, if you're done for a while** — then you should **Destroy** it (optionally snapshot first), not just power off.

---

### The Practical Mental Model

Think of it like a **hotel room**:

- **Power off** = you're in the room sleeping. The room is still yours, you still pay.
- **Destroy** = you checked out. No more charges.
- **Snapshot → Destroy** = you packed your bags, stored them at the front desk, and checked out. Small storage fee, but no room charge.

---

### Bottom Line

> Powering off is mostly a **technical state**, not a **billing state**. If saving money is the goal, **Destroy** is the only option that matters.
