---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Fan Twitch Stop: Motherboard Protection"
translated: false
type: note
---

**Question:** The fan twitches briefly then stops after plugging in ATX 12V — what does this mean and what is the cause?

---**Answer:**

**Fan twitches briefly then stops = classic symptom of the motherboard detecting a fault and shutting itself down immediately to protect components.**

---

**What is actually happening:**

```
Press power button
       ↓
PSU sends power → fan twitches (brief power surge)
       ↓
Motherboard tries to POST
       ↓
Detects something WRONG
       ↓
Emergency shutdown → fan stops
```

The board is **not broken** — it is **protecting itself.**

---

**Most common causes — check in this order:**

**1. 🔴 RAM not seated properly (most common)**

- Remove RAM stick completely
- Clean gold contacts with eraser
- Push back in firmly until both clips click
- Try one stick at a time

**2. 🔴 Motherboard standoff short circuit**

- A brass standoff touching the back of the board where it shouldn't
- Extra standoff in wrong hole = short circuit = instant shutdown

**3. 🔴 CPU not seated correctly**

- Open CPU socket cover
- Check no bent pins
- Reseat CPU carefully

**4. 🔴 Wrong half of 4+4 pin inserted**

- Make sure correct keyed half is inserted into ATX12V socket

**5. 🟡 PSU weak or failing**

- 12V rail collapses under load → board shuts down

---

**Quick test — strip down to bare minimum:**

Disconnect everything except:

```
✅ 24-pin power
✅ ATX 12V (4-pin)
✅ CPU + CPU fan
✅ 1 stick of RAM only
❌ Remove GPU
❌ Remove all SATA drives
❌ Remove USB front panel cables
```

Then press power. Does it still twitch and stop?

- **Still twitches** → likely RAM or CPU issue
- **Boots now** → one of the removed components was causing the short

---

**References:**

- [Tom's Hardware – CPU fan spins half second then stops](https://forums.tomshardware.com/threads/hit-power-buton-cpu-fan-spins-for-half-a-second-then-stops-spin-and-stop-forever-no-booting.3034486/)
- [AnandTech – Fan starts and stops continuously diagnosis](https://forums.anandtech.com/threads/motherboard-dead-cpu-fan-starts-and-stops-continuously.2564774/post-39810021)
