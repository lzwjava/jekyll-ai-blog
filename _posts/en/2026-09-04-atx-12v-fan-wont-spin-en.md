---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX 12V Fan Won't Spin
translated: false
type: note
---

**Question:** Why does plugging in the ATX 12V connector cause the fan to not run — is it a CPU issue or something else?

---**Answer:**

This is actually a **very important diagnostic situation**. Let me break it down clearly:

---

**First — understand what "fan not running" means here:**

There are **two very different scenarios:**

---

**Scenario A — Fan doesn't spin when you ONLY plug in ATX12V (without pressing power button)**

```
This is COMPLETELY NORMAL ✅
```
- The fan will NOT spin just by plugging in the ATX12V cable
- The fan only runs **after you press the power button** and the system boots
- ATX12V alone does not start anything — it just **stands by waiting**

---

**Scenario B — Fan doesn't spin even AFTER pressing power button**

This is a real problem. Possible causes ranked by likelihood:

| # | Cause | How to check |
|---|---|---|
| 1 | **Short circuit somewhere** | Motherboard detects fault → shuts down immediately to protect itself |
| 2 | **CPU not seated properly** | Board refuses to boot without a working CPU |
| 3 | **Fan not plugged into CPU_FAN header** | Must go into `CPU_FAN` not `CHA_FAN` |
| 4 | **Wrong half of 4+4 pin inserted** | Keyed wrong → no power delivery |
| 5 | **Dead CPU** | Rare but possible |
| 6 | **Faulty PSU** | Not delivering stable 12V |

---

**Quick diagnosis steps:**

1. **Unplug ATX12V** → press power → do fans spin now?
   - Yes → problem is **short circuit on the 12V line or CPU/VRM issue**
   - No → problem is **elsewhere (24-pin, PSU, power button)**

2. **Check fan is plugged into correct header** on H81M-K:
   - CPU cooler fan → must go into **`CPU_FAN`** (4-pin near CPU socket)
   - NOT into `CHA_FAN`

3. **Check ATX12V is fully clicked in** — you should hear a click when seated properly

---

**Most likely answer for your situation:**

When the ATX 12V connector is plugged in and the system won't start, there are security fixtures on the motherboard that stop the computer from working if something is wrong — usually a short circuit or memory not correctly placed. So the board is likely **protecting itself** from something.

---

**Can you tell me more?**
- Does the fan twitch briefly then stop?
- Or does nothing happen at all when you press power?

That will narrow it down further.

---

**References:**
- [Tom's Hardware – ATX 12V connector fan issue diagnosis](https://forums.tomshardware.com/threads/atx-12v-connector.1664339/)
- [Case Fan Not Spinning – Box.co.uk](https://box.co.uk/blog/case-fan-not-spinning-fix)
