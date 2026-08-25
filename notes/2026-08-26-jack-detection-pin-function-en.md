---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jack Detection Pin Function
translated: false
type: note
---

**Question:** What do jack detection sensor pins do in the front audio header?

**Answer:**

Jack detection pins are signal pins that tell the motherboard's audio chip **whether or not a plug is physically inserted** into the front panel jack.

---

**How it works — step by step:**

**1. No plug inserted**
The jack detection pin is in a default "open" state — the circuit is broken, no signal.

**2. You plug in headphones**
The physical 3.5mm jack has a small mechanical switch inside it. When a plug is inserted, it **closes that switch**, which sends a signal through the detection pin back to the audio codec chip.

**3. Audio codec reacts**
The chip receives the signal and automatically:

- **Activates** the front headphone output
- **Mutes or disables** the rear speaker output (so sound doesn't come from both at once)
- Pops up the Windows/OS notification: *"Audio device connected"*

---

**Why AC'97 (old 7-pin) didn't have this properly:**

The older AC'97 standard handled jack detection differently — it used a **loopback method**, physically rerouting the rear audio signal through the front panel cable. This meant:

- No smart software detection
- Plugging into the front automatically cut off the rear, mechanically — not intelligently
- No OS pop-up prompts
- Less reliable switching

HD Audio (10-pin) replaced this with **dedicated detection pins**, so the audio chip handles everything in software/firmware, which is smarter and more flexible.

---

**Simple analogy:**

Think of it like a **doorbell sensor** — the jack detection pin is the sensor at the door. When a plug (visitor) arrives, the sensor notifies the audio chip (the host), who then decides what to do (switch audio routing).

---

**References:**

- [AAFP Connector Explained — CGDirector](https://www.cgdirector.com/aafp-connector-on-motherboard/)
- [Front Audio Mod: 7-pin to 10-pin discussion — HardForum](https://hardforum.com/threads/front-audio-mod-7-pin-to-10-pin.1325991/)
- [What is AAFP on Motherboard — SunbeamTech](https://sunbeamtech.com/hardware-guides/what-is-aafp-on-motherboard/)
