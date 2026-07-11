---
audio: false
generated: true
image: false
lang: en
layout: post
title: JAUD1 Front Panel Audio Header
translated: false
type: note
---

**Question:** What does JAUD1 mean on the MSI MAG B760M Mortar WiFi motherboard?

**Answer:**

`JAUD1` is the standard label MSI (and most motherboard vendors) use for the **front panel audio header** — a 9-pin (2x5, one pin removed as a key) header on the PCB.

Breakdown of the naming convention:
- `J` = Jumper/connector (generic prefix for any pin header on the board)
- `AUD` = Audio
- `1` = instance number (first one; boards rarely have a second)

**Physical purpose:** it's where you plug in the cable coming from your case's front-panel audio jacks (headphone-out + mic-in on the top/front of your case). The cable is almost always labeled `HD AUDIO` (or `AC'97` on very old cases — don't use that mode on a modern board).

**Pinout** (standard Intel HD Audio front panel spec, which MSI follows):

```
Pin 1: MIC2_L
Pin 2: GND (Ground)
Pin 3: MIC2_R
Pin 4: -ACJ_DETECT (presence detect, no-connect on many boards)
Pin 5: LINE2_R
Pin 6: GND (sense)
Pin 7: FP_IO_R (reserved/key — this is the missing pin slot)
Pin 8: KEY (no pin, physically blocked)
Pin 9: LINE2_L
Pin 10: GND (sense)
```

**Practical steps for your build:**
1. Find `JAUD1` on the bottom-left edge of the board (MSI almost always puts it there, silkscreened).
2. Locate your case's front panel audio cable — should say `HD Audio` on the connector.
3. Plug it in — the connector is keyed (missing pin 8) so it only goes in one orientation.
4. In BIOS, there's usually a setting under Advanced → Onboard Devices to toggle HD Audio vs legacy AC97 mode — leave it on HD Audio (default) for a modern case cable.

If your case cable is old and says `AC'97`, don't force it — it won't work correctly with the default HD Audio setting, and modern boards often don't even support the legacy mode anymore.

No other header on that board (`JFP1`, `JFP2` for power/reset/LEDs, `JUSB1-4` for USB headers, `JCI1` for chassis intrusion) shares this naming pattern by coincidence — it's just MSI's consistent `J + function + number` scheme across their whole lineup, so once you know this you can decode any other header on the silkscreen without pulling up the manual.
