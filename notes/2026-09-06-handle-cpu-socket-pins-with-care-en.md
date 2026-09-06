---
audio: false
generated: true
image: false
lang: en
layout: post
title: Handle CPU Socket Pins with Care
translated: false
type: note
---

Question: Are CPU socket pins (针脚) critical components that should never be touched or cleaned with sharp objects, and will bent pins prevent the CPU from booting?

Answer:

Yes, absolutely. CPU socket pins are extremely delicate and critical for proper operation. Here's what you need to know:

**Why pins matter**

Each pin in the socket corresponds to a specific electrical signal — power, data, ground, etc. If even one critical pin is bent or broken, the CPU may fail to POST (Power-On Self-Test) or boot at all. In severe cases, it can cause permanent damage to the motherboard.

**What NOT to do**

- Never use a knife, screwdriver, or any metal tool to clean dirt from the socket
- Never blow aggressively with compressed air at an angle that could bend pins
- Never touch the pins with your fingers (static and oils can cause issues too)
- Never force a CPU into the socket

**If pins are already bent**

It *can* sometimes be repaired carefully using a mechanical pencil (with the lead removed), a fine sewing needle, or a thin plastic card — very gently straightening each pin under magnification. But this is risky and there's no guarantee of success.

**Safe cleaning methods**

- Use **dry compressed air** blown straight-on (not at an angle)
- Use a **soft, dry anti-static brush**
- For stubborn dirt, **99% isopropyl alcohol** on a soft brush (let it fully dry before installing CPU)

**Intel vs AMD note**

- **Intel** (LGA sockets) — pins are on the **motherboard**; bending them damages the motherboard (expensive!)
- **AMD** (AM4/AM5 sockets) — pins are on the **CPU** itself (LGA on AM5); slightly less catastrophic but still serious

So yes, treat the socket pins with extreme care — one careless moment can turn a working system into an expensive paperweight.
