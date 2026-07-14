---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 Fan Port Means No Included Fan
translated: false
type: note
---

Question: Since the MI50 has a fan port, does that mean I don't need to buy a fan/shroud separately?

Answer:

No — you still need to buy one. The fan port existing just means there's *somewhere to plug a fan in*; it doesn't mean a fan ships with the card.

Here's why: these MI50 cards are pulls from datacenter server sleds, where cooling came from the chassis-level fan wall pushing air through the whole rack, not from anything mounted on the card itself. Sellers pull the card bare — heatsink fins present, fan header present, **no fan attached** — because in its original deployment it never needed one. That's true for almost every listing you'll find on Taobao/eBay/AliExpress for these cards.

So your buy list is unchanged:

1. A small blower fan matching the header's voltage/pin spec (likely a 40mm 12V PWM or DC blower, ~5W class)
2. A shroud/duct to direct that fan's airflow through the heatsink fins (3D printed or a pre-made kit)

**Before you buy anything, check the actual product listing** — some sellers on Taobao specifically bundle a shroud + fan with the card *because* this is such a common gap buyers hit. Search the exact listing page for "风扇" (fan) or "散热" (cooling) in the title/description — if it's not mentioned, assume bare card, no fan.

If your specific card came from a seller who already bundled a fan+shroud, then yes, you're done — but that has to be confirmed from the actual listing, not assumed from the header's presence.
