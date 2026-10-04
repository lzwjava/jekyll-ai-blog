---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Monitor Connections Explained
translated: false
type: note
---

Question: If I use HDMI with an RTX 4070, what connectors do I need for one or multiple monitors?

Answer: The RTX 4070 handles this well. Most RTX 4070 cards have **3x DisplayPort 1.4a and 1x HDMI 2.1**, and the card can drive up to 4 displays at once.

**HDMI in this setup**

- The HDMI port is HDMI 2.1, so a good HDMI cable can carry 4K at 120 Hz (and higher with compression).
- Use an **"Ultra High Speed" HDMI 2.1 cable** (48 Gbps certified). An older cable may limit you to 4K 60 Hz or cause flickering.
- Your monitor must also have an HDMI 2.1 port to get the full speed. If the monitor only has HDMI 2.0, you will be capped at about 4K 60 Hz, or 1440p at 144 Hz.

**For multiple monitors**

- The card has only **one HDMI port**, so with 2 or 3 monitors you will need to use DisplayPort for the others.
- Typical setup: Monitor 1 on DisplayPort, Monitor 2 on DisplayPort, Monitor 3 on HDMI.
- If a monitor has no DisplayPort input, use a **DisplayPort-to-HDMI adapter or cable** (active adapters work best for high refresh rates or 4K).

**DisplayPort vs HDMI**

- **DisplayPort 1.4a** is usually the best choice for PC monitors, especially for high refresh rates (144 Hz and above) and G-Sync.
- **HDMI 2.1** is the better choice for TVs or monitors that only have HDMI.

**Quick tips**

- Plug every monitor directly into the GPU, not the motherboard video ports (those use the integrated graphics, not the 4070).
- Check the exact port layout of your specific card model, since a few custom designs differ.
- Set the refresh rate manually in Windows (Settings > Display > Advanced display) after connecting, because it can default to 60 Hz.

If you tell me your monitor models or resolution and refresh rate, I can tell you exactly which cable to buy.

References:

- No external sources were used for this answer.
