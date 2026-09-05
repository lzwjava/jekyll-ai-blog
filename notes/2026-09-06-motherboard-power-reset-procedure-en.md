---
audio: false
generated: true
image: false
lang: en
layout: post
title: Motherboard Power Reset Procedure
translated: false
type: note
---

**Question:** When the motherboard shuts everything down, how do we fully restart it? Do we need to unplug the 24-pin connector, or switch off the PSU? Does the motherboard still hold power briefly even after shutdown?

---

**Answer:**

Great observation — you are **absolutely right** in your thinking. Here is the full explanation:

---

### ⚡ Why the Motherboard Still Has Power After Shutdown

Even when the system shuts down (whether by thermal protection or you press the power button), the motherboard is **NOT fully dead**. As long as the PSU is connected to the wall:

```
Wall outlet → PSU → Motherboard 24-pin
                         ↓
              +5VSB (Standby Voltage)
              always ON even when "off"
```

The **+5VSB (5V Standby)** line on the 24-pin connector is **always live** whenever the PSU is plugged into the wall — even with the PC switched off. This is what allows features like:
- Wake-on-LAN
- USB charging while PC is off
- Power button detection

---

### 🔄 So How Do You Properly Reset / Restart?

Here are the methods, from **least effective → most effective**:

| Method | Does it work? | Why |
|---|---|---|
| Press power button again | ❌ Usually NO | Motherboard still in protection state |
| Switch off PSU rear switch | ✅ YES — wait 10–15 sec | Cuts all power including +5VSB |
| Unplug PSU from wall | ✅ YES — wait 10–15 sec | Same as above, fully drains capacitors |
| Unplug 24-pin from motherboard | ✅ YES | Physically removes all power from board |
| Remove CMOS battery briefly | ✅ YES (full reset) | Clears all board state completely |

---

### ⏱️ Why Wait 10–15 Seconds?

You are also right that even after unplugging, the motherboard **holds residual power briefly** — because the board has **capacitors** that store a small charge. They drain within a few seconds. This is why you must:

```
1. Switch off PSU (or unplug from wall)
        ↓
2. WAIT 10–15 seconds
        ↓
3. Capacitors fully discharge
        ↓
4. Now board is truly at zero power
        ↓
5. Safe to reconnect and restart
```

---

### ✅ Best Practice for Your Situation

Since you are diagnosing a thermal shutdown problem, the **recommended full reset procedure** is:

1. **Switch off the PSU** using the rear switch (the **O** side)
2. Wait **15 seconds** for capacitors to drain
3. Fix the heatsink / thermal paste issue
4. Switch PSU back on (**I** side)
5. Press power button

If your Huntkey 280W PSU has **no rear switch**, then unplug it from the wall socket and wait 15 seconds instead.

---

### 💡 Summary

> Yes — you are correct. Simply pressing the power button after a thermal shutdown usually does nothing. You must fully cut power at the PSU switch or wall outlet, wait for capacitors to drain, then reconnect. The motherboard stays in a protected/latched state until all standby power is completely gone.

---

**References:**
- [ATX +5VSB Standby Power Explained — electronics.stackexchange.com](https://electronics.stackexchange.com/questions/40592/what-is-5vsb-in-atx-power-supply)
- [How to fully power cycle a PC — Tom's Hardware](https://forums.tomshardware.com/threads/how-to-fully-reset-motherboard-after-shutdown.3400000/)
