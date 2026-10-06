---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 Power Spike Trips PSU
translated: false
type: note
---

Good question — and I have a strong hypothesis. The likely root cause: **the 250W Tesla M40's power draw spike is tripping the machine's old power supply.**

## Why this happens

The M40 went from:
- **Idle**: just now, `nvidia-smi` showed **16W** (that's all it needed sitting there)
- **Model load**: when llama-server starts, CUDA initializes and pushes ~10GB into the GPU, the card suddenly ramps up toward **170–250W**

On a 2016-era desktop with a likely 400–500W (or aging) PSU, that instant +200W spike can trip over-current protection → **instant power-off**. It comes back on with the power button (which is exactly what you saw — it "shuts down," not "freezes").

> For comparison: the earlier outage during the **model download** was probably different — that's the Killer E2400 NIC freezing under network load (a known Linux `alx` driver quirk). That machine was still *up* the whole time (uptime kept counting).

## My plan once you power it back on

I'll do three things immediately (all remote, no shutdowns):

1. **Cap the GPU power** so the spike never happens:
   ```bash
   sudo nvidia-smi -pm 1        # persistence mode
   sudo nvidia-smi -pl 150      # power-limit to 150W
   ```
   The 14B model still runs fine at 150W (mildly slower, much safer).

2. **Check the logs** for the real killer: PSU/MCE/thermal errors from last boot:
   ```bash
   journalctl -b -1 -p err      # previous boot errors
   sudo dmesg | grep -iE "NVRM|thermal|mce|power"
   ```

3. **Check cooling** — the M40 is a passively-cooled server card (no fan, just a heatsink). What's the airflow in your case like, and does the M40 have its **8-pin power** connected? Also — what's the **PSU wattage** on the label? That'll confirm the diagnosis.

---

**Before you power it on**, could you check two things on the box:
1. When it "shut down," did the **fans/lights actually stop** (full power-off), or did it stay lit but frozen? (power-off = PSU theory confirmed)
2. What's the **PSU wattage** printed on its label?

Power it on when ready, then tell me — I'll connect, cap the GPU power, and check the logs before starting the server again.
